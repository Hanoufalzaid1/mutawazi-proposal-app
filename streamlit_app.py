
import streamlit as st
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import tempfile
import base64

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني ومالي تلقائيًا.")

logo_center_path = "logo_center.png"
logo_corner_path = "logo_corner.png"

uploaded_rfp = st.file_uploader("📎 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع", "مشروع تطوير وتأسيس تقارير هيئة التأمين")
client_name = st.text_input("👤 اسم الجهة", "هيئة التأمين")

if st.button("🚀 توليد العرض الفني"):
    if not uploaded_rfp:
        st.warning("يرجى رفع كراسة الشروط أولاً.")
    else:
        doc = Document()

        # الهيدر بالشعار
        table = doc.add_table(rows=1, cols=2)
        cells = table.rows[0].cells
        try:
            run = cells[0].paragraphs[0].add_run()
            run.add_picture(logo_corner_path, width=Inches(1))
        except:
            pass
        cells[0].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        cells[1].text = ""
        cells[1].paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        doc.add_paragraph("\n")

        # شعار الشركة في المنتصف
        try:
            p = doc.add_paragraph()
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            r = p.add_run()
            r.add_picture(logo_center_path, width=Inches(2))
        except:
            pass

        # اسم المشروع
        title_p = doc.add_paragraph(project_name)
        title_p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        title_p.runs[0].font.size = Pt(16)
        title_p.runs[0].bold = True

        doc.add_paragraph("\n\n")

        sections = {
            "مقدمة": f"تتشرف شركة متوازي بتقديم هذا العرض الفني لمنافسة {project_name} لصالح {client_name}.",
            "فهم المشروع": "يهدف المشروع إلى تأسيس إطار تقارير شامل للجهة يشمل إعداد ونشر تقارير مطبوعة ورقمية.",
            "نطاق العمل": "يشمل نطاق العمل تحليل الاحتياج، تصميم نماذج التقارير، إعداد الأدلة التشغيلية، وتدريب منسوبي الجهة.",
            "المنهجية": "سنتبع منهجية متكاملة تبدأ بتحليل الفجوة وتنتهي بتسليم الحلول التشغيلية الجاهزة باستخدام أحدث تقنيات BI.",
            "الجدول الزمني": "مدة تنفيذ المشروع 4 أشهر تبدأ من توقيع العقد، مقسّمة على 4 مراحل رئيسية.",
            "الفريق التنفيذي": "يتكون الفريق من مدير مشروع، خبير بيانات، محلل أعمال، ومطور حلول ذكاء أعمال.",
            "الخبرات السابقة": "نفذت الشركة مشاريع مشابهة مع جهات حكومية في مجالات إعداد التقارير وتحسين اتخاذ القرار.",
            "خطة إدارة الجودة": "سنقوم بتطبيق معايير إدارة الجودة ISO 9001 مع مراجعات أسبوعية وتوثيق كل المخرجات.",
            "خطة الأمن السيبراني": "الالتزام بتطبيق ضوابط الهيئة الوطنية للأمن السيبراني NCA.",
            "الامتثال للكراسة": "تمت مراجعة جميع المتطلبات والتأكد من توافق العرض الفني مع كراسة الشروط."
        }

        for section, content in sections.items():
            doc.add_heading(section, level=2)
            doc.add_paragraph(content)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            with open(tmp.name, "rb") as f:
                st.download_button("⬇️ تحميل العرض الفني", f, file_name="العرض_الفني.docx")
    