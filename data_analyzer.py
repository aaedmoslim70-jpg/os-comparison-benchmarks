import json
import platform
from datetime import datetime

def generate_report(results):
    """توليد تقرير مقارنة شامل"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تقرير مقارنة أنظمة التشغيل</title>
        <style>
            body {{ font-family: Arial, sans-serif; direction: rtl; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; }}
            .section {{ margin: 20px; padding: 15px; border: 1px solid #ddd; }}
            .metric {{ padding: 10px; background: #ecf0f1; margin: 5px 0; }}
            .good {{ color: green; }}
            .warning {{ color: orange; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: right; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 تقرير مقارنة أنظمة التشغيل</h1>
            <p>التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>🖥️  معلومات النظام</h2>
            <div class="metric"><strong>النظام:</strong> {results['system_info']['os']}</div>
            <div class="metric"><strong>المعالج:</strong> {results['system_info']['processor']}</div>
            <div class="metric"><strong>الإصدار:</strong> {results['system_info']['platform']}</div>
        </div>
        
        <div class="section">
            <h2>📈 نتائج القياسات</h2>
            <pre>{json.dumps(results['benchmarks'], indent=2, ensure_ascii=False)}</pre>
        </div>
    </body>
    </html>
    """
    
    filename = f"results/report_{platform.system()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📄 تم توليد التقرير: {filename}")