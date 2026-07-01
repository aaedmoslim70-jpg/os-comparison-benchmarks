import psutil
import time
import subprocess
import platform
from datetime import datetime

class ProcessManagementBenchmark:
    def __init__(self):
        self.os_type = platform.system()
        self.results = {}
    
    def benchmark_process_creation(self, num_processes=10):
        """قياس سرعة إنشاء العمليات"""
        print(f"\n📊 قياس إنشاء {num_processes} عمليات...")
        
        start_time = time.time()
        processes = []
        
        try:
            if self.os_type == "Windows":
                for i in range(num_processes):
                    p = subprocess.Popen(['cmd', '/c', 'echo hello'], 
                                        stdout=subprocess.DEVNULL)
                    processes.append(p)
            else:  # Linux, macOS
                for i in range(num_processes):
                    p = subprocess.Popen(['echo', 'hello'],
                                        stdout=subprocess.DEVNULL)
                    processes.append(p)
            
            for p in processes:
                p.wait()
            
            elapsed = time.time() - start_time
            self.results['process_creation_time'] = elapsed
            
            print(f"✅ وقت إنشاء {num_processes} عمليات: {elapsed:.4f} ثانية")
            print(f"⏱️ متوسط لكل عملية: {elapsed/num_processes*1000:.2f} ms")
            
            return elapsed
        
        except Exception as e:
            print(f"❌ خطأ: {e}")
            return None
    
    def benchmark_process_switching(self, duration=5):
        """قياس سرعة تبديل العمليات (Context Switching)"""
        print(f"\n📊 قياس تبديل العمليات لمدة {duration} ثواني...")
        
        start_time = time.time()
        context_switches = 0
        
        process = psutil.Process()
        ctx_before = process.num_ctx_switches()
        
        while time.time() - start_time < duration:
            # عملية حسابية مكثفة
            for _ in range(10000):
                _ = sum([i**2 for i in range(100)])
        
        ctx_after = process.num_ctx_switches()
        context_switches = ctx_after.voluntary + ctx_after.involuntary
        
        print(f"✅ عدد تبديلات السياق: {context_switches}")
        print(f"⏱️ تبديلات في الثانية: {context_switches/duration:.0f}")
        
        self.results['context_switches'] = context_switches
        return context_switches
    
    def benchmark_thread_creation(self, num_threads=50):
        """قياس إنشاء الخيوط (Threads)"""
        import threading
        
        print(f"\n📊 قياس إنشاء {num_threads} خيط...")
        
        threads = []
        
        def worker():
            time.sleep(0.1)
        
        start_time = time.time()
        
        for i in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        elapsed = time.time() - start_time
        self.results['thread_creation_time'] = elapsed
        
        print(f"✅ وقت إنشاء {num_threads} خيط: {elapsed:.4f} ثانية")
        
        return elapsed
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        print("🔄 بدء قياسات إدارة العمليات...")
        self.benchmark_process_creation(10)
        self.benchmark_process_switching(3)
        self.benchmark_thread_creation(50)
        return self.results