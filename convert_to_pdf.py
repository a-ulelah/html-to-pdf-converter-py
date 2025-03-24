import sys
import os
import traceback
import time
import re

# تأكد من أن المخرجات تظهر فوراً
sys.stdout.reconfigure(encoding='utf-8')

print("بدء تنفيذ برنامج التحويل...")
print(f"نسخة Python: {sys.version}")

# تسجيل المخرجات في ملف
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output.log')
print(f"سيتم تسجيل المخرجات في: {log_file}")

# إعادة توجيه المخرجات إلى ملف السجل والشاشة
class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger(log_file)

# وظيفة لإضافة CSS للطباعة إلى ملف HTML
def add_print_css(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # التحقق مما إذا كان CSS الطباعة موجود بالفعل
        if '@media print' in content:
            print("CSS الطباعة موجود بالفعل في الملف")
            return html_file_path
            
        # إضافة CSS للطباعة المحسن
        print_css = '''
        @media print {
            body {
                margin: 0;
                padding: 0;
                background-color: white !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                font-size: 11px !important;
            }
            .container {
                margin: 0 !important;
                padding: 10px !important;
                max-width: 100% !important;
                box-shadow: none !important;
                border-radius: 0 !important;
                transform: scale(0.95);
                transform-origin: top center;
            }
            .header {
                margin-bottom: 10px !important;
                padding-bottom: 10px !important;
            }
            .header h1 {
                font-size: 20px !important;
            }
            .header h2 {
                font-size: 14px !important;
            }
            .contact-item {
                font-size: 11px !important;
                margin: 2px 0 !important;
            }
            .section {
                page-break-inside: avoid;
                margin-top: 10px !important;
            }
            .section-title {
                font-size: 14px !important;
                margin-bottom: 5px !important;
                padding-bottom: 2px !important;
            }
            .summary {
                padding: 8px !important;
                margin-bottom: 10px !important;
                font-size: 11px !important;
            }
            .job, .education, .certificate {
                page-break-inside: avoid;
                margin-bottom: 8px !important;
                padding-bottom: 8px !important;
            }
            .job-title, .education-degree {
                font-size: 12px !important;
            }
            .job-period {
                font-size: 11px !important;
            }
            ul {
                margin: 4px 0 !important;
                padding-right: 15px !important;
                padding-left: 15px !important;
            }
            li {
                margin-bottom: 2px !important;
                font-size: 11px !important;
            }
            .skills-list {
                gap: 4px !important;
            }
            .skill-item {
                padding: 3px 8px !important;
                font-size: 10px !important;
                border-radius: 15px !important;
            }
            .skill-cat {
                margin-bottom: 8px !important;
            }
            .skill-cat-title {
                font-size: 12px !important;
                margin-bottom: 4px !important;
            }
            .certificates {
                gap: 5px !important;
            }
            .certificate {
                padding: 5px !important;
                margin-bottom: 5px !important;
                font-size: 11px !important;
            }
            .certificate-title {
                font-size: 11px !important;
            }
            .certificate-issuer, .certificate-date {
                font-size: 10px !important;
            }
            /* تحسينات خاصة للغة العربية */
            html[lang="ar"] .container {
                direction: rtl !important;
            }
            @page {
                size: A4;
                margin: 5mm !important;
            }
        }
        '''
        
        # إدراج CSS للطباعة قبل إغلاق وسم style
        modified_content = re.sub(r'(</style>)', print_css + r'\1', content)
        
        # إنشاء ملف HTML مؤقت جديد مع اسم فريد لتجنب مشاكل الأحرف الخاصة
        import uuid
        temp_html_path = os.path.join(os.path.dirname(html_file_path), f"temp_{uuid.uuid4().hex}.html")
        with open(temp_html_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
            
        print(f"تم إضافة CSS للطباعة إلى: {temp_html_path}")
        
        # التأكد من أن الملف المؤقت تم إنشاؤه بنجاح
        if not os.path.exists(temp_html_path):
            print(f"تحذير: فشل إنشاء الملف المؤقت: {temp_html_path}")
            return html_file_path
            
        return temp_html_path
        
    except Exception as e:
        print(f"خطأ أثناء إضافة CSS للطباعة: {e}")
        return html_file_path

# طباعة معلومات تشخيصية عن الملفات في المجلد الحالي
print("الملفات الموجودة في المجلد:")
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"المجلد الحالي: {current_dir}")
for file in os.listdir(current_dir):
    file_path = os.path.join(current_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"- {file} (الحجم: {file_size} بايت)")
    if file.endswith('.html'):
        print(f"  تم العثور على ملف HTML: {file}")

# تحديد مسارات الملفات بشكل مطلق
current_dir = os.path.dirname(os.path.abspath(__file__))

# البحث عن ملف السيرة الذاتية العربية
html_file = None
for file in os.listdir(current_dir):
    # تجاهل الأحرف الخاصة في بداية اسم الملف
    clean_filename = file.lstrip('\u200f\u200e')
    if 'arabic' in clean_filename.lower() and clean_filename.endswith('.html'):
        # إنشاء نسخة من الملف بدون أحرف خاصة في بداية الاسم
        if file != clean_filename + '.html':
            clean_file_path = os.path.join(current_dir, 'arabiccv_clean.html')
            try:
                with open(os.path.join(current_dir, file), 'r', encoding='utf-8') as src_file:
                    content = src_file.read()
                with open(clean_file_path, 'w', encoding='utf-8') as dest_file:
                    dest_file.write(content)
                html_file = clean_file_path
                print(f"تم إنشاء نسخة نظيفة من الملف: {html_file}")
            except Exception as e:
                print(f"خطأ أثناء إنشاء نسخة نظيفة من الملف: {e}")
                html_file = os.path.join(current_dir, file)
        else:
            html_file = os.path.join(current_dir, file)
        print(f"تم العثور على ملف HTML: {html_file}")
        break

if html_file is None or not os.path.exists(html_file):
    print("لم يتم العثور على ملف HTML العربي!")
    # محاولة استخدام ملف السيرة الذاتية الإنجليزية كبديل
    for file in os.listdir(current_dir):
        if 'english' in file.lower() and file.endswith('.html'):
            html_file = os.path.join(current_dir, file)
            print(f"تم العثور على ملف HTML الإنجليزي كبديل: {html_file}")
            break

if html_file is None or not os.path.exists(html_file):
    print("لم يتم العثور على أي ملف HTML!")
    sys.exit(1)

pdf_file = os.path.join(current_dir, 'cv.pdf')
print(f"مسار ملف HTML: {html_file}")
print(f"مسار ملف PDF: {pdf_file}")

try:
    # محاولة استخدام wkhtmltopdf مباشرة
    import subprocess
    wkhtmltopdf_installer = os.path.join(current_dir, 'wkhtmltopdf-installer.exe')
    if os.path.exists(wkhtmltopdf_installer):
        print(f"تم العثور على wkhtmltopdf-installer.exe في: {wkhtmltopdf_installer}")
        print("محاولة تثبيت وتنفيذ wkhtmltopdf...")
        try:
            # تثبيت wkhtmltopdf
            print("تثبيت wkhtmltopdf...")
            subprocess.run([wkhtmltopdf_installer, '/S'], check=True)
            print("تم تثبيت wkhtmltopdf بنجاح")
            
            # إضافة CSS للطباعة إلى ملف HTML
            temp_html_file = add_print_css(html_file)
            
            # استخدام wkhtmltopdf مباشرة مع خيارات تنسيق محسنة
            wkhtmltopdf_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
            if os.path.exists(wkhtmltopdf_path):
                # إضافة خيارات تنسيق محسنة لضمان ظهور السيرة الذاتية على صفحة واحدة
                cmd = [
                    wkhtmltopdf_path,
                    "--page-size", "A4",
                    "--margin-top", "5mm",
                    "--margin-bottom", "5mm",
                    "--margin-left", "5mm",
                    "--margin-right", "5mm",
                    "--encoding", "UTF-8",
                    "--enable-local-file-access",
                    "--print-media-type",
                    "--disable-smart-shrinking",
                    "--dpi", "300",
                    "--zoom", "0.85",
                    "--image-dpi", "300",
                    "--image-quality", "100",
                    "--no-background",
                    temp_html_file, pdf_file
                ]
                print(f"تنفيذ الأمر: {' '.join(cmd)}")
                subprocess.run(cmd, check=True)
                print(f"تم تحويل الملف بنجاح إلى: {pdf_file}")
                
                # حذف الملف المؤقت
                if temp_html_file != html_file and os.path.exists(temp_html_file):
                    os.remove(temp_html_file)
                    print(f"تم حذف الملف المؤقت: {temp_html_file}")
                    
                sys.exit(0)
            else:
                print(f"لم يتم العثور على wkhtmltopdf في المسار المتوقع: {wkhtmltopdf_path}")
        except Exception as direct_error:
            print(f"فشل تثبيت أو استخدام wkhtmltopdf مباشرة: {direct_error}")
    else:
        print("لم يتم العثور على wkhtmltopdf-installer.exe")
        
    # محاولة استخدام Chrome أو Edge
    try:
        import subprocess
        print("محاولة استخدام Chrome لتحويل الملف...")
        
        if html_file is None or not os.path.exists(html_file):
            print("لم يتم العثور على ملف HTML!")
            sys.exit(1)
            
        # إضافة CSS للطباعة إلى ملف HTML
        temp_html_file = add_print_css(html_file)
        
        # استخدام Chrome في وضع headless لتحويل HTML إلى PDF مع خيارات محسنة
        # استخدام مسار مطلق للملف المؤقت والملف الناتج
        abs_temp_html = os.path.abspath(temp_html_file)
        abs_pdf_file = os.path.abspath(pdf_file)
        
        # تحويل المسارات إلى تنسيق URL لتجنب مشاكل الأحرف الخاصة
        path_for_url = abs_temp_html.replace('\\', '/')
        file_url = f"file:///{path_for_url}"
        
        # التأكد من عدم وجود ملف PDF قديم قبل إنشاء ملف جديد
        if os.path.exists(pdf_file):
            try:
                os.remove(pdf_file)
                print(f"تم حذف ملف PDF القديم: {pdf_file}")
            except Exception as e:
                print(f"تحذير: لا يمكن حذف ملف PDF القديم: {e}")
        
        cmd = [
            'powershell', '-Command',
            f'Start-Process "chrome" -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf=\"{abs_pdf_file}\"", "--print-to-pdf-no-header", "--default-page-size=A4", "--hide-scrollbars", "\"{file_url}\"" -Wait -NoNewWindow'
        ]
        print(f"تنفيذ الأمر: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
        # انتظار لحظة للتأكد من اكتمال عملية إنشاء الملف
        time.sleep(2)
        # التحقق من صحة ملف PDF
        retry_count = 0
        max_retries = 3
        pdf_valid = False
        
        while retry_count < max_retries and not pdf_valid:
            if os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 1000:  # التأكد من أن الملف موجود وحجمه معقول
                print(f"تم تحويل الملف باستخدام Chrome إلى: {pdf_file}")
                print(f"حجم ملف PDF: {os.path.getsize(pdf_file)} بايت")
                
                # محاولة فتح الملف للتأكد من صحته
                try:
                    # فتح الملف للقراءة فقط للتحقق من إمكانية الوصول إليه
                    with open(pdf_file, 'rb') as test_file:
                        # قراءة أول 100 بايت للتأكد من أنه ملف PDF صالح
                        header = test_file.read(100)
                        if b'%PDF-' in header:  # التحقق من وجود توقيع PDF
                            print("تم التحقق من صحة ملف PDF بنجاح")
                            pdf_valid = True
                            break
                        else:
                            print("تحذير: الملف لا يبدو أنه PDF صالح، محاولة مرة أخرى...")
                except Exception as e:
                    print(f"تحذير: لا يمكن التحقق من صحة ملف PDF: {e}")
            else:
                print(f"تحذير: ملف PDF غير موجود أو حجمه صغير جدًا: {pdf_file}")
            
            # إذا لم ينجح، حاول مرة أخرى
            if not pdf_valid:
                retry_count += 1
                if retry_count < max_retries:
                    print(f"محاولة {retry_count + 1} من {max_retries} لإنشاء ملف PDF...")
                    time.sleep(2)  # انتظار قبل المحاولة مرة أخرى
                    # محاولة إنشاء الملف مرة أخرى
                    subprocess.run(cmd, check=True)
                else:
                    print("فشلت جميع محاولات إنشاء ملف PDF صالح")
        
        if pdf_valid:
            print(f"تم تحويل الملف بنجاح باستخدام Chrome إلى: {pdf_file}")
        else:
            print(f"تحذير: لم يتم إنشاء ملف PDF صالح بعد {max_retries} محاولات")
        
        # حذف الملف المؤقت
        if temp_html_file != html_file and os.path.exists(temp_html_file):
            os.remove(temp_html_file)
            print(f"تم حذف الملف المؤقت: {temp_html_file}")
    except Exception as chrome_error:
        print(f"فشلت محاولة التحويل باستخدام Chrome: {chrome_error}")
        
        # محاولة أخيرة باستخدام Microsoft Edge
        try:
            print("محاولة استخدام Microsoft Edge لتحويل الملف...")
            # إضافة CSS للطباعة إلى ملف HTML إذا لم يتم ذلك بالفعل
            if 'temp_html_file' not in locals():
                temp_html_file = add_print_css(html_file)
                
            edge_cmd = [
                'powershell', '-Command',
                f'Start-Process "msedge" -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf={pdf_file}", "--print-to-pdf-no-header", "--default-page-size=A4", "--hide-scrollbars", "{temp_html_file}"'
            ]
            print(f"تنفيذ الأمر: {' '.join(edge_cmd)}")
            subprocess.run(edge_cmd, check=True)
            print(f"تم تحويل الملف بنجاح باستخدام Microsoft Edge إلى: {pdf_file}")
            
            # حذف الملف المؤقت
            if temp_html_file != html_file and os.path.exists(temp_html_file):
                os.remove(temp_html_file)
                print(f"تم حذف الملف المؤقت: {temp_html_file}")
        except Exception as edge_error:
            print(f"فشلت جميع محاولات التحويل!")
            print(f"خطأ Edge: {edge_error}")
            sys.exit(1)
    
except ImportError:
    # إذا لم تكن مكتبة weasyprint مثبتة، نحاول استخدام pdfkit
    try:
        import pdfkit
        print("تم استيراد مكتبة pdfkit بنجاح")
        
        # تحديد مسارات الملفات
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file = None
        
        # محاولة العثور على ملف السيرة الذاتية العربية
        for file in os.listdir(current_dir):
            if 'arabic' in file.lower() and file.endswith('.html'):
                html_file = os.path.join(current_dir, file)
                print(f"تم العثور على ملف HTML: {html_file}")
                break
                
        if html_file is None or not os.path.exists(html_file):
            print("لم يتم العثور على ملف HTML!")
            sys.exit(1)
            
        pdf_file = os.path.join(current_dir, 'arabic_cv.pdf')
        
        print(f"مسار ملف HTML: {html_file}")
        print(f"مسار ملف PDF: {pdf_file}")
        
        # التحقق من وجود wkhtmltopdf
        wkhtmltopdf_installer = os.path.join(current_dir, 'wkhtmltopdf-installer.exe')
        if os.path.exists(wkhtmltopdf_installer):
            print(f"تم العثور على wkhtmltopdf-installer.exe في: {wkhtmltopdf_installer}")
            print("محاولة تنفيذ wkhtmltopdf مباشرة...")
            try:
                import subprocess
                # محاولة استخدام wkhtmltopdf مباشرة
                wkhtmltopdf_path = os.path.join(current_dir, 'wkhtmltopdf.exe')
                if not os.path.exists(wkhtmltopdf_path):
                    print("تثبيت wkhtmltopdf...")
                    subprocess.run([wkhtmltopdf_installer, '/S'], check=True)
                    print("تم تثبيت wkhtmltopdf بنجاح")
                
                # استخدام wkhtmltopdf مباشرة
                cmd = [wkhtmltopdf_path, html_file, pdf_file]
                print(f"تنفيذ الأمر: {' '.join(cmd)}")
                subprocess.run(cmd, check=True)
                print(f"تم تحويل الملف بنجاح إلى: {pdf_file}")
                sys.exit(0)
            except Exception as direct_error:
                print(f"فشل استخدام wkhtmltopdf مباشرة: {direct_error}")
        
        # التحويل من HTML إلى PDF باستخدام pdfkit
        try:
            pdfkit.from_file(html_file, pdf_file)
            print(f"تم تحويل الملف بنجاح إلى: {pdf_file}")
        except Exception as pdfkit_error:
            print(f"فشل التحويل باستخدام pdfkit: {pdfkit_error}")
            raise
        
    except ImportError:
        print("يرجى تثبيت إحدى المكتبات: weasyprint أو pdfkit")
        print("يمكنك تثبيت weasyprint باستخدام: pip install weasyprint")
        print("أو تثبيت pdfkit باستخدام: pip install pdfkit")
        sys.exit(1)
    except Exception as e:
        print(f"حدث خطأ أثناء التحويل باستخدام pdfkit: {e}")
        print("قد تحتاج إلى تثبيت wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        
        # محاولة استخدام طريقة بديلة باستخدام Chrome
        try:
            import subprocess
            print("محاولة استخدام Chrome لتحويل الملف...")
            
            if html_file is None or not os.path.exists(html_file):
                print("لم يتم العثور على ملف HTML!")
                sys.exit(1)
                
            # استخدام Chrome في وضع headless لتحويل HTML إلى PDF
            cmd = [
                'powershell', '-Command',
                f'Start-Process "chrome" -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf={pdf_file}", "{html_file}"'
            ]
            print(f"تنفيذ الأمر: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"تم تحويل الملف بنجاح باستخدام Chrome إلى: {pdf_file}")
        except Exception as chrome_error:
            print(f"فشلت محاولة التحويل باستخدام Chrome: {chrome_error}")
            
            # محاولة أخيرة باستخدام Microsoft Edge
            try:
                print("محاولة استخدام Microsoft Edge لتحويل الملف...")
                edge_cmd = [
                    'powershell', '-Command',
                    f'Start-Process "msedge" -ArgumentList "--headless", "--disable-gpu", "--print-to-pdf={pdf_file}", "{html_file}"'
                ]
                print(f"تنفيذ الأمر: {' '.join(edge_cmd)}")
                subprocess.run(edge_cmd, check=True)
                print(f"تم تحويل الملف بنجاح باستخدام Microsoft Edge إلى: {pdf_file}")
            except Exception as edge_error:
                print(f"فشلت جميع محاولات التحويل!")
                print(f"خطأ Edge: {edge_error}")
                sys.exit(1)
except Exception as e:
    print(f"حدث خطأ أثناء التحويل: {e}")
    print("تفاصيل الخطأ:")
    traceback.print_exc()
    sys.exit(1)