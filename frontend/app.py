import streamlit as st
import os, sys, time, threading
import speech_recognition as sr
import pyttsx3
import pythoncom

# ---- backend path ----
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend"))
sys.path.append(backend_path)
from main import run_rag

# ---- page config ----
st.set_page_config(page_title="AI — Intelligent Qns & Ans System", page_icon="🧠", layout="wide")
st.title("🧠 AI — Intelligent Qns & Ans System (Voice + PDF + RAG)")
st.markdown("🎤 Talk or type to your documents using local Hugging Face models (FLAN-T5 Small).")

# ---- TTS: reliable blocking speech on Windows ----
def speak_blocking(text: str):
    """
    Reliable TTS on Windows (no 'run loop already started').
    Uses SAPI5 and initializes COM for the current thread.
    """
    try:
        pythoncom.CoInitialize()
        eng = pyttsx3.init(driverName="sapi5")
        eng.setProperty("rate", 170)
        voices = eng.getProperty("voices")
        eng.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
        eng.say(text)
        eng.runAndWait()
        eng.stop()
    except Exception as e:
        print(f"TTS error: {e}")

# ---- session state ----
ss = st.session_state
ss.setdefault("chat_history", [])
ss.setdefault("chat_running", False)
ss.setdefault("last_user", "")
ss.setdefault("last_ai", "")
ss.setdefault("status", "")

# ---- UI placeholders ----
status_ph = st.empty()
heard_ph = st.empty()
reply_ph = st.empty()

# ---- file upload ----
uploaded = st.file_uploader("📄 Upload your PDF", type=["pdf"])
typed_q = st.text_input("💬 Or type a question:")

# ---- Speech recognition helper ----
def listen_once(recognizer: sr.Recognizer) -> str:
    with sr.Microphone() as source:
        ss.status = "🎧 Listening... Speak now!"
        status_ph.info(ss.status)
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    ss.status = "🧠 Recognizing..."
    status_ph.info(ss.status)
    return recognizer.recognize_google(audio)

# ---- Instant Voice Mode ----
st.markdown("### 🎙️ Speak Your Question (Instant Mode)")
if st.button("🎤 Speak Now"):
    if not uploaded:
        st.warning("⚠️ Please upload a PDF first.")
    else:
        recognizer = sr.Recognizer()
        try:
            query = listen_once(recognizer)
            heard_ph.success(f"✅ You said: **{query}**")

            pdf_path = "temp.pdf"
            with open(pdf_path, "wb") as f:
                f.write(uploaded.read())

            with st.spinner("📚 Processing your document..."):
                response = run_rag(pdf_path, query)
            os.remove(pdf_path)

            reply_ph.markdown(f"**🤖 AI:** {response}")
            speak_blocking(response)

            ss.last_user, ss.last_ai = query, response
            ss.chat_history.append({"question": query, "answer": response})
            status_ph.success("✅ Response generated & spoken!")

        except sr.UnknownValueError:
            st.error("❌ Could not understand your voice.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# ---- Typed Question ----
if st.button("Ask (Typed Question)"):
    if not uploaded or not typed_q.strip():
        st.warning("⚠️ Please upload a PDF and type a question.")
    else:
        pdf_path = "temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded.read())

        with st.spinner("🧠 Thinking..."):
            answer = run_rag(pdf_path, typed_q.strip())
        os.remove(pdf_path)

        reply_ph.markdown(f"**🤖 AI:** {answer}")
        speak_blocking(answer)
        ss.chat_history.append({"question": typed_q.strip(), "answer": answer})
        status_ph.success("✅ Response generated & spoken!")

# ---- Continuous Voice Chat ----
def voice_chat_loop(pdf_path: str):
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 0.8
    speak_blocking("Voice chat mode activated. You can start speaking now.")
    ss.status = "✅ Voice chat running"
    status_ph.success(ss.status)

    try:
        while ss.chat_running:
            try:
                user_text = listen_once(r)
                ss.last_user = user_text
                heard_ph.success(f"**🧍 You said:** {user_text}")

                ss.status = "📚 Reading & generating answer..."
                status_ph.info(ss.status)
                ai_text = run_rag(pdf_path, user_text)

                ss.last_ai = ai_text
                reply_ph.markdown(f"**🤖 AI:** {ai_text}")
                ss.chat_history.append({"question": user_text, "answer": ai_text})

                ss.status = "🔊 Speaking..."
                status_ph.info(ss.status)
                speak_blocking(ai_text)

                ss.status = "✅ Ready for next question"
                status_ph.success(ss.status)

            except sr.UnknownValueError:
                status_ph.error("❌ Didn't catch that. Try again.")
                speak_blocking("Sorry, I didn't catch that.")
            except sr.WaitTimeoutError:
                status_ph.info("⏳ No voice detected. Listening again...")
            except Exception as e:
                status_ph.error(f"⚠️ Error: {e}")
                break
    finally:
        ss.chat_running = False
        status_ph.warning("🛑 Voice chat stopped.")
        speak_blocking("Voice chat mode stopped.")

# ---- Start / Stop Chat ----
col1, col2 = st.columns(2)
with col1:
    if st.button("🎧 Start Voice Chat Mode"):
        if not uploaded:
            st.warning("⚠️ Please upload a PDF first.")
        elif not ss.chat_running:
            tmp_pdf = "temp.pdf"
            with open(tmp_pdf, "wb") as f:
                f.write(uploaded.getbuffer())
            ss.chat_running = True
            threading.Thread(target=voice_chat_loop, args=(tmp_pdf,), daemon=True).start()
            st.success("✅ Voice Chat Mode started!")
        else:
            st.info("ℹ️ Voice Chat already running.")

with col2:
    if st.button("🛑 Stop Voice Chat"):
        if ss.chat_running:
            ss.chat_running = False
            st.warning("🛑 Stopping Voice Chat...")
        else:
            st.info("ℹ️ Voice Chat not running.")

# ---- Show last messages ----
if ss.last_user:
    heard_ph.success(f"**🧍 You said:** {ss.last_user}")
if ss.last_ai:
    reply_ph.markdown(f"**🤖 AI:** {ss.last_ai}")

# ---- History ----
if ss.chat_history:
    st.markdown("---")
    st.subheader("💬 Conversation History")
    for chat in reversed(ss.chat_history[-6:]):
        st.markdown(f"**🧍 You:** {chat['question']}")
        st.markdown(f"**🤖 AI:** {chat['answer']}")
        st.markdown("")

st.markdown("---")
st.caption("💡 Built by Chandan Kheto | Powered by LangChain RAG + FLAN-T5 Small + SpeechRecognition + pyttsx3")
