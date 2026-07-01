import os
import time
import tempfile
import platform

class FileSystemBenchmark:
    def __init__(self):
        self.results = {}
        self.test_dir = tempfile.mkdtemp()
    
    def benchmark_file_creation(self, num_files=50):
        """قياس سرعة إنشاء الملفات"""
        start = time.time()
        
        try:
            for i in range(num_files):
                filepath = os.path.join(self.test_dir, f'test_file_{i}.txt')
                with open(filepath, 'w') as f:
                    f.write(f"Test file {i}\n" * 10)
        except Exception as e:
            print(f"Error creating files: {e}")
        
        elapsed = time.time() - start
        self.results['file_creation_time'] = elapsed
        return elapsed
    
    def benchmark_file_write(self, file_size_mb=10):
        """قياس سرعة الكتابة"""
        filepath = os.path.join(self.test_dir, 'large_file.bin')
        data = b'X' * (1024 * 1024)  # 1 MB
        
        start = time.time()
        
        try:
            with open(filepath, 'wb') as f:
                for _ in range(file_size_mb):
                    f.write(data)
        except Exception as e:
            print(f"Error writing file: {e}")
        
        elapsed = time.time() - start
        throughput = file_size_mb / elapsed if elapsed > 0 else 0
        self.results['file_write_throughput'] = throughput
        return elapsed
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        try:
            self.benchmark_file_creation(30)
            self.benchmark_file_write(5)
        except Exception as e:
            print(f"Error in filesystem benchmark: {e}")
        return self.results
