import time
from typing import Callable, Any
from functools import wraps


class Timer:
    """Simple timer for benchmarking."""
    
    def __init__(self):
        self._start: float | None = None
        self._laps: list[float] = []
    
    def start(self) -> 'Timer':
        """Start the timer."""
        self._start = time.perf_counter()
        return self
    
    def stop(self) -> float:
        """Stop and return elapsed time in milliseconds."""
        if self._start is None:
            raise RuntimeError("Timer not started")
        
        elapsed = (time.perf_counter() - self._start) * 1000
        self._laps.append(elapsed)
        self._start = None
        return elapsed
    
    def lap(self) -> float:
        """Get current elapsed time without stopping."""
        if self._start is None:
            raise RuntimeError("Timer not started")
        return (time.perf_counter() - self._start) * 1000
    
    def reset(self) -> 'Timer':
        """Reset timer and clear laps."""
        self._start = None
        self._laps = []
        return self
    
    @property
    def laps(self) -> list[float]:
        return self._laps.copy()
    
    @property
    def total(self) -> float:
        return sum(self._laps)
    
    @property
    def average(self) -> float:
        return self.total / len(self._laps) if self._laps else 0.0
    
    @property
    def min(self) -> float:
        return min(self._laps) if self._laps else 0.0
    
    @property
    def max(self) -> float:
        return max(self._laps) if self._laps else 0.0


def timed(func: Callable) -> Callable:
    """Decorator that prints execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{func.__name__}: {elapsed:.2f}ms")
        return result
    return wrapper


def benchmark(iterations: int = 100):
    """Decorator that benchmarks a function over multiple iterations."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            times = []
            result = None
            
            for _ in range(iterations):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                times.append(elapsed)
            
            avg = sum(times) / len(times)
            min_t = min(times)
            max_t = max(times)
            
            print(f"{func.__name__} ({iterations} runs):")
            print(f"  avg: {avg:.2f}ms | min: {min_t:.2f}ms | max: {max_t:.2f}ms")
            
            return result
        return wrapper
    return decorator