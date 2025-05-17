import os
import difflib
from datetime import datetime
from netmiko import ConnectHandler
import subprocess

# === KONFIGURACJA ===
DEVICE_IPS = ["192.168.56.128", "192.168.56.129"]  # Dodaj tu kolejne adresy
USERNAME = "cisco"
PASSWORD = "cisco123!"
DEVICE_TYPE = "cisco_ios"

CONFIG_DIR = "configs"
LOG_DIR = "logs"

# === FUNKCJE ===
def ensure_dirs():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)


def get_device_config(device):
    print(f"[*] Łączenie z {device['host']}...")
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command("show running-config")
        connection.disconnect()
        print("[*] Konfiguracja pobrana.")
        return output
    except Exception as e:
        print(f"[!] Błąd połączenia z {device['host']}: {e}")
        return None


def load_previous_config(hostname):
    path = os.path.join(CONFIG_DIR, f"{hostname}.cfg")
    if not os.path.exists(path):
        return ""
    with open(path, "r") as f:
        return f.read()


def save_current_config(config, hostname):
    path = os.path.join(CONFIG_DIR, f"{hostname}.cfg")
    with open(path, "w") as f:
        f.write(config)
    print(f"[*] Konfiguracja zapisana do {path}")


def log_diff(current, previous, hostname):
    diff = list(difflib.unified_diff(
        previous.splitlines(), current.splitlines(),
        fromfile="previous", tofile="current", lineterm=""
    ))
    if diff:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(LOG_DIR, f"{hostname}_diff_{now}.log")
        with open(log_path, "w") as f:
            f.write("\n".join(diff))
        print(f"[!] Wykryto zmiany! Różnice zapisane w: {log_path}")
        return True
    else:
        print("[*] Brak zmian w konfiguracji.")
        return False


def commit_to_git():
    try:
        subprocess.run(["git", "add", CONFIG_DIR], check=True)
        subprocess.run(["git", "commit", "-m", f"Backup {datetime.now().isoformat()}"], check=True)
        print("[*] Zmiany zatwierdzone w repozytorium Git.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Błąd przy commitowaniu do Git: {e}")


# === GŁÓWNA LOGIKA ===
def main():
    ensure_dirs()

    devices = [
        {
            "device_type": DEVICE_TYPE,
            "host": ip,
            "username": USERNAME,
            "password": PASSWORD
        }
        for ip in DEVICE_IPS
    ]

    any_changes = False

    for device in devices:
        hostname = device["host"].replace(".", "_")  # Alternatywnie: użyj komendy "show hostname"
        current_config = get_device_config(device)

        if current_config is None:
            continue  # Przejdź do kolejnego urządzenia jeśli wystąpił błąd

        previous_config = load_previous_config(hostname)

        if log_diff(current_config, previous_config, hostname):
            save_current_config(current_config, hostname)
            any_changes = True

    if any_changes:
        commit_to_git()


if __name__ == "__main__":
    main()
