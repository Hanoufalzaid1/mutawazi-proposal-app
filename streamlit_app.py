import streamlit as st
from docx import Document
import base64
import os

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني ومالي تلقائيًا")

uploaded_file = st.file_uploader("📤 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع")
client_name = st.text_input("🏛️ اسم الجهة")
gov_logo = st.file_uploader("🎖️ شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

if st.button("🚀 توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        # Placeholder action: just show confirmation
        st.success("✅ تم توليد العرض الفني بنجاح!")
        st.download_button("📥 تحميل العرض الفني (Word)", "ملف وهمي", file_name="عرض_فني.docx")
        st.download_button("📥 تحميل العرض الفني (PDF)", "ملف وهمي", file_name="عرض_فني.pdf")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
