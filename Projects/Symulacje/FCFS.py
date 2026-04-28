print("FIRST COME FIRST SERVE SCHEDULLING")

# Lista przechowująca obiekty reprezentujące procesy
process_list = []


# Klasa reprezentująca proces
class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid  # Identyfikator procesu (np. P1, P2, ...)
        self.arrival = arrival  # Czas przybycia procesu
        self.burst = burst  # Czas wykonania procesu (czas CPU)
        self.et = 0  # Czas zakończenia (exit time)
        self.tat = 0  # Czas cyklu (Turnaround Time = Exit - Arrival)
        self.wt = 0  # Czas oczekiwania (Waiting Time = Turnaround - Burst)


# Wczytywanie danych procesów z pliku "procesy.txt"
with open("minprocesy.txt", "r") as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        parts = line.strip().split()  # Dzieli wiersz na części (arrival, burst)
        arrival, burst = map(int, parts)  # Zamienia stringi na inty
        pid = f"P{i + 1}"  # Tworzy nazwę procesu (np. P1, P2...)
        process_list.append(Process(pid, arrival, burst))  # Dodaje proces do listy

# Sortujemy procesy po czasie przybycia (zgodnie z FCFS)
process_list.sort(key=lambda process: process.arrival)

n = len(process_list)  # Liczba procesów

# Obliczanie Exit Time (et), Turnaround Time (tat) i Waiting Time (wt) dla każdego procesu
for i in range(n):
    if i == 0:
        # Pierwszy proces zaczyna od swojego czasu przybycia
        process_list[i].et = process_list[i].arrival + process_list[i].burst
    else:
        # Proces startuje po poprzednim lub po swoim przybyciu (którekolwiek później)
        start = max(process_list[i].arrival, process_list[i - 1].et)
        process_list[i].et = start + process_list[i].burst

    # Obliczenie TAT i WT
    process_list[i].tat = process_list[i].et - process_list[i].arrival
    process_list[i].wt = process_list[i].tat - process_list[i].burst

# Średni czas oczekiwania
avg_WT = sum(p.wt for p in process_list) / n
avg_Tat = sum(p.tat for p in process_list) / n

# Wyświetlenie wyników
print("\nProcess | Arrival | Burst | Exit | TurnAround | Waiting")
for p in process_list:
    print(f"{p.pid:^8} | {p.arrival:^7} | {p.burst:^5} | {p.et:^4} | {p.tat:^10} | {p.wt:^7}")

print("\nAverage Waiting Time: ", avg_WT)
print("\nAverage Turnaround Time: ", avg_Tat)



