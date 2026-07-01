import json
import platform
from datetime import datetime
from config import SYSTEM_INFO, RESULTS_DIR
from benchmarks.cpu_memory import MemoryBenchmark
from benchmarks.process_management import ProcessManagementBenchmark
from benchmarks.filesystem import FileSystemBenchmark
from benchmarks.security import SecurityBenchmark
from utils.logger import setup_logger
from utils.data_analyzer import generate_report

# إعداد السجل
logger = setup_logger()

class ComparisonBenchmark:
    def __init__(self):
        self.all_results = {
            'system_info': SYSTEM_INFO,
            'benchmarks': {}
        }
    
    def run_all_benchmarks(self):
        """تشغيل جميع الاختبارات"""
        print("\n" + "="*60)
        print("🚀 برنامج مقارنة أنظمة التشغيل الحديثة")
        print("="*60)
        print(f"🖥️  النظام: {SYSTEM_INFO['os']}")
        print(f"📊 المنصة: {SYSTEM_INFO['platform']}")
        print(f"⚙️  المعالج: {SYSTEM_INFO['processor']}")
        print("="*60)
        
        try:
            # قياسات الذاكرة والمعالج
            print("\n\n[1/4] 🧠 قياسات الذاكرة والمعالج...")
            memory_bench = MemoryBenchmark()
            self.all_results['benchmarks']['memory'] = memory_bench.run_all()
            
            # قياسات إدارة العمليات
            print("\n\n[2/4] ⚙️  قياسات إدارة العمليات...")
            process_bench = ProcessManagementBenchmark()
            self.all_results['benchmarks']['processes'] = process_bench.run_all()
            
            # قياسات نظام الملفات
            print("\n\n[3/4] 📁 قياسات نظام الملفات...")
            fs_bench = FileSystemBenchmark()
            self.all_results['benchmarks']['filesystem'] = fs_bench.run_all()
            
            # قياسات الأمان
            print("\n\n[4/4] 🔒 قياسات الأمان...")
            security_bench = SecurityBenchmark()
            self.all_results['benchmarks']['security'] = security_bench.run_all()
            
            # حفظ النتائج
            self._save_results()
            self._generate_report()
            
            print("\n" + "="*60)
            print("✅ اكتملت جميع القياسات بنجاح!")
            print("="*60)
            
        except Exception as e:
            logger.error(f"خطأ أثناء تنفيذ القياسات: {e}")
            print(f"❌ خطأ: {e}")
    
    def _save_results(self):
        """حفظ النتائج في ملف JSON"""
        filename = f"{RESULTS_DIR}/benchmark_results_{platform.system()}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 تم حفظ النتائج في: {filename}")
    
    def _generate_report(self):
        """توليد تقرير HTML"""
        generate_report(self.all_results)

if __name__ == "__main__":
    benchmark = ComparisonBenchmark()
    benchmark.run_all_benchmarks()