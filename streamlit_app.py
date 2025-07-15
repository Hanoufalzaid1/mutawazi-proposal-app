import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import tempfile
import os
from openai import OpenAI
from textwrap import dedent
from base64 import b64encode

# إعداد الصفحة
st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

# تحويل صورة الشعار إلى base64 لعرضها في الزاوية
def get_base64_logo(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode()

logo_base64 = get_base64_logo("logo_corner.png")

# إدراج الشعار والثيم
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #e6f4ea;
    }}
    h1 {{
        color: #004d26;
    }}
    .stTextInput > div > div > input {{
        background-color: #f7fcf9;
        border: 1px solid #aad4bc;
    }}
    .stDownloadButton button {{
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
    }}
    .stButton button {{
        background-color: #388e3c;
        color: white;
        border-radius: 8px;
    }}
    .logo-container {{
        position: fixed;
        bottom: 15px;
        right: 15px;
        z-index: 100;
    }}
    .logo-container img {{
        width: 80px;
        opacity: 0.95;
    }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="شعار متوازي">
    </div>
    """,
    unsafe_allow_html=True
)

# عنوان الصفحة
st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني احترافي")

# مدخلات المستخدم
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

# تهيئة OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# توليد العرض الفني باستخدام GPT
def generate_proposal(content, project, client_name):
    system_prompt = "أنت مساعد خبير في كتابة العروض الفنية بناءً على كراسة الشروط."
    user_prompt = f"""هذه كراسة شروط لمشروع جديد: {content}

اكتب عرضًا فنيًا متكاملًا باسم المشروع: {project} والجهة: {client_name}، وابدأه بمقدمة من نحن، ثم فهم المشروع، نطاق العمل، المنهجية، الجدول الزمني، الفريق المقترح، والخاتمة.
"""
    response = client.chat.completions.create(
        model="gpt-4-turbo-2024-04-09",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=3000,
        temperature=0.7
    )
    return response.choices[0].message.content

# عند الضغط على زر توليد
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
