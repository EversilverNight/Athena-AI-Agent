import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import os
import subprocess
from voice_interface import listen_and_transcribe, speak
from model_switcher import SmartModelRouter
from health_monitor import run_pc_health_check
from config.settings import load_settings
from config.persona import get_persona_prompt

settings = load_settings()
persona = get_persona_prompt()
model_router = SmartModelRouter(settings)

# Tray icon image (you can replace this with any 64x64 image later)
ICON_PATH = "assets/icon.png"

def start_voice_mode():
    speak("Listening...", settings)
    text = listen_and_transcribe()
    if text:
        print(f"🗣️ Heard: {text}")
        llm = model_router.get_model()
        response = llm(f"{persona}\nUser: {text}\nAthena:")
        print(f"Athena: {response}")
        speak(response, settings)

def toggle_mode():
    model_router.toggle_manual_mode()
    speak(f"Switched to {model_router.current_model} mode.", settings)

def run_health_check():
    speak("Running a system scan now.", settings)
    run_pc_health_check()

def exit_app(icon, item):
    icon.stop()
    speak("Tray closed. Athena signing off.", settings)
    os._exit(0)

def setup_tray():
    icon = pystray.Icon("Athena")
    try:
        image = Image.open(ICON_PATH)
    except:
        image = Image.new('RGB', (64, 64), color=(0, 0, 0))

    icon.icon = image
    icon.menu = (
        item("🎤 Speak", lambda: threading.Thread(target=start_voice_mode).start()),
        item("🔁 Switch Mode", lambda: threading.Thread(target=toggle_mode).start()),
        item("🛡️ Health Check", lambda: threading.Thread(target=run_health_check).start()),
        item("❌ Exit", exit_app)
    )
    icon.run()

if __name__ == "__main__":
    setup_tray()
