# Erick AI 🤖

A personal AI chat assistant powered by **Google Gemini 2.5**, built with Python and Streamlit.

## ✨ Features

- 🌐 **Beautiful Web UI** — Modern chat interface built with Streamlit
- 🤖 **AI Personality Presets** — Choose from Friendly Assistant, Tech Lead, Creative Writer, Educator, or set a Custom persona
- 🧠 **Model Selection** — Switch between `gemini-2.5-flash` and `gemini-2.5-pro`
- 🔍 **Google Search Grounding** — Toggle real-time web search so the AI can cite live sources
- 💾 **Download Chat History** — Export your conversation as a `.txt` file
- ⚡ **Streaming Responses** — See the AI's answer appear in real time

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A free Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Erick-litmus/Erick-litmus.git
   cd Erick-litmus
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   ```

3. **Set up your API key:**
   - Copy `.env.template` to `.env`
   - Paste your Gemini API key inside:
     ```
     GEMINI_API_KEY=your_key_here
     ```

4. **Run the Web UI:**
   ```bash
   .venv\Scripts\streamlit run app.py
   ```

5. **Or run the terminal chat:**
   ```bash
   .venv\Scripts\python assistant.py
   ```

## 📁 Project Structure

```
Erick-litmus/
├── app.py              # Streamlit Web UI
├── assistant.py        # Terminal-based chat client
├── requirements.txt    # Python dependencies
├── .env.template       # API key template
└── .gitignore          # Ignored files (includes .env)
```

## 🔒 Security
Your `.env` file containing your API key is excluded from version control via `.gitignore`. **Never share your API key publicly.**

## 📄 License
MIT License — feel free to use, modify, and share!
