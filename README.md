🧠 AI — Intelligent Q&A System (Voice + PDF + RAG)

🎤 Your personal offline ChatGPT-like assistant that can read PDFs, understand your questions, and speak answers back — powered by LangChain + Hugging Face + SpeechRecognition + pyttsx3.

🚀 Overview

The AI — Intelligent Q&A System is a local Generative AI assistant that combines:

🧩 Retrieval-Augmented Generation (RAG)

🗂️ Document intelligence (PDF parsing)

🎙️ Voice input & output (SpeechRecognition + TTS)

You can upload any PDF, ask questions by typing or speaking, and the AI will:

Extract content from your document

Use free Hugging Face models (FLAN-T5 Small) to understand and answer

Speak the answer back to you with natural voice

⚡ Works entirely offline — no OpenAI API keys or paid models required.

✨ Features

✅ Upload PDF files (books, notes, research papers, resumes, etc.)
✅ Ask questions by typing or voice
✅ Listen to the AI’s spoken answers
✅ Chat continuously in Voice Chat Mode
✅ Uses local FLAN-T5-small model (lightweight, ~500MB)
✅ RAG pipeline with FAISS + SentenceTransformer embeddings
✅ Streamlit frontend with clean, responsive UI

🧰 Tech Stack
Component	Technology
💬 LLM	FLAN-T5 Small

🧠 Framework	LangChain

🗂️ Vector DB	FAISS
🗃️ Embeddings	SentenceTransformer (all-MiniLM-L6-v2)
🧾 Frontend	Streamlit
🎙️ Voice Input	SpeechRecognition
🔊 Voice Output	pyttsx3 (SAPI5, Windows TTS)
🧩 PDF Parsing	PyMuPDF (fitz)
📁 Project Structure
AI-Intelligent-QnA/
│
├── backend/
        AI note.pdf
│   ├── main.py              # RAG entry point
│   ├── rag_pipeline.py      # RAG building (LangChain + HF)
│   ├── pdf_loader.py        # PDF text extraction
│                  
│
├── frontend/
│   └── app.py               # Streamlit + Voice Assistant UI
│

├── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/<your-username>/AI-Intelligent-QnA.git
cd AI-Intelligent-QnA

2️⃣ Create Virtual Environment
python -m venv mvenv
mvenv\Scripts\activate       # On Windows
# source mvenv/bin/activate  # On Linux/Mac

3️⃣ Install Dependencies
pip install -r requirements.txt


If you don’t have requirements.txt, create it with:

langchain
langchain-community
langchain-huggingface
streamlit
speechrecognition
pyttsx3
pyaudio
python-dotenv
pymupdf
faiss-cpu
sentence-transformers
pythoncom

4️⃣ (Optional) Install PyAudio Safely
pip install pipwin
pipwin install pyaudio

🧠 Run the App
▶️ Start Backend + Frontend (Single Command)
cd frontend
streamlit run app.py

🧩 Then:

Upload your PDF file

Click 🎤 Speak Now or type your question

Watch the magic — AI reads, answers, and speaks back to you!

🎧 Voice Chat Mode

Once a PDF is uploaded, click:

🎧 Start Voice Chat Mode


You can then talk freely — ask multiple questions without pressing any buttons.
To stop, click:

🛑 Stop Voice Chat

🧩 Example Demo

📘 Example PDF: AI_notes.pdf

Action	Description
🎤 Speak: “Explain neural networks”	AI extracts relevant content
🤖 Answer: “A neural network is a system of connected nodes that learns patterns from data…”	
🔊 Voice: Speaks the same response aloud	
🧱 Key Concepts Demonstrated

✅ Retrieval-Augmented Generation (RAG)

✅ LangChain document loading & embeddings

✅ Local LLM integration (Hugging Face)

✅ Speech-to-Text and Text-to-Speech orchestration

✅ Streamlit multi-threaded voice app design

✅ End-to-end GenAI pipeline with no API cost

📸 Screenshots (Add after testing)
Feature	Preview
App Interface	(Add screenshot here)
Voice Input + Output	(Add screenshot here)
Continuous Chat Mode	(Add screenshot here)
👨‍💻 Author

👤 Chandan Kheto
💼 AI / ML / NLP / GenAI Developer
🌍 Building AI-powered applications for real-world use
📧 Reach me on LinkedIn

⭐ Future Enhancements

Add multilingual speech support (Whisper + gTTS)

Add chat memory (LangChain Memory)

Integrate OpenAI or Gemini for optional cloud inference

Build Docker container for easy deployment

🏁 License

This project is open-source under the MIT License

💬 Closing Note

“You don’t need an API key to build powerful AI —
you just need creativity, open-source tools, and consistency.”

💡 Built with ❤️ by Chandan Kheto.
