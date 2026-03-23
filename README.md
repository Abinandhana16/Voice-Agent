# Voice Agent for Healthcare Providers

An intelligent assistant designed for healthcare providers to streamline patient queries using Natural Language Processing (NLP) and Speech Recognition.

## 🚀 Features
- **Intent Recognition:** Classifies user queries into categories like Appointment Booking, Doctor Availability, and Insurance Eligibility.
- **Voice Support:** Users can interact using voice commands which are converted to text.
- **Interactive UI:** A clean and modern dashboard built with Streamlit.
- **Simple & Fast:** Uses Scikit-learn's Naive Bayes for efficient classification.

## 🛠️ Tech Stack
- **Python**: Core programming language.
- **Streamlit**: Web interface and dashboard.
- **Scikit-learn**: Intent recognition using machine learning (Tf-Idf + Naive Bayes).
- **SpeechRecognition**: Voice-to-text conversion.
- **PyAudio**: Handling microphone input.

## 📂 Project Structure
- `app.py`: Main application code.
- `requirements.txt`: List of dependencies.
- `README.md`: Project documentation.

## 📖 How it Works
1. **User Input:** The user provides input via text or voice.
2. **Preprocessing:** Text is converted to numerical vectors using `TfidfVectorizer`.
3. **Classification:** A Naive Bayes classifier predicts the intent of the query.
4. **Response:** A predefined response is randomly selected and displayed.
