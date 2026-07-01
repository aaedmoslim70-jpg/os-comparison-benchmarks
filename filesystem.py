import os
import time
import tempfile
import platform

class FileSystemBenchmark:
    def __init__(self):
        self.results = {}
        self.test_dir = tempfile.mkdtemp()
    
    def benchmark_file_creation(self, num_files=100):
        """قياس سرعة إنشاء الملفات"""
        print(f"\n📊 قياس إنشاء {num_files} ملف...")
        
        start = time.time()
        
        for i in range(num_files):
            filepath = os.path.join(self.test_dir, f'test_file_{i}.txt')
            with open(filepath, 'w') as f:
                f.write(f"Test file {i}\n" * 100)
        
        elapsed = time.time() - start
        files_per_sec = num_files / elapsed
        
        print(f"✅ وقت الإنشاء: {elapsed:.4f} ثانية")
        print(f"📄 ملفات/الثانية: {files_per_sec:.0f}")
        
        self.results['file_creation_time'] = elapsed
        return elapsed
    
    def benchmark_file_read(self, num_files=100):
        """قياس سرعة قراءة الملفات"""
        print(f"\n📊 قياس قراءة {num_files} ملف...")
        
        start = time.time()
        
        for i in range(num_files):
            filepath = os.path.join(self.test_dir, f'test_file_{i}.txt')
            with open(filepath, 'r') as f:
                _ = f.read()
        
        elapsed = time.time() - start
        files_per_sec = num_files / elapsed
        
        print(f"✅ وقت القراءة: {elapsed:.4f} ثانية")
        print(f"📄 ملفات/الثانية: {files_per_sec:.0f}")
        
        self.results['file_read_time'] = elapsed
        return elapsed
    
    def benchmark_file_write(self, file_size_mb=50):
        """قياس سرعة الكتابة على الملفات"""
        print(f"\n📊 قياس كتابة ملف {file_size_mb}MB...")
        
        filepath = os.path.join(self.test_dir, 'large_file.bin')
        data = b'X' * (1024 * 1024)  # 1 MB
        
        start = time.time()
        
        with open(filepath, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data)
        
        elapsed = time.time() - start
        throughput = file_size_mb / elapsed
        
        print(f"✅ وقت الكتابة: {elapsed:.4f} ثانية")
        print(f"⚡ الإنتاجية: {throughput:.2f} MB/s")
        
        self.results['file_write_throughput'] = throughput
        return elapsed
    
    def benchmark_directory_operations(self, num_dirs=50):
        """قياس عمليات المجلدات"""
        print(f"\n📊 قياس إنشاء {num_dirs} مجلد...")
        
        start = time.time()
        
        for i in range(num_dirs):
            dir_path = os.path.join(self.test_dir, f'dir_{i}')
            os.makedirs(dir_path, exist_ok=True)
        
        elapsed = time.time() - start
        dirs_per_sec = num_dirs / elapsed
        
        print(f"✅ وقت الإنشاء: {elapsed:.4f} ثانية")
        print(f"📁 مجلدات/الثانية: {dirs_per_sec:.0f}")
        
        self.results['directory_creation_time'] = elapsed
        return elapsed
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        print("🔄 بدء قياسات نظام الملفات...")
        self.benchmark_file_creation(100)
        self.benchmark_file_read(100)
        self.benchmark_file_write(20)
        self.benchmark_directory_operations(50)
        return self.results