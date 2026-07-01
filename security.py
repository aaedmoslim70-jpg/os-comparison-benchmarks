import hashlib
import time
import platform
import os

class SecurityBenchmark:
    def __init__(self):
        self.results = {}
    
    def benchmark_hashing(self, data_size_mb=100):
        """قياس سرعة عمليات الـ Hashing"""
        print(f"\n📊 قياس عمليات Hashing على {data_size_mb}MB...")
        
        data = b'X' * (data_size_mb * 1024 * 1024)
        
        algorithms = ['md5', 'sha256', 'sha512']
        
        for algo in algorithms:
            start = time.time()
            hasher = hashlib.new(algo)
            hasher.update(data)
            elapsed = time.time() - start
            
            throughput = data_size_mb / elapsed
            print(f"✅ {algo.upper()}: {elapsed:.4f}s ({throughput:.2f} MB/s)")
            
            self.results[f'hash_{algo}_throughput'] = throughput
        
        return self.results
    
    def benchmark_encryption_simulation(self, iterations=10000):
        """محاكاة عمليات التشفير"""
        print(f"\n📊 محاكاة عمليات التشفير ({iterations:,} تكرار)...")
        
        start = time.time()
        
        for i in range(iterations):
            _ = hashlib.sha256(f'encryption_test_{i}'.encode()).hexdigest()
        
        elapsed = time.time() - start
        ops_per_sec = iterations / elapsed
        
        print(f"✅ الوقت: {elapsed:.4f} ثانية")
        print(f"⚡ العمليات/الثانية: {ops_per_sec:,.0f}")
        
        self.results['encryption_ops_per_sec'] = ops_per_sec
        return elapsed
    
    def check_security_features(self):
        """التحقق من ميزات الأمان في النظام"""
        print("\n🔒 فحص ميزات الأمان...")
        
        features = {
            'os': platform.system(),
            'aslr_available': self._check_aslr(),
            'file_permissions': self._check_file_permissions(),
        }
        
        self.results['security_features'] = features
        return features
    
    def _check_aslr(self):
        """التحقق من ASLR"""
        if platform.system() == "Linux":
            try:
                with open('/proc/sys/kernel/randomize_va_space', 'r') as f:
                    return int(f.read().strip()) > 0
            except:
                return False
        return None
    
    def _check_file_permissions(self):
        """التحقق من أذونات الملفات"""
        test_file = '/tmp/test_perms.txt' if platform.system() != "Windows" else os.environ.get('TEMP') + '\\test_perms.txt'
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except:
            return False
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        print("🔄 بدء قياسات الأمان...")
        self.benchmark_hashing(50)
        self.benchmark_encryption_simulation(10000)
        self.check_security_features()
        return self.results