import streamlit as st
import google.generativeai as genai

# إعداد واجهة التطبيق
st.set_page_config(page_title="مدرب التسويق الذكي", page_icon="🤖")

st.title("🤖 مدربك التسويقي الخاص")
st.info("خبير في قطع الغيار، أعمال الليزر، وفطور خات")

# --- ضع مفتاحك هنا ---
# استبدل الجملة بالأسفل بمفتاح الـ API الذي نسخته سابقاً
API_KEY = "AIzaSyAZVRCK1h8UxcgRTJ_KfwXmwO22-at1ogo" 
# -----------------------

if API_KEY != "ضعه_هنا":
    genai.configure(api_key=API_KEY)
    
    # تحميل بيانات مشاريعك
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            context = f.read()
    except:
        context = "بيانات المشاريع غير موجودة."

    model = genai.GenerativeModel('gemini-1.5-flash')

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("اسألني عن خطة تسويقية أو فكرة جديدة..."):
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            full_prompt = f"أنت مدرب تسويق استراتيجي. معلومات مشاريعي: {context}. أجب على: {user_input}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
else:
    st.warning("يرجى وضع مفتاح الـ API داخل الكود ليعمل التطبيق.")
