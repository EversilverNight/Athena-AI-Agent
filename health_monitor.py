import psutil
import shutil
import platform
import os

def run_pc_health_check():
    print("🔍 Running PC health scan...")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    battery = psutil.sensors_battery() if hasattr(psutil, "sensors_battery") else None

    print(f"CPU Usage: {cpu}%")
    print(f"RAM Usage: {ram.percent}% of {round(ram.total / (1024 ** 3), 2)} GB")
    print(f"Disk Usage: {disk.percent}% of {round(disk.total / (1024 ** 3), 2)} GB")

    if battery:
        print(f"Battery: {battery.percent}% {'(Plugged in)' if battery.power_plugged else '(On battery)'}")

    if cpu > 85:
        print("⚠️ High CPU usage detected.")
    if ram.percent > 85:
        print("⚠️ High RAM usage detected.")
    if disk.percent > 90:
        print("⚠️ Disk space is running low.")

    print("✅ PC scan complete.")
