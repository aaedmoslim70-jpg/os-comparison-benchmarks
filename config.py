import platform
import os
from datetime import datetime

# معلومات النظام
SYSTEM_INFO = {
    'os': platform.system(),
    'platform': platform.platform(),
    'processor': platform.processor(),
    'python_version': platform.python_version(),
    'architecture': platform.architecture()[0],
    'timestamp': datetime.now().isoformat()
}

# إعدادات Benchmarks
BENCHMARK_CONFIG = {
    'cpu_iterations': 100000,
    'memory_test_size': 50 * 1024 * 1024,  # 50 MB
    'process_count': 5,
    'duration_seconds': 10,
    'file_size_mb': 20
}

# المجلدات
RESULTS_DIR = 'results'
BENCHMARKS_DIR = 'benchmarks'

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs('logs', exist_ok=True)
