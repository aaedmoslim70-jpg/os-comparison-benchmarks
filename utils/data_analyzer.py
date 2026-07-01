import json
import platform
from datetime import datetime

def generate_report(results):
    """توليد تقرير مقارنة شامل"""
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>تقرير مقارنة أنظمة التشغيل</title>
            <style>
                body {{ font-family: Arial, sans-serif; direction: rtl; background: #f5f5f5; }}
                .header {{ background: #667eea; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px; padding: 15px; border: 1px solid #ddd; background: white; border-radius: 8px; }}
                .metric {{ padding: 10px; background: #ecf0f1; margin: 5px 0; border-radius: 4px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ border: 1px solid #ddd; padding: 10px; text-align: right; }}
                th {{ background: #667eea; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 تقرير مقارنة أنظمة التشغيل</h1>
                <p>التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>🖥️ معلومات النظام</h2>
                <div class="metric"><strong>النظام:</strong> {results.get('system_info', {}).get('os', 'غير متوفر')}</div>
                <div class="metric"><strong>المعالج:</strong> {results.get('system_info', {}).get('processor', 'غير متوفر')}</div>
                <div class="metric"><strong>الإصدار:</strong> {results.get('system_info', {}).get('platform', 'غير متوفر')}</div>
                <div class="metric"><strong>البنية:</strong> {results.get('system_info', {}).get('architecture', 'غير متوفر')}</div>
            </div>
            
            <div class="section">
                <h2>📈 نتائج القياسات</h2>
                <pre style="background: #f9f9f9; padding: 15px; border-radius: 4px; overflow-x: auto;">{json.dumps(results.get('benchmarks', {}), indent=2, ensure_ascii=False)}</pre>
            </div>
        </body>
        </html>
        """
        
        os.makedirs('results', exist_ok=True)
        filename = f"results/report_{platform.system()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ تم توليد التقرير: {filename}")
    except Exception as e:
        print(f"❌ خطأ في توليد التقرير: {e}")

import os
