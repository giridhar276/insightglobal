
from functools import lru_cache

@lru_cache(maxsize=32)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Compute Fibonacci numbers
for i in range(10):
    print(fibonacci(i))
