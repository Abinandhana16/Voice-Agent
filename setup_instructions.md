# Setup Instructions

Follow these steps to run the Voice Agent for Healthcare Providers on your local machine.

### Prerequisites
- Python 3.8 or higher installed.
- A working microphone for voice input.

### Step 1: Clone or Copy the Files
Create a folder for the project and place `app.py` and `requirements.txt` inside it.

### Step 2: Install Dependencies
Open your terminal or command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```
*Note: If you face issues with `pyaudio`, you might need to install it specifically for your OS (e.g., `pip install pipwin` then `pipwin install pyaudio` on Windows).*

### Step 3: Run the Application
Launch the Streamlit app by running:
```bash
streamlit run app.py
```

### Step 4: Access the UI
Once the command runs, a local URL (usually `http://localhost:8501`) will open in your default browser.

### Sample Queries to Try
1. "I want to schedule an appointment with a cardiologist."
2. "Is Dr. Smith free tomorrow?"
3. "Do you accept Medicare?"
4. "What are the visiting hours?"
