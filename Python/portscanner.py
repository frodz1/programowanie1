import socket

# Funkcja skanująca porty w podanym zakresie dla danego hosta/IP
def scan_ports(host_port, start_port, end_port):
    print(f"Skanuję porty {host_port}...")
    # Lista przechowująca informacje o otwartych portach
    open_ports = []

    # Iterujemy po wszystkich portach w podanym zakresie
    for port in range(start_port, end_port + 1):
        # Tworzenie gniazda TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Ustawienie limitu czasu połączenia na 1 sekundę
        sock.settimeout(1)

        # Próba połączenia z danym portem - udane połączenie zwraca 0
        result = sock.connect_ex((host_port, port))

        if result == 0:
            print(f"Port {port} is open")
            # Dodanie do listy otwartych portów
            open_ports.append(port)
        # Zamknięcie połączenia
        sock.close()

    # Jeżeli nie znaleziono żadnych otwartych portów
    if not open_ports:
        print("Nie znaleziono otwartych portów.")

# Pobranie danych od użytkownika
target_hosts = input("Wprowadź adres IP: ")
first_port = int(input("Podaj port początkowy: "))
last_port = int(input("Podaj port końcowy: "))

# Wywołanie fukcji
scan_ports(target_hosts, first_port, last_port)
