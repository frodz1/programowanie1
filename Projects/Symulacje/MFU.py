# Funkcja implementująca algorytm zastępowania stron MFU (Most Frequently Used)
def MFU_replacement(strony, pojemnosc):
    cache = []  # Lista reprezentująca pamięć podręczną (RAM)
    frequency = {}  # Słownik przechowujący częstotliwość odwiedzin każdej strony
    page_faults = 0  # Licznik błędów strony (page faults)

    # Iteracja po wszystkich żądanych stronach
    for page in strony:
        if page not in cache:
            # Jeśli strona nie znajduje się w pamięci – wystąpił błąd strony
            page_faults += 1
            if len(cache) < pojemnosc:
                # Jeśli jest jeszcze miejsce w pamięci – dodaj stronę
                cache.append(page)
            else:
                # W przeciwnym razie znajdź stronę najczęściej używaną (MFU) i ją usuń
                mfu_page = max(cache, key=lambda p: frequency.get(p, 0))
                cache.remove(mfu_page)
                del frequency[mfu_page]
                # Dodaj nową stronę do pamięci
                cache.append(page)
            # Zainicjuj częstotliwość dla nowej strony
            frequency[page] = 1
        else:
            # Jeśli strona już jest w pamięci – zwiększ jej częstotliwość
            frequency[page] += 1

    # Zwróć całkowitą liczbę błędów strony
    return page_faults


# Wczytanie stron z pliku tekstowego
with open("strony.txt", "r") as file:
    content = file.read()

# Konwersja danych z pliku do listy liczb całkowitych (stron)
pages = list(map(int, content.strip().split()))

# Pobranie pojemności RAM od użytkownika
while True:
    try:
        capacity = int(input("Podaj pojemność pamięci RAM: "))
        if capacity > 0:
            break
        else:
            print("Pamięć RAM musi być liczbą dodatnią. Spróbuj ponownie.")
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę całkowitą dodatnią.")

# Wywołanie funkcji MFU i obliczenie liczby błędów strony
result = MFU_replacement(pages, capacity)

# Obliczenie współczynnika błędów strony (page fault ratio)
pf_ratio = round((result / len(pages)) * 100, 2)

# Wyświetlenie wyników
print("Liczba błędów strony:", result)
print(f"Page fault ratio wynosi: {pf_ratio}%")




