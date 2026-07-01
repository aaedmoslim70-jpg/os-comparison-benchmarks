import psutil
import time
import numpy as np
from config import BENCHMARK_CONFIG

class MemoryBenchmark:
    def __init__(self):
        self.results = {}
    
    def benchmark_memory_allocation(self):
        """قياس سرعة تخصيص الذاكرة"""
        allocation_times = []
        test_size = 5 * 1024 * 1024  # 5 MB
        
        for i in range(3):
            start = time.time()
            data = bytearray(test_size)
            elapsed = time.time() - start
            allocation_times.append(elapsed)
        
        avg_time = np.mean(allocation_times)
        self.results['memory_allocation_time'] = avg_time
        return avg_time
    
    def benchmark_cpu_intensive(self, iterations=100000):
        """قياس أداء CPU"""
        start = time.time()
        result = 0
        for i in range(iterations):
            result += i ** 2
        elapsed = time.time() - start
        operations_per_sec = iterations / elapsed if elapsed > 0 else 0
        self.results['cpu_performance'] = operations_per_sec
        return elapsed
    
    def benchmark_memory_usage(self, duration=3):
        """قياس استخدام الذاكرة"""
        process = psutil.Process()
        memory_samples = []
        
        start = time.time()
        while time.time() - start < duration:
            mem_info = process.memory_info()
            memory_samples.append(mem_info.rss / 1024 / 1024)  # MB
            time.sleep(0.5)
        
        avg_memory = np.mean(memory_samples) if memory_samples else 0
        peak_memory = np.max(memory_samples) if memory_samples else 0
        
        self.results['avg_memory'] = avg_memory
        self.results['peak_memory'] = peak_memory
        return memory_samples
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        try:
            self.benchmark_memory_allocation()
            self.benchmark_cpu_intensive()
            self.benchmark_memory_usage(2)
        except Exception as e:
            print(f"Error in memory benchmark: {e}")
        return self.results
