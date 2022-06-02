from multiprocessing import Queue
from timeit import timeit

from shared_memory_deque import StaticDeque

def mp_queue():
    item = "dakfjaöldfjaöljdföadjföaldjföaldjflakdsöfjöladjföasldjföadjföaljdf".encode()
    q = Queue()

    for _ in range(10_000):
        q.put(item)
    for _ in range(10_000):
        q.get()

def static_deque():
    item = "dakfjaöldfjaöljdföadjföaldjföaldjflakdsöfjöladjföasldjföadjföaljdf".encode()
    q = StaticDeque(10_000, len(item))
    for _ in range(10_000):
        q.append(item)
    for _ in range(10_000):
        q.pop_left()

def q_timeit():
    time_d = timeit("static_deque()", number=10, globals=globals())
    time_mp = timeit("mp_queue()", number=10, globals=globals())
    ratio = (1 - time_mp / time_d) * 100
    print(f"Result static deque {time_d:.2f} s.\n"
          f"Result mp queue  {time_mp:.2f} s.\n"
          f"{ratio:.0f} % slower.")


if __name__ == "__main__":
    q_timeit()
