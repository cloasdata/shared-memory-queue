from shared_memory_deque import StaticDeque
from line_profiler import LineProfiler


def lp_pop_left():
    # shows the bottleneck
    load = b"https://docs.python.org/3/library/multiprocessing.shared_memory.html#multiprocessing.shared_memory.SharedMemory"
    times = 10_000


    def run_append():
        d = StaticDeque(times, len(load))

        for _ in range(times):
            d.append(load)

        for _ in range(times):
            d.pop_left()

    d = StaticDeque(times, len(load))
    for _ in range(times):
        d.append(load)
    lp = LineProfiler()
    lp.add_function(d.pop_left)
    lp(run_append)()
    lp.print_stats()

if __name__ == "__main__":
    lp_pop_left()