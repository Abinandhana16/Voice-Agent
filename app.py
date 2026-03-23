import streamlit as st
import speech_recognition as sr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import random

# --- Data Preparation ---
# Sample data for healthcare intents
data = [
    # Appointment booking
    ("I want to book an appointment with a cardiologist", "appointment"),
    ("Schedule a visit to the dentist for tomorrow", "appointment"),
    ("Can I get an appointment with Dr. Smith?", "appointment"),
    ("Need to book a health checkup", "appointment"),
    ("Make a booking for a routine physical", "appointment"),
    
    # Doctor availability
    ("Is the neurologist available today?", "availability"),
    ("When is Dr. Gupta free for a consultation?", "availability"),
    ("Check doctor availability for next Monday", "availability"),
    ("Are there any open slots for an eye specialist?", "availability"),
    ("Is Dr. Sarah available this evening?", "availability"),
    
    # Insurance eligibility
    ("Does my insurance cover skin treatment?", "insurance"),
    ("Check if my insurance is valid here", "insurance"),
    ("Is Medicare accepted by this hospital?", "insurance"),
    ("Am I eligible for cashless treatment?", "insurance"),
    ("Can I use my health insurance for this surgery?", "insurance"),
    
    # General healthcare inquiries
    ("What are the hospital visiting hours?", "general"),
    ("Where is the pharmacy located?", "general"),
    ("Tell me about your emergency services", "general"),
    ("How do I get a medical certificate?", "general"),
    ("What are the symptoms of common flu?", "general")
]

# Convert to DataFrame
df = pd.DataFrame(data, columns=['text', 'intent'])

# --- Model Training ---
# Create a simple NLP pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

# Train the model
model.fit(df['text'], df['intent'])

# Intent to Response mapping
responses = {
    "appointment": [
        "Sure! I can help you book an appointment. Which department or doctor are you looking for?",
        "I can schedule that for you. Please provide your preferred date and time.",
        "We have slots available for next week. Would you like me to book one for you?"
    ],
    "availability": [
        "Let me check the doctor's schedule for you. One moment...",
        "Dr. Smith is available from 10 AM to 2 PM tomorrow. Would you like to book a slot?",
        "Yes, we have specialists available throughout the day. Which specialty are you interested in?"
    ],
    "insurance": [
        "We accept most major insurance providers. Please share your provider name to confirm.",
        "Your insurance eligibility can be verified at the reception desk with your ID card.",
        "Yes, we support Medicare and several private health insurance plans."
    ],
    "general": [
        "Our hospital is open 24/7 for emergencies. Visiting hours are 10 AM to 8 PM.",
        "The pharmacy is located on the ground floor, right next to the main entrance.",
        "Is there anything specific you would like to know about our healthcare services?"
    ],
    "fallback": [
        "I'm sorry, I didn't quite catch that. Could you please rephrase your query?",
        "I'm still learning. Can you try asking about appointments, doctor availability, or insurance?",
        "I'm not sure how to help with that. Feel free to ask about our medical services."
    ]
}

def get_response(user_input):
    # Predict the intent
    intent = model.predict([user_input])[0]
    
    # Check probability (simple fallback logic)
    probs = model.predict_proba([user_input])[0]
    max_prob = max(probs)
    
    if max_prob < 0.3:  # Low confidence threshold
        return random.choice(responses["fallback"])
    
    return random.choice(responses[intent])

# --- Voice Recognition Function ---
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak now.")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.warning("No speech detected.")
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
    return None

# --- Streamlit UI ---
st.set_page_config(page_title="Healthcare Voice Agent", page_icon="🏥")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-bubble {
        background-color: #e1f5fe;
        text-align: right;
    }
    .bot-bubble {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Voice Agent for Healthcare Providers")
st.write("Welcome to the intelligent healthcare assistant. Ask about appointments, doctors, or insurance.")

# Sidebar for information
with st.sidebar:
    st.header("Project Info")
    st.info("""
    **Developer:** AI & DS Student
    **Stack:** Python, Streamlit, Scikit-learn, SpeechRecognition
    **Purpose:** Intelligent Assistant for Healthcare
    """)
    st.write("---")
    st.write("### Sample Queries:")
    st.write("- Book an appointment")
    st.write("- Is Dr. Smith available?")
    st.write("- Does my insurance work here?")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role_class = "user-bubble" if message["role"] == "user" else "bot-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}"><b>{message["role"].capitalize()}:</b> {message["content"]}</div>', unsafe_allow_html=True)

# User Input Layout
col1, col2 = st.columns([4, 1])

with col1:
    user_query = st.text_input("Type your query here...", placeholder="e.g., Book an appointment with cardiologist")

with col2:
    voice_button = st.button("🎤 Listen")

# Process Input
final_query = None

if st.button("Get Response") and user_query:
    final_query = user_query
elif voice_button:
    voice_text = recognize_speech()
    if voice_text:
        st.success(f"Recognized: {voice_text}")
        final_query = voice_text

if final_query:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": final_query})
    
    # Get bot response
    response = get_response(final_query)
    
    # Add bot message to history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update chat display
    st.rerun()

st.write("---")
st.caption("Powered by Natural Language Processing & Speech Recognition")
