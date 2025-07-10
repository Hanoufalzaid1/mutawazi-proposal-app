import streamlit as st
from docx import Document
from PyPDF2 import PdfReader
import base64
import os
import tempfile

st.set_page_config(page_title="منصة إعداد العروض - متوازي", layout="centered")

st.title("📄 منصة إعداد العروض - متوازي")
st.markdown("قم برفع كراسة الشروط وسيتم توليد عرض فني تلقائيًا بنفس تنسيق عروض متوازي")

uploaded_file = st.file_uploader("📤 ارفع كراسة الشروط (PDF)", type=["pdf"])
project_name = st.text_input("📌 اسم المشروع")
client_name = st.text_input("🏛️ اسم الجهة")
gov_logo = st.file_uploader("🎖️ شعار الجهة الحكومية (اختياري)", type=["png", "jpg"])

# قالب ثابت لعناوين العرض الفني
SECTION_TITLES = [
    "من نحن",
    "رؤيتنا",
    "رسالتنا",
    "خدماتنا",
    "فهمنا للمشروع",
    "أهداف المشروع",
    "نطاق العمل والمسؤوليات",
    "المنهجية المقترحة لتنفيذ المشروع",
    "الخطة الزمنية للمشروع",
    "مخرجات المشروع المتوقعة",
    "الفريق المقترح",
    "هيكل الفريق وخبراته",
    "الملحقات الفنية"
]

# نصوص افتراضية لكل قسم
DEFAULT_CONTENT = {
    "من نحن": "نحن في متوازي نُمكِّن المؤسسات من التحول بالذكاء الاصطناعي بثقة عبر خدمات استراتيجية وتطبيقية...",
    "رؤيتنا": "أن نكون الشريك الموثوق في التحول المؤسسي وحوكمة الذكاء الاصطناعي.",
    "رسالتنا": "تمكين المنظمات من تنفيذ استراتيجياتها بنجاح وقيادة التحول عبر أطر فعالة.",
    "خدماتنا": "نقدم خدمات في الحوكمة، إدارة المشاريع، إدارة المخاطر، الذكاء الاصطناعي، والامتثال للمعايير الدولية...",
    "فهمنا للمشروع": "استنادًا إلى الكراسة، نُدرك أن الجهة تسعى إلى...",
    "أهداف المشروع": "يهدف المشروع إلى...",
    "نطاق العمل والمسؤوليات": "يتضمن نطاق العمل توفير...",
    "المنهجية المقترحة لتنفيذ المشروع": "نقترح منهجية تعتمد على...",
    "الخطة الزمنية للمشروع": "من المتوقع تنفيذ المشروع خلال...",
    "مخرجات المشروع المتوقعة": "تشمل المخرجات ما يلي...",
    "الفريق المقترح": "يتكون الفريق من مختصين في...",
    "هيكل الفريق وخبراته": "تم تصميم هيكل الفريق ليشمل...",
    "الملحقات الفنية": "سيتم إرفاق جميع المستندات الداعمة هنا."
}

# استخراج النص من الكراسة
@st.cache_data
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# تحليل الكراسة وتوليد محتوى مخصص (بسيط مبدئي)
def parse_requirements(text):
    content = DEFAULT_CONTENT.copy()
    if "الأهداف" in text:
        content["أهداف المشروع"] = "تم تحديد أهداف المشروع بناءً على الكراسة لتشمل..."
    if "نطاق العمل" in text:
        content["نطاق العمل والمسؤوليات"] = "وفقًا للكراسة، يشمل نطاق العمل..."
    if "الجدول الزمني" in text:
        content["الخطة الزمنية للمشروع"] = "تشير الكراسة إلى تنفيذ المشروع خلال..."
    return content

if st.button("🚀 توليد العرض الفني"):
    if uploaded_file and project_name and client_name:
        raw_text = extract_text_from_pdf(uploaded_file)
        parsed_sections = parse_requirements(raw_text)

        doc = Document()
        doc.add_heading(f"العرض الفني لمشروع {project_name}", level=1)
        doc.add_paragraph(f"الجهة: {client_name}")

        for title in SECTION_TITLES:
            doc.add_heading(title, level=2)
            doc.add_paragraph(parsed_sections.get(title, ""))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            doc.save(tmp.name)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            st.download_button("📥 تحميل العرض الفني (Word)", f, file_name=f"عرض_فني_{project_name}.docx")

        st.success("✅ تم توليد العرض الفني بنجاح!")
    else:
        st.error("يرجى تعبئة جميع الحقول المطلوبة.")
