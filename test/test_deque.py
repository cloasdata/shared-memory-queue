import random
import multiprocessing as mp
import pickle

import pytest

from src.sharedmemqueue.shm_queue import StaticDeque


def random_item(length=2) -> bytes:
    return random.randint(0,24000).to_bytes(length,"big")


class TestStaticDeque:
    # todo raise full / empty
    def test_init(self):
        d = StaticDeque(10, 4)
        assert str(d)

    def test_is_empty(self):
        d = StaticDeque(1, 1)
        assert d.is_empty

    def test_is_full(self):
        d = StaticDeque(1, 1)
        d.append(b"1")
        assert d.is_full

    def test_put(self):
        d = StaticDeque(10, 2)
        items = [random_item() for _ in range(10)]
        for item in items:
            d.append(item)
            print(d.last)
        assert len(d) == 10
        assert d.data.buf.tobytes() == b"".join(items)

    def test_put_left(self):
        d = StaticDeque(10, 2)
        items = [random_item() for _ in range(10)]
        for item in items:
            d.append_left(item)
        assert len(d) == 10
        assert d.data.buf.tobytes() == b"".join(reversed(items))

    def test_pop(self):
        d = StaticDeque(10, 2)
        items = [random_item() for _ in range(10)]
        for item in items:
            d.append(item)
        result = [d.pop() for _ in range(d._maxsize)]
        assert result == list(reversed(items))

    def test_pop_left(self):
        d = StaticDeque(10, 2)
        items = [random_item() for _ in range(10)]
        for item in items:
            d.append(item)
        result = [d.pop_left() for _ in range(d._maxsize)]
        assert result == items

    def test_repr(self):
        d = StaticDeque(10, 2)
        assert repr(d) == "StaticDeque([], maxsize=10, byte_length=2)"
        d.append(b'23')
        assert repr(d) == "StaticDeque([b'23',], maxsize=10, byte_length=2)"
        d.append(b'23')
        assert repr(d) == "StaticDeque([b'23',b'23',], maxsize=10, byte_length=2)"

    def test_pickleable(self):
        d = StaticDeque(10, 2)
        assert pickle.dumps(d)

        d.append(random_item())
        b = pickle.dumps(d)
        c = pickle.loads(b)
        assert c



class TestIntegration:
    def test_producer_consumer_sync(self, capsys):
        maxitems = 10
        length = 2
        work = [random_item(length) for _ in range(maxitems)]
        q = StaticDeque(maxitems, length)

        def consumer(q: StaticDeque):
            print("Starting to consume until empty")
            res = []
            while not q.is_empty:
                item = q.pop()
                res.append(item)

            print("Empty. Reverse direction")
            while res:
                q.append_left(res.pop())
            print("Consumer bye")

        def producer(q:StaticDeque, work):
            for item in work:
                q.append(item)

        pp = mp.Process(target=producer, args=(q, work))
        pp.run()
        cp = mp.Process(target=consumer, args=(q,))
        cp.run()
        assert [q.pop() for _ in range(q._maxsize)] == work
