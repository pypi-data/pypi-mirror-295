import os
import struct
from functools import lru_cache
from itertools import accumulate

import numpy as np
import torch


def print_rank_0(*message):
    """If distributed is initialized print only on rank 0."""
    if torch.distributed.is_initialized():
        if torch.distributed.get_rank() == 0:
            print(*message, flush=True)
    else:
        print(*message, flush=True)


def make_dataset(path):
    if not IndexedDataset.exists(path):
        print(f"Dataset does not exist: {path}")
        print(
            "Path should be a basename that both .idx and .bin can be appended to get full filenames."
        )
        return None
    if MMapIndexedDataset.exists(path):
        return MMapIndexedDataset(path)
    return None


def read_longs(f, n):
    a = np.empty(n, dtype=np.int64)
    f.readinto(a)
    return a


dtypes = {
    1: np.uint8,
    2: np.int8,
    3: np.int16,
    4: np.int32,
    5: np.int64,
    6: np.float32,
    7: np.float64,
    8: np.uint16,
}


def code(dtype):
    for k in dtypes.keys():
        if dtypes[k] == dtype:
            return k
    raise ValueError(dtype)


def index_file_path(prefix_path):
    return prefix_path + ".idx"


def data_file_path(prefix_path):
    return prefix_path + ".bin"


class IndexedDataset(torch.utils.data.Dataset):
    """Loader for IndexedDataset"""

    _HDR_MAGIC = b"TNTIDX\x00\x00"

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.data_file = None
        self.read_index(path)

    def read_index(self, path):
        with open(index_file_path(path), "rb") as f:
            magic = f.read(8)
            assert magic == self._HDR_MAGIC, (
                "Index file doesn't match expected format. "
                "Make sure that --dataset-impl is configured properly."
            )
            version = f.read(8)
            assert struct.unpack("<Q", version) == (1,)
            code, self.element_size = struct.unpack("<QQ", f.read(16))
            self.dtype = dtypes[code]
            self._len, self.s = struct.unpack("<QQ", f.read(16))
            self.doc_count = struct.unpack("<Q", f.read(8))
            self.dim_offsets = read_longs(f, self._len + 1)
            self.data_offsets = read_longs(f, self._len + 1)
            self.sizes = read_longs(f, self.s)
            self.doc_idx = read_longs(f, self.doc_count)

    def read_data(self, path):
        self.data_file = open(data_file_path(path), "rb", buffering=0)

    def check_index(self, i):
        if i < 0 or i >= self._len:
            raise IndexError("index out of range")

    def __del__(self):
        if self.data_file:
            self.data_file.close()

    # @lru_cache(maxsize=8)
    def __getitem__(self, idx):
        if not self.data_file:
            self.read_data(self.path)
        if isinstance(idx, int):
            i = idx
            self.check_index(i)
            tensor_size = self.sizes[self.dim_offsets[i] : self.dim_offsets[i + 1]]
            a = np.empty(tensor_size, dtype=self.dtype)
            self.data_file.seek(self.data_offsets[i] * self.element_size)
            self.data_file.readinto(a)
            return a
        elif isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))
            if step != 1:
                raise ValueError("Slices into indexed_dataset must be contiguous")
            sizes = self.sizes[self.dim_offsets[start] : self.dim_offsets[stop]]
            size = sum(sizes)
            a = np.empty(size, dtype=self.dtype)
            self.data_file.seek(self.data_offsets[start] * self.element_size)
            self.data_file.readinto(a)
            offsets = list(accumulate(sizes))
            sents = np.split(a, offsets[:-1])
            return sents

    def __len__(self):
        return self._len

    def size(self, index):
        return self.sizes[index]

    @staticmethod
    def exists(path):
        return os.path.exists(index_file_path(path)) and os.path.exists(
            data_file_path(path)
        )

    @property
    def supports_prefetch(self):
        return False  # avoid prefetching to save memory


