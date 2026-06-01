🎤 AI Pengalihan Kode Suara (Speech-to-Speech NLP System)
Sistem NLP multilingual real-time berbasis AI yang mampu mengubah suara menjadi respons suara dalam berbagai bahasa menggunakan pipeline:

🎙️ Whisper (Speech-to-Text)
🧠 Gemma / LLM (Text Reasoning & Response Generation)
🔊 XTTS / Edge-TTS (Text-to-Speech)
⚡ FastAPI (Backend API)
🎛️ Gradio (Frontend Interface)
✨ Features
🎤 Speech-to-Speech AI Pipeline
🌐 Multilingual Support:
- Bahasa Indonesia
- English
- Arabic

🔄 Code-Switching Detection
🤖 AI Response with LLM (Gemma)
🔊 Natural Voice Output (TTS)
⚡ Real-time Processing
🎛️ Simple Web UI (Gradio)

📁 Project Structure
voice-cs-system/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── whisper_asr.py
│   │   ├── llm.py
│   │   ├── tts.py
│   │   └── utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── .env
├── README.md
└── requirements.txt

⚙️ Installation
1. Clone Repository
git clone https://github.com/username/voice-cs-system.git
cd voice-cs-system

2. Buat Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate
Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

# Model Settings
WHISPER_MODEL=base
LLM_MODEL=gemma

# API Config
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8080

# TTS Config
TTS_ENGINE=xtts

# Optional API Keys (jika pakai cloud LLM)
OPENAI_API_KEY=your_key_here
🚀 Cara Menjalankan Backend (FastAPI)
Jalankan server:
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
📌 Backend akan berjalan di:
http://localhost:8080

🎛️ Cara Menjalankan Frontend (Gradio)
Buka terminal baru:
python gradio_app/app.py

Jika sukses, akan muncul:
Running on local URL:  http://127.0.0.1:7863
🔄 Alur Sistem
🎤 Audio Input
      ↓
📝 Whisper (Speech-to-Text)
      ↓
🧠 Gemma / LLM Processing
      ↓
🌐 Code-Switch Detection (optional)
      ↓
🔊 XTTS / Edge-TTS
      ↓
🎧 Audio Output
🧪 Testing API (Optional)
Upload audio:
POST /transcribe
Request response:
{
  "text": "Hello how are you"
}
📦 Requirements

Project NLP – Speech-to-Speech AI System
Dibuat untuk kebutuhan pembelajaran Natural Language Processing (NLP) dan sistem AI real-time.