# 🖥️ OS Comparison Benchmarks - نظام مقارنة أنظمة التشغيل

## مقدمة
أداة شاملة وديناميكية لقياس وتقييم أداء أنظمة التشغيل المختلفة (Windows, Linux, macOS) مع واجهة ويب تفاعلية.

## الميزات الرئيسية ✨

- **واجهة ويب ديناميكية**: تحديث فوري للنتائج أثناء الاختبار
- **قياسات شاملة**:
  - 🧠 أداء المعالج والذاكرة
  - ⚙️ إدارة العمليات والخيوط
  - 📁 أداء نظام الملفات
  - 🔒 الأمان والتشفير
- **تقارير قابلة للتصدير**: JSON و HTML
- **متعدد المنصات**: Windows, Linux, macOS
- **واجهة عربية**: دعم كامل للعربية (RTL)
- **سريع جداً**: اختبارات محسّنة للأداء

## المتطلبات 📋

```bash
Python 3.8+
Flask 2.3.0+
Flask-CORS 4.0.0+
psutil 5.9.5+
NumPy 1.24.3+
```

## التثبيت 🚀

### 1. استنسخ المستودع
```bash
git clone https://github.com/aaedmoslim70-jpg/os-comparison-benchmarks.git
cd os-comparison-benchmarks
```

### 2. أنشئ بيئة افتراضية
```bash
# على Linux/macOS
python3 -m venv venv
source venv/bin/activate

# على Windows
python -m venv venv
venv\Scripts\activate
```

### 3. ثبت المتطلبات
```bash
pip install -r requirements.txt
```

## الاستخدام 🎯

### تشغيل الخادم
```bash
python app.py
```

### فتح الواجهة
افتح المتصفح على `http://localhost:5000`

### خطوات الاستخدام
1. سيتم عرض معلومات نظامك تلقائياً
2. اضغط "بدء الاختبارات"
3. تابع التقدم في الوقت الفعلي
4. اعرض النتائج المفصلة
5. حمل النتائج بصيغة JSON

## هيكل المشروع 📦

```
os-comparison-benchmarks/
├── app.py                    # خادم Flask الرئيسي
├── config.py                 # الإعدادات
├── requirements.txt          # المتطلبات
├── README.md                 # التوثيق
├── .gitignore               # ملف التجاهل
├── benchmarks/
│   ├── __init__.py
│   ├── cpu_memory.py         # قياسات المعالج والذاكرة
│   ├── filesystem.py         # قياسات نظام الملفات
│   ├── process_management.py # إدارة العمليات
│   └── security.py           # الأمان والتشفير
├── utils/
│   ├── __init__.py
│   ├── logger.py             # نظام السجلات
│   └── data_analyzer.py      # تحليل البيانات
├── templates/
│   └── index.html            # الواجهة الرئيسية
├── static/
│   ├── css/
│   │   └── style.css         # الأنماط
│   └── js/
│       └── script.js         # السكريبتات
├── logs/                     # السجلات
└── results/                  # نتائج الاختبارات
```

## مكونات القياس 📊

### المعالج والذاكرة 🧠
- ⚡ أداء CPU في العمليات الحسابية
- 💾 سرعة تخصيص الذاكرة
- 📈 استخدام الذاكرة المتوسط والأقصى

### إدارة العمليات ⚙️
- ⏱️ سرعة إنشاء العمليات
- 🧵 سرعة إنشاء الخيوط
- 🔄 تبديل السياق

### نظام الملفات 📁
- 📝 سرعة إنشاء الملفات
- ✍️ سرعة الكتابة (MB/s)
- 📂 عمليات المجلدات

### الأمان والتشفير 🔒
- 🔐 سرعة Hashing (MD5, SHA256)
- 🔑 عمليات التشفير (ops/sec)
- 🛡️ فحص الميزات الأمنية

## API Endpoints 🔌

```
GET  /api/system-info
POST /api/benchmarks/start
GET  /api/benchmarks/status
GET  /api/benchmarks/results
GET  /api/benchmarks/export
```

## الأمثلة 💡

### الحصول على معلومات النظام
```bash
curl http://localhost:5000/api/system-info
```

### بدء الاختبارات
```bash
curl -X POST http://localhost:5000/api/benchmarks/start
```

### الحصول على الحالة
```bash
curl http://localhost:5000/api/benchmarks/status
```

### الحصول على النتائج
```bash
curl http://localhost:5000/api/benchmarks/results
```

## النتائج 📈

يتم حفظ النتائج في:
- `results/benchmark_results_[OS]_[DATE].json` - تنسيق JSON
- `results/report_[OS]_[DATE].html` - تقرير HTML
- `logs/benchmark_[DATE].log` - السجلات

## الأداء ⚡

- وقت التشغيل: **~30 ثانية** (يمكن تقليله)
- حجم النتائج: **صغير جداً** (أقل من 1 MB)
- استهلاك الذاكرة: **منخفض جداً** (< 50 MB)

## التطوير 🔧

### إضافة معيار جديد

1. أنشئ فئة جديدة في `benchmarks/`:
```python
class NewBenchmark:
    def run_all(self):
        # تطبيق المنطق
        return self.results
```

2. أضفه في `app.py`:
```python
new_bench = NewBenchmark()
benchmark_results['benchmarks']['new'] = new_bench.run_all()
```

3. أضفه في `script.js`:
```javascript
function displayNewResults(data) {
    // عرض النتائج
}
```

## استكشاف الأخطاء 🐛

### الخادم لا يشتغل
```bash
# تحقق من المنفذ
netstat -tulpn | grep 5000

# استخدم منفذ مختلف
PORT=8000 python app.py
```

### خطأ في المتطلبات
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### النتائج لا تظهر
- تحقق من `logs/` للأخطاء
- افتح Developer Tools (F12)
- تحقق من Network tab

## الترخيص 📄
MIT License

## المساهمة 🤝
نرحب بالمساهمات! يرجى فتح Issue أو Pull Request.

## الدعم 💬
للأسئلة والاستفسارات، يرجى فتح Issue على GitHub.

---

**صنع بـ ❤️ لمقارنة أداء أنظمة التشغيل**
