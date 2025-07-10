import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import tempfile
import os

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")
st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني احترافي")

uploaded_file = st.file_uploader("📤 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع")
client_name = st.text_input("🏛️ اسم الجهة")
gov_logo = st.file_uploader("🎖️ شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

# استخراج النص من PDF
@st.cache_data
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# توليد العرض الفني باستخدام نموذج مضمّن محليًا
from textwrap import dedent

import openai
import os

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_proposal(content, project, client):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "أنت خبير في كتابة العروض الفنية لشركات استشارية."},
            {"role": "user", "content": f"""اكتب عرضًا فنيًا احترافيًا لمشروع بعنوان "{project}" تابع للجهة "{client}"، واستند إلى المعلومات التالية من كراسة الشروط:\n{content[:3000]}"""}
        ],
        temperature=0.6,
        max_tokens=1800,
    )
    return response.choices[0].message.content

if st.button("🚀 توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        with st.spinner("📖 جارٍ قراءة الكراسة وتحليلها..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            proposal_text = generate_proposal(extracted_text, project_name, client_name)

        doc = Document()
        doc.add_heading(f"العرض الفني لمشروع {project_name}", level=1)
        doc.add_paragraph(f"الجهة: {client_name}")

        for section in proposal_text.split("\n\n"):
            lines = section.strip().split("\n", 1)
            if len(lines) == 2:
                title, content = lines
                doc.add_heading(title.strip(), level=2)
                doc.add_paragraph(content.strip())
            else:
                doc.add_paragraph(section.strip())

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            st.download_button("📥 تحميل العرض الفني (Word)", f, file_name=f"عرض_فني_{project_name}.docx")

        st.success("✅ تم توليد العرض الفني بنجاح!")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
