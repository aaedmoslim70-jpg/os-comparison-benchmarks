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
    'cpu_iterations': 1000000,
    'memory_test_size': 100 * 1024 * 1024,  # 100 MB
    'process_count': 10,
    'duration_seconds': 30,
    'file_size_mb': 50
}

# المجلدات
RESULTS_DIR = 'results'
BENCHMARKS_DIR = 'benchmarks'

os.makedirs(RESULTS_DIR, exist_ok=True)