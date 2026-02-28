import streamlit as st
import google.generativeai as genai

# --- 1. PAGE SETUP & UI ---
st.set_page_config(page_title="Mera Personal English Teacher", layout="wide", page_icon="👨‍🏫")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; font-weight: bold; border: none; font-size: 16px; transition: 0.3s; padding: 10px;}
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .card { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #11998e; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE API CONFIGURATION ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("❌ API Key Error: Streamlit Settings > Secrets mein 'GEMINI_API_KEY' set karein.")
    st.stop()

# --- 3. SIDEBAR: MODEL SELECTION & NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/reading.png", width=80)
    st.title("⚙️ Teacher Settings")
    
    available_models = {
        "Gemini 3.1 Pro Preview (Best)": "gemini-3.1-pro-preview",
        "Gemini 3 Flash Preview (Fast)": "gemini-3-flash-preview",
        "Gemini 2.5 Pro": "gemini-2.5-pro"
    }
    selected_model_id = available_models[st.selectbox("Select AI Model:", list(available_models.keys()))]
    
    st.markdown("---")
    st.title("📚 Padhaai Ke Levels")
    app_mode = st.radio("Aaj kya seekhna hai?", [
        "1. Uchaaran (Pronunciation) 🗣️", 
        "2. Roj ke Shabd (Basic Words) 🍎", 
        "3. Baat-cheet (Conversation) 🤝", 
        "4. Formal & Legal Email 📧"
    ])

# Initialize AI Model
model = genai.GenerativeModel(selected_model_id)

st.title("👨‍🏫 Mera Personal English Teacher")
st.write("Namaste! Main aapka AI teacher hun. Main aapko bilkul zero se English sikhayunga. Ghabrayein nahi, hum aaram se seekhenge.")

# --- MODULE 1: UCHAARAN (PRONUNCIATION) ---
if app_mode == "1. Uchaaran (Pronunciation) 🗣️":
    st.header("🗣️ Uchaaran (Sahi se bolna seekhein)")
    st.write("Aapko 'b', 'v', 'श', 'स' ya kisi English word ko bolne mein dikkat hai? Yahan type karein.")
    
    word_to_pronounce = st.text_input("Kaunsa shabd bolna seekhna hai? (Jaise: 'v', 'school', 'environment')")
    
    if st.button("Sikhao Teacher 🎓"):
        if word_to_pronounce:
            prompt = f"""
            Aap ek patient English teacher hain. User ekdam beginner hai aur use Hindi mein 'b', 'v', 'श', 'स' aur hard English words bolne mein dikkat hoti hai. 
            User ne '{word_to_pronounce}' bolna seekhne ko kaha hai. 
            Kripya bilkul simple Hindi mein samjhayein ki is shabd ya akshar ko bolte waqt:
            1. Honth (lips) kaise rakhne hain?
            2. Jeebh (tongue) kahan touch karni chahiye?
            3. Hawa kaise nikalni hai?
            Isko ek 1 saal ke bacche ko bolna sikhane wale pyaar se samjhayein.
            """
            with st.spinner("Teacher aapke liye aasan tarika soch rahe hain..."):
                response = model.generate_content(prompt)
                st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
        else:
            st.warning("Pehle koi shabd likhein.")

# --- MODULE 2: BASIC WORDS ---
elif app_mode == "2. Roj ke Shabd (Basic Words) 🍎":
    st.header("🍎 Rojmara ke Basic Shabd")
    st.write("Aaiye roz use hone wale chote-chote shabd seekhein.")
    
    category = st.selectbox("Kaunse shabd seekhne hain?", ["Ghar ke saaman", "Rishte (Family)", "Bhavnayein (Feelings)", "Office ke shabd"])
    
    if st.button("Aaj ke 5 naye shabd dikhao 📝"):
        prompt = f"""
        User bilkul zero level par hai. Use '{category}' se jude 5 aasan English words sikhayein.
        Format yeh hona chahiye:
        1. English Word
        2. Hindi Meaning
        3. Bolna kaise hai? (Uchaaran Hindi script mein, jaise Apple -> एप्पल)
        4. Ek chota sa aasan vakya (sentence).
        """
        with st.spinner("Naye shabd taiyar ho rahe hain..."):
            response = model.generate_content(prompt)
            st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)

# --- MODULE 3: CONVERSATION ---
elif app_mode == "3. Baat-cheet (Conversation) 🤝":
    st.header("🤝 Logon se Baat-cheet karna")
    st.write("Aap kisi se Hindi mein kya kehna chahte hain? Yahan likhein, main aapko bataunga use English mein kaise bolna hai.")
    
    hindi_sentence = st.text_area("Apni baat Hindi (ya Hinglish) mein likhein:", placeholder="Jaise: Mujhe aapse ek zaroori baat karni hai...")
    
    if st.button("English mein Translate karein 🔄"):
        if hindi_sentence:
            prompt = f"""
            User ko English bilkul nahi aati. User kehna chahta hai: "{hindi_sentence}"
            1. Iski bilkul aasan aur natural English translation dijiye.
            2. Use padhna kaise hai (Hindi mein uchaaran likhein).
            3. Grammer ka ek chota sa rule samjhayein (bahut simple bhasha mein).
            """
            with st.spinner("Translate kar rahe hain..."):
                response = model.generate_content(prompt)
                st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
        else:
            st.warning("Pehle kuch likhein.")

# --- MODULE 4: FORMAL & LEGAL EMAIL ---
elif app_mode == "4. Formal & Legal Email 📧":
    st.header("📧 Formal aur Legal Email Likhna")
    st.write("Aapko kisi ko professional ya legal email bhejna hai? Aap bas apni aam bhasha mein likh dein ki kya likhna hai, AI use perfect legal English mein badal dega.")
    
    email_idea = st.text_area("Aap email mein kya kehna chahte hain? (Tooti-footi Hindi mein likh dein)", height=150, placeholder="Jaise: Mujhe court mein apni date aage badhani hai kyunki meri tabiyat kharab hai, please judge sahab ko mail likh do...")
    email_tone = st.radio("Email ka style kaisa hona chahiye?", ["Formal (Office ke liye)", "Legal (Vakeel/Court/Police ke liye)"])
    
    if st.button("✨ Mera Perfect Email Banaiye"):
        if email_idea:
            prompt = f"""
            User ki English weak hai. User ka idea yeh hai: "{email_idea}"
            User chahta hai ki is par ek '{email_tone}' email likha jaye.
            
            Kripya ek perfect, professional aur grammatically correct English Email draft karein. 
            Email ke brackets mein [Name], [Date] aadi likhein taaki user apna detail bhar sake.
            Niche ek line mein us email ka Hindi summary bhi de dein taaki user samajh sake ki usne kya bheja hai.
            """
            with st.spinner("Aapka professional email likha ja raha hai..."):
                response = model.generate_content(prompt)
                st.success("✅ Aapka Email Ready hai!")
                st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
        else:
            st.warning("Pehle likhein ki email mein kya batana hai.")
