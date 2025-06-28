import speech_recognition as sr
import pyttsx3
import whisper
import os

# Choose your transcription engine
USE_WHISPER = True
model = None

if USE_WHISPER:
    try:
        model = whisper.load_model("base")
    except Exception as e:
        print("Whisper load failed, falling back to basic STT:", e)
        USE_WHISPER = False

def listen_and_transcribe(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = r.listen(source, timeout=timeout)
        print("🔊 Processing...")

        if USE_WHISPER:
            try:
                with open("audio/temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                result = model.transcribe("audio/temp.wav")
                return result["text"]
            except Exception as e:
                print("Whisper failed:", e)
                return ""
        else:
            try:
                return r.recognize_google(audio)
            except sr.UnknownValueError:
                return ""
            except sr.RequestError as e:
                print("STT Error:", e)
                return ""

def speak(text, settings=None):
    engine = pyttsx3.init()
    voice_id = settings.get("default_voice", "female_en") if settings else None

    if voice_id:
        for voice in engine.getProperty('voices'):
            if voice_id.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.setProperty('rate', 175)
    engine.say(text)
    engine.runAndWait()
