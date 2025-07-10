import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import openai
import tempfile
import os

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")
st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني احترافي باستخدام ChatGPT")

# قراءة مفتاح OpenAI API من متغير البيئة الآمن
openai.api_key = os.environ.get("OPENAI_API_KEY")

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

# توليد العرض الفني باستخدام ChatGPT (التوافق مع openai>=1.0.0)
def generate_proposal(content, project, client):
    system_msg = """
    أنت مساعد محترف متخصص في كتابة العروض الفنية. الرجاء كتابة عرض فني متكامل باللغة العربية لشركة استشارية سعودية تدعى \"متوازي\".
    العرض يجب أن يشمل العناصر التالية:
    1. من نحن
    2. رؤيتنا
    3. رسالتنا
    4. خدماتنا
    5. فهم المشروع
    6. أهداف المشروع
    7. نطاق العمل والمسؤوليات
    8. المنهجية المقترحة لتنفيذ المشروع
    9. الخطة الزمنية للمشروع
    10. مخرجات المشروع المتوقعة
    11. الفريق المقترح
    12. هيكل الفريق وخبراته
    13. الملاحق الفنية
    الرجاء الاعتماد على محتوى الكراسة المرفقة التي توضح متطلبات المشروع.
    """
    user_msg = f"اسم المشروع: {project}\nاسم الجهة: {client}\nمحتوى الكراسة:\n{content}"

    chat_response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.5,
        max_tokens=3000
    )
    return chat_response.choices[0].message.content

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

        st.success("✅ تم توليد العرض الفني بنجاح باستخدام ChatGPT!")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
