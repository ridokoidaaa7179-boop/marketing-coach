import streamlit as st
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="مدرب التسويق الذكي", page_icon="🤖")

st.title("🤖 مدربك التسويقي الخاص")
st.info("خبير في قطع الغيار، أعمال الليزر، وفطور خات")

# جلب المفتاح من الخزنة السرية
API_KEY = st.secrets["GEMINI_API_KEY"]

if API_KEY:
    genai.configure(api_key=API_KEY)

# تحميل بيانات مشاريعك
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        context = f.read()
except Exception:
    context = "بيانات المشاريع غير موجودة"

model = genai.GenerativeModel('gemini-1.5-flash')

# شات التطبيق
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اسألني عن خطة تسويقية أو فكرة جديدة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    full_prompt = f"أنت مدرب تسويق خبير. هذه بيانات مشاريعي:\n{context}\n\nالسؤال: {prompt}"
    
    try:
        response = model.generate_content(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
