import secrets
from queue import Full, Empty


import multiprocessing.shared_memory as sm


class StaticDeque:
    # A deque like implementation of a double ended queue.
    # It can be pickled and used on multi processes.
    # Non block, not thread safe
    # Note: To handle chunk size behevaior of windows, we slice against self._memsize instead against buf.nbytes
    # Performance: mp.Queue runs about 30-40 % faster. However, it is not pickleable.

    # todo unbound operation
    # todo rotate instead raising

    def __init__(self, maxsize, byte_length):
        self.length = byte_length
        self._maxsize = maxsize
        self._memsize = self._maxsize * self.length
        self.data = sm.SharedMemory(
            name=f"seq_{id(self)}_{secrets.token_hex(4)}",
            create=True,
            size= self._memsize
        )
        self._last = sm.SharedMemory(name=f"last_{id(self)}", create=True, size=4)

    @property
    def last(self) -> int:
        return int.from_bytes(self._last.buf[:4], "big")

    @last.setter
    def last(self, v: int):
        self._last.buf[:4] = v.to_bytes(4, "big")

    @property
    def is_empty(self):
        return not bool(self.last)

    @property
    def is_full(self):
        return self.__len__() >= self._maxsize

    def append(self, item: bytes):
        if not self.is_full:
            self.data.buf[self.last:self.last+self.length] = item
            self.last = self.last + self.length
        else:
            raise Full

    def append_left(self, item: bytes):
        if not self.is_full:
            seq = self.data.buf[:]
            data_copy = seq[:self._memsize].tobytes()
            seq[:self.length] = item
            seq[self.length:self._memsize] = data_copy[:seq.nbytes - self.length]
            self.last = self.last + self.length
        else:
            raise Full

    def pop(self):
        if not self.is_empty:
            penumilate = self.last - self.length
            res = self.data.buf[penumilate:self.last].tobytes()
            self.data.buf[penumilate:self.last] = bytes(self.length)
            self.last = self.last - self.length
            return res
        else:
            raise Empty

    def pop_left(self):
        if not self.is_empty:
            res = self.data.buf[:self.length].tobytes()
            mem = self.data.buf[self.length:self._memsize]
            self.data.buf[:self._memsize - self.length] = mem
            self.last = self.last - self.length
            return res
        else:
            raise Empty

    def __repr__(self):
         res = ""
         for idx in range(self._maxsize):
            start = idx * self.length
            end = start + self.length
            item = self.data.buf[start:end].tobytes()
            if item != bytes(self.length):
                res += str(self.data.buf[start:end].tobytes()) + ","
         return f"{self.__class__.__name__}([{res}], maxsize={self._maxsize}, byte_length={self.length})"

    def __len__(self):
        return self.last // self.length
