import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import matplotlib.pyplot as plt
import math

wymiary_ogrodu = 100

class Mysz:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self.path = [[self.x, self.y]]

    def movement(self):
        self.x += random.randrange(-1, 2)
        self.y += random.randrange(-1, 2)
        if not 0 < self.x < wymiary_ogrodu or not 0 < self.y < wymiary_ogrodu:
            self.x = self.path[-1][0]
            self.y = self.path[-1][1]
        self.path.append([self.x, self.y])

class Przecietniak:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = [[self.x, self.y]]

    def movement(self):
        self.x += random.randrange(-10, 11)
        self.y += random.randrange(-10, 11)
        if not 0 < self.x < wymiary_ogrodu or not 0 < self.y < wymiary_ogrodu:
            self.x = self.path[-1][0]
            self.y = self.path[-1][1]
        self.path.append([self.x, self.y])

    def spotkanie(self, mysz: Mysz):
        odleglosc = math.sqrt((self.x - mysz.x)**2 + (self.y - mysz.y)**2)
        if odleglosc < 4:
            mysz.x = mysz.path[0][0]
            mysz.y = mysz.path[0][1]
            mysz.path.append([mysz.x, mysz.y])
            return True

class Leniuch:
    def __init__(self, x, y):
        self.przegonienia = 0
        self.x = x
        self.y = y
        self.path = [[self.x, self.y]]

    def movement(self):
        self.x += random.randrange(-10, 11)
        self.y += random.randrange(-10, 11)
        if not 0 < self.x < wymiary_ogrodu or not 0 < self.y < wymiary_ogrodu:
            self.x = self.path[-1][0]
            self.y = self.path[-1][1]
        self.path.append([self.x, self.y])

    def spotkanie(self, mysz: Mysz):
        odleglosc = math.sqrt((self.x - mysz.x)**2 + (self.y - mysz.y)**2)
        if odleglosc < 4:
            zainteresowanie = random.choices([True, False],
                                             weights=[1 / (1 + math.e ** (-0.1 * self.przegonienia)), 1 - (1 / (1 + math.e ** (-0.1 * self.przegonienia)))]
                                             )
            if zainteresowanie:
                mysz.x = mysz.path[0][0]
                mysz.y = mysz.path[0][1]
                mysz.path.append([mysz.x, mysz.y])
                self.przegonienia += 1
            return True
        return False

class Kociak:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = [[self.x, self.y]]

    def movement(self):
        self.x += random.randrange(-5, 6)
        self.y += random.randrange(-5, 6)
        odleglosc_dom = math.sqrt((self.x - self.path[0][0]) ** 2 + (self.y - self.path[0][1]) ** 2)
        if not 0 < self.x < wymiary_ogrodu or not 0 < self.y < wymiary_ogrodu:
            self.x = self.path[-1][0]
            self.y = self.path[-1][1]
        if odleglosc_dom < 100:
            self.path.append([self.x, self.y])
        else:
            self.x = self.path[-1][0]
            self.y = self.path[-1][1]

    def spotkanie(self, mysz: Mysz):
        odleglosc = math.sqrt((self.x - mysz.x)**2 + (self.y - mysz.y)**2)
        if odleglosc < 4:
            odleglosc_dom = math.sqrt((self.x - self.path[0][0]) ** 2 + (self.y - self.path[0][1]) ** 2)
            if odleglosc_dom < 50:
                mysz.x = mysz.path[0][0]
                mysz.y = mysz.path[0][1]
                mysz.path.append([mysz.x, mysz.y])
            else:
                self.x = self.path[0][0]
                self.y = self.path[0][1]

def wczytywanie_pozycji(plik):
    dane = []
    for linia in plik:
        try:
            koordynaty = linia.strip().split()
            koordynaty = list(map(int, koordynaty))
            if any(x < 0 for x in koordynaty):
                raise ValueError
            if len(koordynaty) != 2:
                raise ValueError("Muszą zostać podane dokładnie dwie wartości x i y")
            dane.append(koordynaty)
        except ValueError:
            messagebox.showerror(f"Błąd w pliku '{plik.name}'",  f"Linia '{linia.strip()}', zwierze nie będzie na wykresie")
            messagebox.showerror("Błąd", "Położenia początkowe muszą być liczbami całkowitymi nieujemnymi i mieścić się w wymiarach ogrodu")
    return dane

