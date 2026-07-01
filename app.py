from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import platform
from datetime import datetime
import threading
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Import benchmarks
from benchmarks.cpu_memory import MemoryBenchmark
from benchmarks.filesystem import FileSystemBenchmark
from benchmarks.process_management import ProcessManagementBenchmark
from benchmarks.security import SecurityBenchmark
from config import SYSTEM_INFO, RESULTS_DIR
from utils.logger import setup_logger

logger = setup_logger()
benchmark_results = {}
benchmark_status = {'running': False, 'progress': 0, 'current_test': ''}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/system-info', methods=['GET'])
def get_system_info():
    """الحصول على معلومات النظام"""
    return jsonify({
        'os': SYSTEM_INFO['os'],
        'platform': SYSTEM_INFO['platform'],
        'processor': SYSTEM_INFO['processor'],
        'architecture': SYSTEM_INFO['architecture'],
        'python_version': SYSTEM_INFO['python_version'],
        'timestamp': SYSTEM_INFO['timestamp']
    })

@app.route('/api/benchmarks/start', methods=['POST'])
def start_benchmarks():
    """بدء الاختبارات"""
    global benchmark_results, benchmark_status
    
    if benchmark_status['running']:
        return jsonify({'error': 'Benchmarks already running'}), 400
    
    def run_benchmarks():
        global benchmark_results, benchmark_status
        try:
            benchmark_status['running'] = True
            benchmark_results = {'system_info': SYSTEM_INFO, 'benchmarks': {}}
            
            # CPU & Memory
            benchmark_status['current_test'] = 'CPU & Memory'
            benchmark_status['progress'] = 0
            memory_bench = MemoryBenchmark()
            benchmark_results['benchmarks']['memory'] = memory_bench.run_all()
            benchmark_status['progress'] = 25
            
            # Process Management
            benchmark_status['current_test'] = 'Process Management'
            process_bench = ProcessManagementBenchmark()
            benchmark_results['benchmarks']['processes'] = process_bench.run_all()
            benchmark_status['progress'] = 50
            
            # Filesystem
            benchmark_status['current_test'] = 'Filesystem'
            fs_bench = FileSystemBenchmark()
            benchmark_results['benchmarks']['filesystem'] = fs_bench.run_all()
            benchmark_status['progress'] = 75
            
            # Security
            benchmark_status['current_test'] = 'Security'
            security_bench = SecurityBenchmark()
            benchmark_results['benchmarks']['security'] = security_bench.run_all()
            benchmark_status['progress'] = 100
            
            # Save results
            filename = f"{RESULTS_DIR}/benchmark_results_{platform.system()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f'Benchmarks completed successfully. Results saved to {filename}')
            benchmark_status['running'] = False
            
        except Exception as e:
            logger.error(f'Error running benchmarks: {e}')
            benchmark_status['running'] = False
            benchmark_status['current_test'] = f'Error: {str(e)}'
    
    thread = threading.Thread(target=run_benchmarks)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Benchmarks started'})

@app.route('/api/benchmarks/status', methods=['GET'])
def get_benchmark_status():
    """الحصول على حالة الاختبارات"""
    return jsonify(benchmark_status)

@app.route('/api/benchmarks/results', methods=['GET'])
def get_benchmark_results():
    """الحصول على نتائج الاختبارات"""
    if not benchmark_results:
        return jsonify({'error': 'No results available'}), 404
    return jsonify(benchmark_results)

@app.route('/api/benchmarks/export', methods=['GET'])
def export_results():
    """تصدير النتائج"""
    if not benchmark_results:
        return jsonify({'error': 'No results available'}), 404
    
    filename = f"benchmark_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    return jsonify(benchmark_results), 200, {'Content-Disposition': f'attachment;filename={filename}'}

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    app.run(debug=False, host='0.0.0.0', port=5000)