class MMapIndexedDataset(torch.utils.data.Dataset):
    class Index(object):
        _HDR_MAGIC = b"MMIDIDX\x00\x00"

        @classmethod
        def writer(cls, path, dtype):
            class _Writer(object):
                def __enter__(self):
                    self._file = open(path, "wb")

                    # Write Magic string so we can check the file format then opening it again.
                    self._file.write(cls._HDR_MAGIC)
                    # Write version number
                    # Little endian unsigned 64 Bit integer
                    self._file.write(struct.pack("<Q", 1))
                    # Little endian unsigned 8 Bit integer
                    self._file.write(struct.pack("<B", code(dtype)))

                    return self

                @staticmethod
                def _get_pointers(sizes):
                    pointers = np.zeros(len(sizes), dtype=np.int64)
                    sizes = np.array(sizes, dtype=np.int64)

                    np.cumsum(sizes[:-1], out=pointers[1:])
                    pointers = pointers * dtype().itemsize
                    return pointers

                def write(self, sizes, doc_idx):
                    pointers = self._get_pointers(sizes)

                    # Little endian unsigned 64 Bit integer
                    self._file.write(struct.pack("<Q", len(sizes)))
                    # Little endian unsigned 64 Bit integer
                    self._file.write(struct.pack("<Q", len(doc_idx)))

                    sizes = np.array(sizes, dtype=np.int32)
                    self._file.write(sizes.tobytes(order="C"))
                    del sizes

                    pointers = np.array(pointers, dtype=np.int64)
                    self._file.write(pointers.tobytes(order="C"))
                    del pointers

                    doc_idx = np.array(doc_idx, dtype=np.int64)
                    self._file.write(doc_idx.tobytes(order="C"))

                def __exit__(self, exc_type, exc_val, exc_tb):
                    self._file.close()

            return _Writer()

        def __init__(self, path):
            with open(path, "rb") as stream:
                magic_test = stream.read(9)
                assert self._HDR_MAGIC == magic_test, (
                    "Index file doesn't match expected format. "
                    "Make sure that --dataset-impl is configured properly."
                )
                # Little endian unsigned 64 Bit integer
                version = struct.unpack("<Q", stream.read(8))
                assert (1,) == version

                # Little endian unsigned 8 Bit integer
                (dtype_code,) = struct.unpack("<B", stream.read(1))
                self._dtype = dtypes[dtype_code]
                self._dtype_size = self._dtype().itemsize

                self._len = struct.unpack("<Q", stream.read(8))[0]
                self._doc_count = struct.unpack("<Q", stream.read(8))[0]
                offset = stream.tell()

            self._bin_buffer_mmap = np.memmap(path, mode="r", order="C")
            self._bin_buffer = memoryview(self._bin_buffer_mmap)
            print_rank_0("    reading sizes...")
            self._sizes = np.frombuffer(
                self._bin_buffer, dtype=np.int32, count=self._len, offset=offset
            )
            print_rank_0("    reading pointers...")
            self._pointers = np.frombuffer(
                self._bin_buffer,
                dtype=np.int64,
                count=self._len,
                offset=offset + self._sizes.nbytes,
            )
            print_rank_0("    reading document index...")
            self._doc_idx = np.frombuffer(
                self._bin_buffer,
                dtype=np.int64,
                count=self._doc_count,
                offset=offset + self._sizes.nbytes + self._pointers.nbytes,
            )

        def __del__(self):
            self._bin_buffer_mmap._mmap.close()
            del self._bin_buffer_mmap

        @property
        def dtype(self):
            return self._dtype

        @property
        def sizes(self):
            return self._sizes

        @property
        def doc_idx(self):
            return self._doc_idx

        @lru_cache(maxsize=8)
        def __getitem__(self, i):
            return self._pointers[i], self._sizes[i]

        def __len__(self):
            return self._len

    def __init__(self, path):
        super().__init__()

        self._path = None
        self._index = None
        self._bin_buffer = None

        self._do_init(path)

    def __getstate__(self):
        return self._path

    def __setstate__(self, state):
        self._do_init(state)

    def _do_init(self, path):
        self._path = path
        self._index = self.Index(index_file_path(self._path))

        print_rank_0("    creating numpy buffer of mmap...")
        self._bin_buffer_mmap = np.memmap(
            data_file_path(self._path), mode="r", order="C"
        )
        print_rank_0("    creating memory view of numpy buffer...")
        self._bin_buffer = memoryview(self._bin_buffer_mmap)

    def __del__(self):
        self._bin_buffer_mmap._mmap.close()
        del self._bin_buffer_mmap
        del self._index

    def __len__(self):
        return len(self._index)

    # @lru_cache(maxsize=8)
    def __getitem__(self, idx):
        if isinstance(idx, int):
            ptr, size = self._index[idx]
            np_array = np.frombuffer(
                self._bin_buffer, dtype=self._index.dtype, count=size, offset=ptr
            )
            return np_array
        elif isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))
            if step != 1:
                raise ValueError("Slices into indexed_dataset must be contiguous")
            ptr = self._index._pointers[start]
            sizes = self._index._sizes[idx]
            offsets = list(accumulate(sizes))
            total_size = sum(sizes)
            np_array = np.frombuffer(
                self._bin_buffer, dtype=self._index.dtype, count=total_size, offset=ptr
            )
            sents = np.split(np_array, offsets[:-1])
            return sents

    def get(self, idx, offset=0, length=None):
        """Retrieves a single item from the dataset with the option to only
        return a portion of the item.

        get(idx) is the same as [idx] but get() does not support slicing.
        """
        ptr, size = self._index[idx]
        if length is None:
            length = size - offset
        ptr += offset * np.dtype(self._index.dtype).itemsize
        np_array = np.frombuffer(
            self._bin_buffer, dtype=self._index.dtype, count=length, offset=ptr
        )
        return np_array

    @property
    def sizes(self):
        return self._index.sizes

    @property
    def doc_idx(self):
        return self._index.doc_idx

    def get_doc_idx(self):
        return self._index._doc_idx

    def set_doc_idx(self, doc_idx_):
        self._index._doc_idx = doc_idx_

    @property
    def supports_prefetch(self):
        return False

    @staticmethod
    def exists(path):
        return os.path.exists(index_file_path(path)) and os.path.exists(
            data_file_path(path)
        )
