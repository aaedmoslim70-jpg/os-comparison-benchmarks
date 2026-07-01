from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import platform
from datetime import datetime
import threading
import os
import sys

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Import benchmarks
try:
    from benchmarks.cpu_memory import MemoryBenchmark
    from benchmarks.filesystem import FileSystemBenchmark
    from benchmarks.process_management import ProcessManagementBenchmark
    from benchmarks.security import SecurityBenchmark
    from config import SYSTEM_INFO, RESULTS_DIR
    from utils.logger import setup_logger
    from utils.data_analyzer import generate_report
except Exception as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

logger = setup_logger()
benchmark_results = {}
benchmark_status = {'running': False, 'progress': 0, 'current_test': '', 'error': None}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/system-info', methods=['GET'])
def get_system_info():
    """الحصول على معلومات النظام"""
    try:
        return jsonify({
            'os': SYSTEM_INFO['os'],
            'platform': SYSTEM_INFO['platform'],
            'processor': SYSTEM_INFO['processor'],
            'architecture': SYSTEM_INFO['architecture'],
            'python_version': SYSTEM_INFO['python_version'],
            'timestamp': SYSTEM_INFO['timestamp']
        })
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({'error': str(e)}), 500

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
            benchmark_status['error'] = None
            benchmark_results = {'system_info': SYSTEM_INFO, 'benchmarks': {}}
            
            # CPU & Memory
            benchmark_status['current_test'] = 'CPU & Memory Benchmarks'
            benchmark_status['progress'] = 0
            memory_bench = MemoryBenchmark()
            benchmark_results['benchmarks']['memory'] = memory_bench.run_all()
            benchmark_status['progress'] = 25
            logger.info("Memory benchmarks completed")
            
            # Process Management
            benchmark_status['current_test'] = 'Process Management Benchmarks'
            process_bench = ProcessManagementBenchmark()
            benchmark_results['benchmarks']['processes'] = process_bench.run_all()
            benchmark_status['progress'] = 50
            logger.info("Process benchmarks completed")
            
            # Filesystem
            benchmark_status['current_test'] = 'Filesystem Benchmarks'
            fs_bench = FileSystemBenchmark()
            benchmark_results['benchmarks']['filesystem'] = fs_bench.run_all()
            benchmark_status['progress'] = 75
            logger.info("Filesystem benchmarks completed")
            
            # Security
            benchmark_status['current_test'] = 'Security Benchmarks'
            security_bench = SecurityBenchmark()
            benchmark_results['benchmarks']['security'] = security_bench.run_all()
            benchmark_status['progress'] = 100
            logger.info("Security benchmarks completed")
            
            # Save results
            os.makedirs(RESULTS_DIR, exist_ok=True)
            filename = f"{RESULTS_DIR}/benchmark_results_{platform.system()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(benchmark_results, f, indent=2, ensure_ascii=False)
            
            # Generate HTML report
            generate_report(benchmark_results)
            
            logger.info(f'Benchmarks completed successfully')
            benchmark_status['running'] = False
            benchmark_status['current_test'] = 'مكتمل ✅'
            
        except Exception as e:
            logger.error(f'Error running benchmarks: {e}')
            benchmark_status['running'] = False
            benchmark_status['error'] = str(e)
            benchmark_status['current_test'] = f'خطأ: {str(e)}'
    
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    logger.info('Starting OS Comparison Benchmarks Application')
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
