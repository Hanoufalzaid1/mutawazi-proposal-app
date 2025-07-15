from pathlib import Path

# Updated streamlit_app.py with:
# - longer paragraphs
# - cleaned formatting (no **, [])
# - RTL document
# - inserted logo on first page

final_code = '''
import streamlit as st
from docx import Document
from docx.shared import Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from PyPDF2 import PdfReader
import tempfile
import os
from openai import OpenAI
from base64 import b64encode
import re

# إعداد الصفحة
st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

# تحويل صورة الشعار إلى base64 لعرضه في الواجهة
def get_base64_logo(image_path):
    with open(image_path, "rb") as image_file:
        return b64encode(image_file.read()).decode()

logo_base64 = get_base64_logo("logo_corner.png")

# إدراج الشعار في الزاوية العليا اليسرى
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #e6f4ea;
    }}
    .logo-container {{
        position: fixed;
        top: 0px;
        left: 0px;
        z-index: 999;
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

# الواجهة
st.title("منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني تفصيلي واحترافي")

uploaded_file = st.file_uploader("ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("اسم المشروع")
client_name = st.text_input("اسم الجهة")
gov_logo = st.file_uploader("شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

@st.cache_data
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\\n"
    return text

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_detailed_proposal(content, project, client_name):
    sections = {
        "من نحن": "اكتب فقرة مفصلة جدًا عن خلفية الشركة وخبراتها، لا تقل عن 700 كلمة، بأسلوب احترافي وعميق.",
        "فهم المشروع": "اشرح فهمك الكامل والدقيق للمشروع، التحديات، والفرص، مع تفاصيل واضحة جدًا.",
        "نطاق العمل": "افصل مكونات نطاق العمل بدقة مع وصف كل مهمة بمحتوى غني ومترابط وطويل.",
        "المنهجية": "اشرح منهجية التنفيذ بطريقة علمية وعملية مفصلة للغاية تشمل المراحل والأدوات.",
        "الجدول الزمني": "صِف الجدول الزمني المقترح وتفاصيل كل مرحلة، لا تقل عن 4 فقرات.",
        "الفريق المقترح": "صِف الفريق بالأسماء الوهمية، الأدوار، وخبراتهم، بشكل مفصل ومهني.",
        "مؤشرات الأداء": "اكتب عن 5 مؤشرات أداء رئيسية وتفسيرها وربطها بجودة التنفيذ.",
        "إدارة الجودة والمخاطر": "اشرح خطة الجودة وكيف ستتم مراجعة الأداء وتقليل المخاطر.",
        "الاستدامة والتوسع": "اكتب كيف ستضمن استدامة المشروع بعد انتهائه وكيف يمكن تطويره.",
        "الخاتمة": "اختتم بكلمات رسمية تؤكد الالتزام الكامل وتكرار اسم المشروع والجهة."
    }

    results = []
    for title, instruction in sections.items():
        prompt = f"""
كراسة الشروط التالية:
{content}

{instruction}
اكتب القسم بعنوان "{title}" بلغة رسمية، وبتنسيق منسق على شكل فقرات طويلة وواضحة من اليمين لليسار.
"""
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {"role": "system", "content": "أنت خبير استشاري تكتب عروض فنية عالية المستوى باللغة العربية."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8000,
            temperature=0.4
        )
        results.append(f"{title}\\n\\n{response.choices[0].message.content.strip()}\\n\\n")
    
    return "\\n".join(results)

def set_paragraph_rtl(paragraph):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)

if st.button("توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        with st.spinner("جارٍ قراءة الكراسة وتحليلها..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
            proposal_text = generate_detailed_proposal(extracted_text, project_name, client_name)

        doc = Document()
        doc.add_heading(f"العرض الفني لمشروع {project_name}", level=1)
        doc.add_paragraph(f"الجهة: {client_name}")

        if gov_logo:
            temp_logo = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            temp_logo.write(gov_logo.read())
            temp_logo.close()
            doc.add_picture(temp_logo.name, width=Inches(2))
            os.unlink(temp_logo.name)

        for paragraph in proposal_text.split("\\n"):
            line = paragraph.strip()
            line = re.sub(r"\\*\\*(.*?)\\*\\*", r"\\1", line)
            line = re.sub(r"\\[(.*?)\\]", r"\\1", line)
            if line.startswith("### "):
                p = doc.add_heading(line.replace("### ", ""), level=3)
            elif line.startswith("## "):
                p = doc.add_heading(line.replace("## ", ""), level=2)
            elif line.startswith("# "):
                p = doc.add_heading(line.replace("# ", ""), level=1)
            elif line:
                p = doc.add_paragraph(line)
            else:
                continue
            set_paragraph_rtl(p)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            st.download_button("تحميل العرض الفني (Word)", f, file_name=f"عرض_فني_{project_name}.docx")

        st.success("تم توليد العرض الفني بنجاح!")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
'''

# Save to file
final_detailed_path = "/mnt/data/streamlit_app_full_detailed.py"
Path(final_detailed_path).write_text(final_code)
final
