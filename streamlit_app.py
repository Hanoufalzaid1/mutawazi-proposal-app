import streamlit as st
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx2pdf import convert
import os
import uuid

# إعداد الصفحة
st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني ومالي تلقائيًا")

# إدخال البيانات
uploaded_file = st.file_uploader("📤 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع")
client_name = st.text_input("🏛️ اسم الجهة")
gov_logo = st.file_uploader("🎖️ شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

# شعارات الشركة
mutawazi_logo_center = "mutawazi_center.png"  # يجب رفع الصورة في مجلد العمل
mutawazi_logo_corner = "mutawazi_icon.png"

if st.button("🚀 توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        # إنشاء الملف
        doc = Document()

        # الغلاف
        section = doc.sections[0]
        header = section.header
        if gov_logo:
            header_paragraph = header.paragraphs[0]
            run = header_paragraph.add_run()
            run.add_picture(gov_logo, width=Inches(1.2))

        # وسط الصفحة
        doc.add_paragraph().add_run().add_picture(mutawazi_logo_center, width=Inches(2))
        doc.add_paragraph(project_name).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.add_paragraph(client_name).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.add_paragraph("شركة متوازي للاستشارات الإدارية").alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.add_page_break()

        # المحتوى التجريبي (25 صفحة)
        for i in range(1, 26):
            p = doc.add_paragraph(f"📄 الصفحة {i}")
            p.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
            doc.add_paragraph("هذا مثال على محتوى عرض فني مفصل وموسع...")
            doc.add_page_break()

        # حفظ الملفات المؤقتة
        file_id = str(uuid.uuid4())
        word_path = f"عرض_فني_{file_id}.docx"
        pdf_path = f"عرض_فني_{file_id}.pdf"

        doc.save(word_path)

        try:
            convert(word_path, pdf_path)
        except:
            st.warning("⚠️ تعذر تحويل الملف إلى PDF - تأكد من دعم النظام لـ Word.")

        # تحميل
        with open(word_path, "rb") as f:
            st.download_button("📥 تحميل العرض الفني (Word)", f, file_name="عرض_فني.docx")

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button("📥 تحميل العرض الفني (PDF)", f, file_name="عرض_فني.pdf")

        # تنظيف
        os.remove(word_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        st.success("✅ تم توليد العرض الفني بنجاح!")

    else:
        st.error("يرجى رفع كراسة الشروط وإدخال اسم المشروع والجهة.")
