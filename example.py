from shared_memory_deque import StaticDeque

deque = StaticDeque(10, 2)
deque.append(b"ed")
print(deque.pop())

