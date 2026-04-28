

from collections import deque

# Klasa reprezentująca pojedynczy proces
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid                        # ID procesu (np. 1, 2, 3)
        self.arrival = arrival                # Czas przybycia
        self.burst = burst                    # Całkowity czas potrzebny na wykonanie
        self.remaining_time = burst           # Pozostały czas wykonania (do zmniejszania w czasie RR)
        self.completion_time = 0              # Czas zakończenia procesu
        self.tat = 0                          # Turnaround Time = completion - arrival
        self.wt = 0                           # Waiting Time = turnaround - burst
        self.started = False                  # Czy proces już zaczął być wykonywany (niewykorzystywane tutaj)

# Wczytywanie danych z pliku
tablica = []
with open("procesy.txt", "r") as file:
    dane = file.readlines()

process_list = []
for i, line in enumerate(dane):
    arrival, burst = map(int, line.strip().split())
    process_list.append(Process(i + 1, arrival, burst))

n = len(process_list)  # Liczba procesów

# Pobranie kwantu czasu od użytkownika
while True:
    try:
        time_quantum = int(input("Podaj kwant czasu (liczba dodatnia): "))
        if time_quantum > 0:
            break
        else:
            print("Kwant czasu musi być liczbą dodatnią. Spróbuj ponownie.")
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę całkowitą dodatnią.")


# Sortujemy procesy według czasu przybycia
process_list.sort(key=lambda p: p.arrival)

# Kolejka gotowości
ready_queue = deque()
current_time = 0
completed = 0
avg_wt = 0  # Suma czasów oczekiwania
avg_tat = 0  # Suma turnaround times
i = 0  # Indeks dla dodawania nowych procesów do kolejki

# Główna pętla wykonująca algorytm Round Robin
while completed < n:
    # Dodaj procesy do kolejki, jeśli już przybyły
    while i < n and process_list[i].arrival <= current_time:
        ready_queue.append(process_list[i])
        i += 1

    if ready_queue:
        process = ready_queue.popleft()

        # Wykonanie procesu przez minimalny z (kwant, czas pozostały)
        exec_time = min(time_quantum, process.remaining_time)
        current_time += exec_time
        process.remaining_time -= exec_time

        # Dodaj nowo przybyłe procesy do kolejki
        while i < n and process_list[i].arrival <= current_time:
            ready_queue.append(process_list[i])
            i += 1

        if process.remaining_time == 0:
            # Proces zakończony
            process.completion_time = current_time
            process.tat = process.completion_time - process.arrival
            process.wt = process.tat - process.burst
            avg_wt += process.wt
            avg_tat += process.tat
            completed += 1
        else:
            # Jeżeli proces się nie zakończył, wraca na koniec kolejki
            ready_queue.append(process)
    else:
        # Jeśli żadnego procesu nie ma w kolejce, przeskakujemy czas
        current_time += 1

# WYDRUK WYNIKÓW
print("\nProcess | Arrival | Burst | Completion | TurnAround | Waiting")
for p in sorted(process_list, key=lambda p: p.pid):
    print(f"{p.pid:^7} | {p.arrival:^7} | {p.burst:^5} | {p.completion_time:^10} | {p.tat:^10} | {p.wt:^7}")

print(f"\nŚredni czas oczekiwania: {avg_wt / n:.2f}")
print(f"Średni czas realizacji (TAT): {avg_tat / n:.2f}")


