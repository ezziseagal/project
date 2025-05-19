# Zautomatyzowany monitoring konfiguracji urządzeń Cisco

## Opis projektu
Celem projektu jest stworzenie lekkiego, zautomatyzowanego systemu monitorowania konfiguracji urządzeń sieciowych Cisco, który pozwala na:
- Wczesne wykrywanie nieautoryzowanych zmian konfiguracyjnych,
- Rejestrowanie tych zmian w systemie kontroli wersji (Git),
- Traktowanie zmian jako potencjalnych incydentów bezpieczeństwa,
- Automatyzację procesów w duchu DevNet i DevSecOps.

## Wymagania
- Python 3.8+
- Biblioteki: `netmiko`, `pyATS`, `genie`
- System kontroli wersji: Git

## Instrukcja uruchomienia
1. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```
2. Uruchom skrypt monitorujący:
   ```bash
   python config_monitor.py
   ```
3. Aby uruchomić testy:
   ```bash
   python tests/test_config_stability.py
   ```

## Struktura projektu
- `config_monitor.py`: Główny skrypt monitorujący konfiguracje.
- `tests/`: Pliki testowe do weryfikacji stabilności konfiguracji.
- `configs/`: Katalog przechowujący konfiguracje urządzeń.
- `logs/`: Katalog przechowujący logi zmian konfiguracji.