def wczytaj_plik_z_danymi(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = wczytywanie_pozycji(plik)
        return dane
    except FileNotFoundError:
        messagebox.showerror("Błąd", f"Plik '{nazwa_pliku}' nie został znaleziony.")
        return []

kociaki_dane = wczytaj_plik_z_danymi('kociaki.txt')
leniuchy_dane = wczytaj_plik_z_danymi('leniuchy.txt')
przecietniaki_dane = wczytaj_plik_z_danymi("przecietniaki.txt")
myszy_dane = wczytaj_plik_z_danymi('myszy.txt')

def generowanie_zwierzat():
    myszy = []
    leniuchy = []
    przecietniaki = []
    kociaki = []

    for mysz in myszy_dane:
        myszy.append(Mysz(mysz[0], mysz[1]))
    for leniuch in leniuchy_dane:
        leniuchy.append(Leniuch(leniuch[0], leniuch[1]))
    for przecietniak in przecietniaki_dane:
        przecietniaki.append(Przecietniak(przecietniak[0], przecietniak[1]))
    for kociak in kociaki_dane:
        kociaki.append(Kociak(kociak[0], kociak[1]))
    return myszy, leniuchy, przecietniaki, kociaki

def tworz_dzien(n):
    myszy, leniuchy, przecietniaki, kociaki = generowanie_zwierzat()
    koty = [leniuchy, przecietniaki, kociaki]
    for _ in range(n):
        for mysz in myszy:
            mysz.movement()
            for grupa_kotow in koty:
                for kot in grupa_kotow:
                    kot.spotkanie(mysz)
        for grupa_kotow in koty:
            for kot in grupa_kotow:
                kot.movement()
                for mysz in myszy:
                    kot.spotkanie(mysz)
    return myszy, leniuchy, przecietniaki, kociaki

def rysuj(myszy, leniuchy, przecietniaki, kociaki, canvas_frame):
    fig, ax = plt.subplots(figsize=(6,5))

    for i, mysz in enumerate(myszy):
        mx_coords = [punkt[0] for punkt in mysz.path]
        my_coords = [punkt[1] for punkt in mysz.path]
        ax.plot(mx_coords, my_coords, color='green')
        if i == 0:
            ax.scatter(mysz.x, mysz.y, color='green', label = "Mysz")
        else:
            ax.scatter(mysz.x, mysz.y, color='green')


    for i, przecietniak in enumerate(przecietniaki):
        px_coords = [punkt[0] for punkt in przecietniak.path]
        py_coords = [punkt[1] for punkt in przecietniak.path]
        ax.plot(px_coords, py_coords, color='blue')
        if i == 0:
            ax.scatter(przecietniak.x, przecietniak.y, color='blue', label="Przecietniak")
        else:
            ax.scatter(przecietniak.x, przecietniak.y, color='blue')

    for i, leniuch in enumerate(leniuchy):
        lx_coords = [punkt[0] for punkt in leniuch.path]
        ly_coords = [punkt[1] for punkt in leniuch.path]
        ax.plot(lx_coords, ly_coords, color='red')
        if i == 0:
            ax.scatter(leniuch.x, leniuch.y, color='red', label = "Leniuch")
            i+=1
        else:
            ax.scatter(leniuch.x, leniuch.y, color='red')

    for i, kociak in enumerate(kociaki):
        kx_coords = [punkt[0] for punkt in kociak.path]
        ky_coords = [punkt[1] for punkt in kociak.path]
        ax.plot(kx_coords, ky_coords, color='orange')
        if i == 0:
            ax.scatter(kociak.x, kociak.y, color='orange', label = "Kociak")
        else:
            ax.scatter(kociak.x, kociak.y, color='orange')

    ax.set_xlim(0, wymiary_ogrodu)
    ax.set_ylim(0, wymiary_ogrodu)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), title="Legenda", ncol=2)
    fig.tight_layout()

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

def start_symulacji():
    try:
        global wymiary_ogrodu
        wymiary_ogrodu = int(entry_rozmiar.get())
        n_iteracji = int(entry_iteracje.get())
        if wymiary_ogrodu <= 0 or n_iteracji <= 0:
            raise ValueError("Wartości muszą być większe od 0.")
        myszy, leniuchy, przecietniaki, kociaki = tworz_dzien(n_iteracji)
        rysuj(myszy, leniuchy, przecietniaki, kociaki, canvas_frame)
    except ValueError as e:
        messagebox.showerror("Błąd", f"Nieprawidłowe dane wejściowe: {e}")

def reset_programu():
    entry_rozmiar.delete(0, tk.END)
    entry_rozmiar.insert(0, "100")
    entry_iteracje.delete(0, tk.END)
    entry_iteracje.insert(0, "10")
    for widget in canvas_frame.winfo_children():
        widget.destroy()

def opusc_program():
    root.destroy()

#GUI
root = tk.Tk()
root.title("Symulacja ogrodu")
root.resizable(True, True)

frame = tk.Frame(root)
frame.pack(pady=10)

label_rozmiar = tk.Label(frame, text="Rozmiar ogrodu:")
label_rozmiar.grid(row=0, column=0, padx=5, pady=5)

entry_rozmiar = tk.Entry(frame)
entry_rozmiar.grid(row=0, column=1, padx=5, pady=5)
entry_rozmiar.insert(0, "100")

label_iteracje = tk.Label(frame, text="Liczba iteracji:")
label_iteracje.grid(row=1, column=0, padx=5, pady=5)

entry_iteracje = tk.Entry(frame)
entry_iteracje.grid(row=1, column=1, padx=5, pady=5)
entry_iteracje.insert(0, "10")

button_start = tk.Button(frame, text="Start", command=start_symulacji)
button_start.grid(row=2, column=0, padx=5, pady=5)

button_reset = tk.Button(frame, text="Reset", command=reset_programu)
button_reset.grid(row=2, column=1, padx=5, pady=5)

button_wyjscie = tk.Button(frame, text="Wyjście", command=opusc_program)
button_wyjscie.grid(row=3, column=0, columnspan=2, pady=10)

canvas_frame = tk.Frame(root)
canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
