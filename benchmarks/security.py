import hashlib
import time
import platform
import os

class SecurityBenchmark:
    def __init__(self):
        self.results = {}
    
    def benchmark_hashing(self, data_size_mb=10):
        """قياس سرعة Hashing"""
        data = b'X' * (data_size_mb * 1024 * 1024)
        algorithms = ['md5', 'sha256']
        
        try:
            for algo in algorithms:
                start = time.time()
                hasher = hashlib.new(algo)
                hasher.update(data)
                elapsed = time.time() - start
                throughput = data_size_mb / elapsed if elapsed > 0 else 0
                self.results[f'hash_{algo}_throughput'] = throughput
        except Exception as e:
            print(f"Error in hashing: {e}")
        
        return self.results
    
    def benchmark_encryption_simulation(self, iterations=5000):
        """محاكاة التشفير"""
        start = time.time()
        
        try:
            for i in range(iterations):
                _ = hashlib.sha256(f'test_{i}'.encode()).hexdigest()
        except Exception as e:
            print(f"Error in encryption simulation: {e}")
        
        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed if elapsed > 0 else 0
        self.results['encryption_ops_per_sec'] = ops_per_sec
        return elapsed
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        try:
            self.benchmark_hashing(5)
            self.benchmark_encryption_simulation(3000)
        except Exception as e:
            print(f"Error in security benchmark: {e}")
        return self.results
