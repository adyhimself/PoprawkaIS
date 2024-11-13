# Funkcjonalność

**PoprawkaIS** to system składający się z dwóch aplikacji webowych:

- **Main App** jest główną aplikacją WWW, która pozwala dodawać, usuwać, modyfikować i wyświetlać listę trenerów.
  Dodatkowo aplikacja pozwala wyświetlić ostatnie 20 logów na temat akcji użytkownika, który korzystał z aplikacji,
  uruchamiana na porcie 8000.
- **Tracking** jest usługą REST-ową, która przyjmuje eventy i zwraca logi na temat akcji użytkownika, których dokonał na
  stronach aplikacji głównej, uruchamiana na porcie 8001.

System został stworzony przy użyciu frameworka Django.

# Instalacja

Poniżej znajduje się instrukcja, która pozwoli na lokalne uruchomienie obu aplikacji.
Upewnij się, że masz zainstalowany Python3.

**1. Sklonuj repozytorium**

```bash
git clone https://github.com/adyhimself/PoprawkaIS
cd PoprawkaIS
```

**2. Stwórz wirtualne środowisko**

```bash
python3 -m venv venv
source venv/bin/activate #dla Windowsa 'venv\scripts\activate'
```

**3. Zainstaluj requirements.txt**

```bash
pip install -r requirements.txt
```

**4. Wykonaj migracje**

```bash
python main_app/manage.py migrate
python tracking_app/manage.py migrate
```

**5. Zbierz pliki statyczne (opcjonalne dla środowiska deweloperskiego)**

```bash
python main_app/manage.py collectstatic
python tracking_app/manage.py collectstatic
```

# Uruchamianie aplikacji

Uruchom serwer dla `main_app` na porcie 8000, używając poniższego polecenia:

```bash
python main_app/manage.py runserver 8000
```

Aplikacja `main_app` będzie dostępna pod adresem http://127.0.0.1:8000/

Uruchom serwer dla `tracking_app` na porcie 8001, używając poniższego polecenia:

```bash
python tracking_app/manage.py runserver 8001
```

Kluczwe endpointy dla tracking_app:

- Log Event (POST): http://127.0.0.1:8001/tracking/event/
- Pobieranie Logów (GET): http://127.0.0.1:8001/tracking/logs/

# Testowanie

Aby zweryfikować działanie obu aplikacji, możnesz uruchomić załączone testy.

Dla `main_app`:

```bash
python main_app/manage.py test trainers
```

Dla `tracking_app`:

```bash
python tracking_app/manage.py test tracking
```
