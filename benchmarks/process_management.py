import psutil
import time
import subprocess
import platform
import threading
from datetime import datetime

class ProcessManagementBenchmark:
    def __init__(self):
        self.os_type = platform.system()
        self.results = {}
    
    def benchmark_process_creation(self, num_processes=5):
        """قياس سرعة إنشاء العمليات"""
        start_time = time.time()
        processes = []
        
        try:
            if self.os_type == "Windows":
                for i in range(num_processes):
                    p = subprocess.Popen(['cmd', '/c', 'echo hello'], 
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                    processes.append(p)
            else:
                for i in range(num_processes):
                    p = subprocess.Popen(['echo', 'hello'],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                    processes.append(p)
            
            for p in processes:
                p.wait(timeout=5)
            
            elapsed = time.time() - start_time
            self.results['process_creation_time'] = elapsed
            return elapsed
        except Exception as e:
            print(f"Error in process creation: {e}")
            self.results['process_creation_time'] = 0
            return 0
    
    def benchmark_thread_creation(self, num_threads=10):
        """قياس إنشاء الخيوط"""
        threads = []
        
        def worker():
            time.sleep(0.05)
        
        start_time = time.time()
        
        for i in range(num_threads):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join(timeout=5)
        
        elapsed = time.time() - start_time
        self.results['thread_creation_time'] = elapsed
        return elapsed
    
    def run_all(self):
        """تشغيل جميع الاختبارات"""
        try:
            self.benchmark_process_creation(3)
            self.benchmark_thread_creation(5)
        except Exception as e:
            print(f"Error in process management: {e}")
        return self.results
