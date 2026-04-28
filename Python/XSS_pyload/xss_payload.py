from selenium import webdriver
import time

# Otwieranie pliku z listą payloadów XSS i wczytanie ich do listy
with open("xss-payload-list.txt", 'r', encoding="utf-8") as f:
    payload = f.readlines()

# Uruchomienie przeglądarki Firefox przez Selenium WebDriver
driver = webdriver.Firefox()

# Iteracja przez każdy payload wczytany z pliku
for lane in payload:
    lane = lane.strip()  # Usunięcie znaków nowej linii lub spacji na końcu

    try:
        # Otwarcie strony z podanym payloadem jako parametr zapytania (symulacja ataku XSS)
        driver.get("https://demo.owasp-juice.shop/#/search?q=" + str(lane))
        time.sleep(3)  # Poczekanie na ewentualne załadowanie strony i pojawienie się alertu

        # Przełączenie się do okienka alertu
        alert = driver.switch_to.alert

        if alert is not None:
            # Zamknięcie alertu
            alert.accept()
            print(f"Występuje podatność na XSS: {lane}.")
            # Przerywamy testowanie po znalezieniu działającego payloadu
            break

    except:
        # Jeśli nie wystąpi alert, przechodzimy do kolejnego payloadu
        print(f"Payload nie zadziałał: {lane}")

driver.quit()
