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
- **تقارير قابلة للتصدير**: JSON وHTML
- **متعدد المنصات**: Windows, Linux, macOS
- **واجهة عربية كاملة**: دعم كامل للعربية (RTL)

## المتطلبات 📋

```bash
Python 3.8+
Flask 2.3.0+
psutil 5.9.5+
NumPy 1.24.3+
```

## التثبيت 🚀

1. استنسخ المستودع:
```bash
git clone https://github.com/aaedmoslim70-jpg/os-comparison-benchmarks.git
cd os-comparison-benchmarks
```

2. أنشئ بيئة افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Linux/macOS
venv\Scripts\activate     # على Windows
```

3. ثبت المتطلبات:
```bash
pip install -r requirements.txt
```

## الاستخدام 🎯

### تشغيل الخادم:
```bash
python app.py
```

ثم افتح المتصفح على `http://localhost:5000`

### واجهة المستخدم:
1. سيتم عرض معلومات نظامك تلقائياً
2. اضغط "بدء الاختبارات"
3. تابع التقدم في الوقت الفعلي
4. اعرض النتائج المفصلة
5. حمل النتائج بصيغة JSON

## مكونات المشروع 📦

### Backend (Python)
- `app.py` - خادم Flask الرئيسي
- `config.py` - الإعدادات والمتغيرات
- `benchmarks/cpu_memory.py` - قياسات المعالج والذاكرة
- `benchmarks/process_management.py` - إدارة العمليات
- `benchmarks/filesystem.py` - نظام الملفات
- `benchmarks/security.py` - الأمان والتشفير
- `utils/logger.py` - نظام السجلات
- `utils/data_analyzer.py` - تحليل البيانات

### Frontend
- `templates/index.html` - الواجهة الرئيسية
- `static/css/style.css` - أنماط التصميم
- `static/js/script.js` - السكريبتات التفاعلية

## النتائج 📊

يتم حفظ النتائج في مجلد `results/` بصيغ متعددة:
- JSON للتحليل البرمجي
- HTML للعرض المباشر

## معايير الأداء المقاسة 📈

### المعالج والذاكرة
- سرعة تخصيص الذاكرة
- سرعة الوصول المتسلسل والعشوائي
- أداء CPU في العمليات الحسابية
- استخدام الذاكرة

### إدارة العمليات
- سرعة إنشاء العمليات
- تبديل السياق (Context Switching)
- إنشاء الخيوط

### نظام الملفات
- سرعة إنشاء الملفات
- سرعة قراءة الملفات
- إنتاجية الكتابة
- عمليات المجلدات

### الأمان
- سرعة Hashing (MD5, SHA256, SHA512)
- عمليات التشفير
- فحص الميزات الأمنية

## API Endpoints 🔌

```
GET  /api/system-info           - معلومات النظام
POST /api/benchmarks/start      - بدء الاختبارات
GET  /api/benchmarks/status     - حالة الاختبارات
GET  /api/benchmarks/results    - نتائج الاختبارات
GET  /api/benchmarks/export     - تصدير النتائج
```

## أمثلة الاستخدام 💡

### البدء
```bash
# شغل الخادم
python app.py

# افتح المتصفح
# http://localhost:5000
```

### الحصول على معلومات النظام
```bash
curl http://localhost:5000/api/system-info
```

### بدء الاختبارات
```bash
curl -X POST http://localhost:5000/api/benchmarks/start
```

## الترخيص 📜
MIT License

## المساهمة 🤝
نرحب بالمساهمات! يرجى فتح Issue أو Pull Request.

## الدعم 💬
للأسئلة والاستفسارات، يرجى فتح Issue على GitHub.

---

**صنع بـ ❤️ لمقارنة أداء أنظمة التشغيل**
