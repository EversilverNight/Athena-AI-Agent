import time
from config.settings import load_settings
from config.persona import get_persona_prompt
from model_switcher import SmartModelRouter
from voice_interface import listen_and_transcribe, speak
from health_monitor import run_pc_health_check
from emotion_tracker import analyze_emotion
from learning_tracker import update_behavior_model

def main():
    print("🚀 Athena is booting...")
    settings = load_settings()
    persona = get_persona_prompt()
    model_router = SmartModelRouter(settings)

    speak("Hello. Athena is now online.", settings)

    while True:
        try:
            text = listen_and_transcribe()
            if not text:
                continue

            print(f"🧠 You said: {text}")

            if "shutdown" in text.lower():
                speak("Shutting down. Goodbye.", settings)
                break

            # Emotion check
            emotion = analyze_emotion(text)
            if emotion:
                print(f"🧘 Emotional tone: {emotion}")

            # Health scan command
            if "check system" in text.lower() or "scan pc" in text.lower():
                speak("Running system check.", settings)
                run_pc_health_check()
                continue

            # Learning log
            update_behavior_model(text)

            # Model reasoning
            llm = model_router.get_model()
            response = llm(f"{persona}\nUser: {text}\nAthena:")
            print(f"Athena: {response}")
            speak(response, settings)

        except KeyboardInterrupt:
            speak("Shutting down due to interrupt.")
            break
        except Exception as e:
            print("❌ Error:", e)
            speak("Sorry, something went wrong.")

if __name__ == "__main__":
    main()
