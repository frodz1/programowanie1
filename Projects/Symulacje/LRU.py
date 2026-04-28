

from collections import OrderedDict

# Funkcja realizująca algorytm LRU (Least Recently Used) za pomocą OrderedDict
def pageFaults(pages, capacity):
    # OrderedDict zapamiętuje kolejność dodanych elementów — kluczowe dla LRU
    cache = OrderedDict()
    page_faults = 0

    # Iteracja po kolejnych żądanych stronach
    for page in pages:
        # Jeżeli strona nie znajduje się w pamięci RAM — błąd strony
        if page not in cache:
            page_faults += 1
            # Jeżeli przekroczono pojemność pamięci, usuwamy najdawniej używaną stronę
            if len(cache) >= capacity:
                cache.popitem(last=False)  # `last=False` oznacza usunięcie pierwszego (najstarszego) elementu
        else:
            # Jeżeli strona już była w pamięci, przesuwamy ją na koniec jako ostatnio używaną
            cache.move_to_end(page)

        # Dodanie (lub ponowne dodanie) strony do pamięci RAM
        cache[page] = True

    # Zwrócenie całkowitej liczby błędów strony
    return page_faults


# Wczytanie stron z pliku tekstowego
with open("strony.txt", "r") as file:
    content = file.read()

# Zamiana wczytanej zawartości na listę liczb całkowitych (numery stron)
pages = list(map(int, content.split()))

# Pobranie od użytkownika pojemności pamięci RAM
while True:
    try:
        capacity = int(input("Podaj pojemność pamięci RAM: "))
        if capacity > 0:
            break
        else:
            print("Pamięć RAM musi być liczbą dodatnią. Spróbuj ponownie.")
    except ValueError:
        print("Nieprawidłowe dane. Wprowadź liczbę całkowitą dodatnią.")

# Wywołanie funkcji LRU i obliczenie liczby błędów strony
result = pageFaults(pages, capacity)

# Obliczenie współczynnika trafień (hit ratio)
pf_ratio = round((result / len(pages)) * 100, 2)

# Wyświetlenie wyników
print("Liczba błędów strony:", result)
print(f"Page fault ratio wynosi: {pf_ratio}%")





