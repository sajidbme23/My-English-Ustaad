import streamlit as st
import google.generativeai as genai

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Meri English Book & AI Dost", layout="wide", page_icon="📖")

st.markdown("""
    <style>
    .topic-btn>button { width: 100%; border-radius: 5px; background-color: #f0f2f6; color: #000; text-align: left; padding: 10px; border: 1px solid #ddd; margin-bottom: 5px; transition: 0.2s;}
    .topic-btn>button:hover { background-color: #e0e4eb; border-color: #11998e; }
    .lesson-card { background-color: #ffffff; padding: 25px; border-radius: 10px; border-top: 5px solid #11998e; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. API SETUP ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key Error: Streamlit Settings > Secrets mein 'GEMINI_API_KEY' set karein.")
    st.stop()

model = genai.GenerativeModel("gemini-3.1-pro-preview")

# --- 3. SESSION STATES ---
if "active_topic" not in st.session_state:
    st.session_state.active_topic = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "model", "content": "Hello mere dost! Main tumhara AI saathi hoon. Aao milkar English seekhein. Aaj kya baat karni hai?"}
    ]

# --- 4. FULL ENGLISH SYLLABUS (BOOKLET) ---
syllabus = {
    "Level 1: Bilkul Shuruat (Zero Level)": [
        "1. ABCD aur Uchaaran (b, v, श, स bolna)", 
        "2. This, That, These, Those ka use", 
        "3. He, She, It, They (Kiske liye kya lagayein?)", 
        "4. A, An, The kahan lagta hai?"
    ],
    "Level 2: Chhote Vakya (Basic Sentences)": [
        "5. Is, Am, Are ka sahi istemaal", 
        "6. Was, Were (Biti hui baatein)", 
        "7. Has, Have, Had (Mere paas kuch hai)", 
        "8. In, On, At, Under (Cheezein kahan hain?)"
    ],
    "Level 3: Tenses (Kaal - Sabse Zaroori)": [
        "9. Present Tense (Jo abhi ho raha hai)", 
        "10. Past Tense (Jo kal hua tha)", 
        "11. Future Tense (Jo aage hoga)", 
        "12. Can, Could, Should (Modals)"
    ],
    "Level 4: Advanced & Reading": [
        "13. Kisi se pehli baar milna (Introduction)", 
        "14. 'How to Win Friends' book se reading aur vocabulary", 
        "15. Office aur Legal Email likhna",
        "16. Phone par English mein baat karna"
    ]
}

# --- 5. APP LAYOUT (TABS) ---
tab1, tab2 = st.tabs(["📖 English Booklet (Syllabus)", "🗣️ AI Dost (Chat & Practice)"])

# ==========================================
# TAB 1: BOOKLET (SYLLABUS)
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2.5])
    
    # Left Column: Index/Buttons
    with col1:
        st.subheader("📑 Topics (Index)")
        for level, topics in syllabus.items():
            with st.expander(level, expanded=True):
                for topic in topics:
                    if st.button(topic, key=topic, use_container_width=True):
                        st.session_state.active_topic = topic

    # Right Column: Lesson Explanation
    with col2:
        if st.session_state.active_topic:
            st.header(f"📘 Topic: {st.session_state.active_topic}")
            
            prompt = f"""
            Tum ek bahut hi pyaar se padhane wale English teacher ho. Tumhara student bilkul zero level par hai.
            Aaj ka topic hai: "{st.session_state.active_topic}".
            
            Is topic ko bilkul simple, aam bolchaal wali Hindi/Hinglish mein samjhao jaise kisi chhote bacche ko samjha rahe ho.
            Bahut saare aasan examples do.
            Agar uchaaran (pronunciation) ka topic ho, toh batao honth aur jeebh kaise chalani hai.
            Agar 'How to Win Friends' ka topic ho, toh book ke pehle chapter ki ek chhoti si line dekar uska meaning aur naye words samjhao.
            Samjhane ka tarika lamba aur detail mein hona chahiye, par bhasha bahut aasan ho.
            """
            
            with st.spinner("Teacher aapke liye lesson taiyar kar rahe hain..."):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='lesson-card'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error("Error aayi. Thodi der baad try karein.")
        else:
            st.info("👈 Left side se koi bhi topic chunein aur padhai shuru karein!")

# ==========================================
# TAB 2: AI DOST (CHAT & PRACTICE)
# ==========================================
with tab2:
    st.subheader("💬 Apne AI Dost se baat karein")
    st.write("Aap yahan Hindi, Hinglish ya tooti-futi English mein baat kar sakte hain. Agar aap English mein galti karenge, toh ye dost aapko sahi karega.")
    
    # Purani chat dikhana
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Naya message type karna
    user_input = st.chat_input("Apne dost se kuch kahiye (Hindi ya English mein)...")
    
    if user_input:
        # User ka message screen par dikhana aur save karna
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # AI se response lena
        chat_prompt = f"""
        Tumhara naam 'AI Dost' hai. Tum user ke best friend aur English tutor ho. 
        User ko English theek se nahi aati aur wo seekh raha hai.
        
        User ne abhi ye kaha: "{user_input}"
        
        TUMHARA KAAM:
        1. Ek dost ki tarah natural aur friendly reply do (Hindi/Hinglish mein).
        2. AGAR user ne English mein likhne ki koshish ki hai aur usme Grammer ya spelling ki galti hai, toh bahut pyaar se batao: "Dost, tumne achhi koshish ki, par isko sahi tarike se aise bolenge: [Sahi English sentence]". Aur galti ka reason chote mein samjhao.
        3. AGAR user ne Hindi mein likha hai, toh uska reply do aur sath mein batao ki "Is baat ko English mein aise bolte hain: [English Translation]".
        4. Hamesha user ko motivate karo.
        """
        
        with st.chat_message("model"):
            with st.spinner("Dost type kar raha hai..."):
                try:
                    response = model.generate_content(chat_prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "model", "content": response.text})
                except Exception as e:
                    st.error("Dost ka network slow hai, baad mein try karein.")
