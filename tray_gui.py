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

# Load config
settings = load_settings()
persona = get_persona_prompt()
model_router = SmartModelRouter(settings)

# Load icon
def get_icon_image():
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    try:
        return Image.open(icon_path)
    except Exception as e:
        print("❌ Failed to load icon:", e)
        return Image.new('RGB', (64, 64), color=(0, 0, 0))

# Voice assistant
def start_voice_mode():
    speak("Listening...", settings)
    text = listen_and_transcribe()
    if text:
        print(f"🗣️ Heard: {text}")
        llm = model_router.get_model()
        response = llm(f"{persona}\nUser: {text}\nAthena:")
        print(f"Athena: {response}")
        speak(response, settings)

# Manual toggle between models
def toggle_mode():
    model_router.toggle_manual_mode()
    speak(f"Switched to {model_router.current_model} mode.", settings)

# Run health scan
def run_health_check():
    speak("Running a system scan now.", settings)
    run_pc_health_check()

# Exit app
def exit_app(icon, item):
    icon.stop()
    speak("Tray closed. Athena signing off.", settings)
    os._exit(0)

# Setup tray
def setup_tray():
    icon = pystray.Icon("Athena")
    icon.icon = get_icon_image()
    icon.menu = (
        item("🎤 Speak", lambda: threading.Thread(target=start_voice_mode).start()),
        item("🔁 Switch Model", lambda: threading.Thread(target=toggle_mode).start()),
        item("🛡️ Health Check", lambda: threading.Thread(target=run_health_check).start()),
        item("❌ Exit", exit_app)
    )
    icon.title = "Athena"
    icon.run()

if __name__ == "__main__":
    setup_tray()
