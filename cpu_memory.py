import psutil
import time
import numpy as np
from config import BENCHMARK_CONFIG

class MemoryBenchmark:
    def __init__(self):
        self.results = {}
    
    def benchmark_memory_allocation(self):
        """قياس سرعة تخصيص الذاكرة"""
        print("\n📊 قياس تخصيص الذاكرة...")
        
        allocation_times = []
        test_size = 10 * 1024 * 1024  # 10 MB
        
        for i in range(5):
            start = time.time()
            data = bytearray(test_size)
            elapsed = time.time() - start
            allocation_times.append(elapsed)
        
        avg_time = np.mean(allocation_times)
        print(f"✅ متوسط وقت تخصيص 10MB: {avg_time*1000:.2f} ms")
        
        self.results['memory_allocation_time'] = avg_time
        return avg_time
    
    def benchmark_memory_access(self, array_size=10**7):
        """قياس سرعة الوصول للذاكرة"""
        print("\n📊 قياس سرعة الوصول للذاكرة...")
        
        arr = np.random.random(array_size)
        
        start = time.time()
        # عملية وصول متسلسل
        result = 0
        for i in range(0, array_size, 1000):
            result += arr[i]
        elapsed_sequential = time.time() - start
        
        start = time.time()
        # عملية وصول عشوائي
        indices = np.random.randint(0, array_size, 10000)
        result = np.sum(arr[indices])
        elapsed_random = time.time() - start
        
        print(f"✅ وصول متسلسل: {elapsed_sequential*1000:.2f} ms")
        print(f"✅ وصول عشوائي: {elapsed_random*1000:.2f} ms")
        
        self.results['memory_sequential_access'] = elapsed_sequential
        self.results['memory_random_access'] = elapsed_random
        
        return elapsed_sequential, elapsed_random
    
    def benchmark_cpu_intensive(self, iterations=1000000):
        """قياس أداء CPU في عمليات حسابية"""
        print(f"\n📊 قياس أداء CPU ({iterations:,} عملية)...")
        
        start = time.time()
        
        result = 0
        for i in range(iterations):
            result += i ** 2
        
        elapsed = time.time() - start
        operations_per_sec = iterations / elapsed
        
        print(f"✅ الوقت: {elapsed:.4f} ثانية")
        print(f"⚡ العمليات/الثانية: {operations_per_sec:,.0f}")
        
        self.results['cpu_performance'] = operations_per_sec
        return elapsed
    
    def benchmark_memory_usage(self, duration=10):
        """قياس استخدام الذاكرة"""
        print(f"\n📊 مراقبة الذاكرة لمدة {duration} ثواني...")
        
        process = psutil.Process()
        memory_samples = []
        
        start = time.time()
        while time.time() - start < duration:
            mem_info = process.memory_info()
            memory_samples.append(mem_info.rss / 1024 / 1024)  # MB
            time.sleep(1)
        
        avg_memory = np.mean(memory_samples)
        peak_memory = np.max(memory_samples)
        
        print(f"✅ متوسط الذاكرة: {avg_memory:.2f} MB")
        print(f"✅ ذروة الذاكرة: {peak_memory:.2f} MB")
        
        self.results['avg_memory'] = avg_memory
        self.results['peak_memory'] = peak_memory
        
        return memory_samples
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        print("🔄 بدء قياسات الذاكرة والمعالج...")
        self.benchmark_memory_allocation()
        self.benchmark_memory_access()
        self.benchmark_cpu_intensive()
        self.benchmark_memory_usage(5)
        return self.results