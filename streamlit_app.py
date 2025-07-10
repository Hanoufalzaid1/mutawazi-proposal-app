import streamlit as st
from docx import Document
import base64
import os

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني تلقائيًا")

uploaded_file = st.file_uploader("📤 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع")
client_name = st.text_input("🏛️ اسم الجهة")
gov_logo = st.file_uploader("🎖️ شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

if st.button("🚀 توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        # Placeholder: إنشاء ملف Word وهمي
        doc = Document()
        doc.add_heading(f"العرض الفني لمشروع {project_name}", level=1)
        doc.add_paragraph(f"الجهة: {client_name}")
        doc.add_paragraph("هذا نص توضيحي لمحتوى العرض الفني.")

        word_path = "عرض_فني.docx"
        doc.save(word_path)

        with open(word_path, "rb") as f:
            st.download_button("📥 تحميل العرض الفني (Word)", f, file_name="عرض_فني.docx")

        st.success("✅ تم توليد العرض الفني بنجاح!")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
