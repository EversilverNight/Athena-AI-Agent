import psutil
import subprocess
import json
from langchain_community.llms import Ollama

class SmartModelRouter:
    def __init__(self, settings):
        self.settings = settings
        self.manual_override = False
        self.current_model = settings["heavy_model"]
        self.model_registry = self._scan_installed_models()

    def _scan_installed_models(self):
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")[1:]
            registry = {}
            for line in lines:
                parts = line.split()
                if len(parts) >= 2:
                    name, size = parts[0], parts[1]
                    registry[name] = {
                        "name": name,
                        "size": self._parse_size(size),
                        "role": self._infer_model_role(name)
                    }
            return registry
        except Exception as e:
            print("Model scan failed:", e)
            return {}

    def _parse_size(self, size_str):
        try:
            if "GB" in size_str:
                return float(size_str.replace("GB", "").strip()) * 1024
            elif "MB" in size_str:
                return float(size_str.replace("MB", "").strip())
            else:
                return 9999  # Unknown size
        except:
            return 9999

    def _infer_model_role(self, name):
        name = name.lower()
        if "dolphin" in name or "mixtral" in name or "llama3" in name:
            return "heavy"
        elif "mistral" in name or "phi" in name or "gemma" in name:
            return "light"
        else:
            return "unknown"

    def get_model(self):
        if not self.manual_override:
            self._auto_select_best_model()
        return Ollama(model=self.current_model)

    def toggle_manual_mode(self):
        self.manual_override = not self.manual_override
        if self.manual_override:
            # Toggle between smallest and largest
            lightest = min(self.model_registry.values(), key=lambda x: x["size"])
            heaviest = max(self.model_registry.values(), key=lambda x: x["size"])
            self.current_model = (
                lightest["name"]
                if self.current_model == heaviest["name"]
                else heaviest["name"]
            )

    def _auto_select_best_model(self):
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent(interval=1)

        best_model = self.current_model

        if ram > 80 or cpu > 75:
            # Find the lightest model
            candidates = [m for m in self.model_registry.values() if m["role"] == "light"]
            if candidates:
                best_model = min(candidates, key=lambda x: x["size"])["name"]
        elif ram < 60 and cpu < 50:
            # Pick most capable model
            candidates = [m for m in self.model_registry.values() if m["role"] == "heavy"]
            if candidates:
                best_model = max(candidates, key=lambda x: x["size"])["name"]

        if best_model != self.current_model:
            self._notify_switch(best_model)
            self.current_model = best_model

    def _notify_switch(self, new_model):
        if self.settings.get("notify_on_model_switch", True):
            from voice_interface import speak
            speak(f"Switching to {new_model} based on system status.", self.settings)
