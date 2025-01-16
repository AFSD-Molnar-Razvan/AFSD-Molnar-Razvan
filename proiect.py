import tkinter as tk
from tkinter import ttk
import random
import time

# Algoritmi de sortare

def bubble_sort(data, draw_data, delay):
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(data, ["red" if x == j or x == j+1 else "blue" for x in range(len(data))])
                time.sleep(delay)
    draw_data(data, ["green" for x in range(len(data))])

def insertion_sort(data, draw_data, delay):
    for i in range(1, len(data)):
        key = data[i]
        j = i-1
        while j >= 0 and key < data[j]:
            data[j+1] = data[j]
            j -= 1
            draw_data(data, ["red" if x == j or x == i else "blue" for x in range(len(data))])
            time.sleep(delay)
        data[j+1] = key
    draw_data(data, ["green" for x in range(len(data))])

# Funcția pentru desenarea datelor
def draw_data(data, colors):
    canvas.delete("all")
    c_width = 800
    c_height = 400
    x_width = c_width / (len(data) + 1)
    offset = 10
    spacing = 5
    normalized_data = [i / max(data) for i in data]

    for i, height in enumerate(normalized_data):
        x0 = i * x_width + offset + spacing
        y0 = c_height - height * 350
        x1 = (i + 1) * x_width + offset
        y1 = c_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i])
        canvas.create_text(x0 + 2, y0, anchor="sw", text=str(data[i]))

    root.update_idletasks()

# Generarea datelor random
def generate_data():
    global data
    data = [random.randint(1, 100) for _ in range(size.get())]
    draw_data(data, ["blue" for _ in range(len(data))])

# Funcția Start

def start_algorithm():
    global data
    if not data:
        return

    if algorithm_menu.get() == "Bubble Sort":
        bubble_sort(data, draw_data, speed.get())
    elif algorithm_menu.get() == "Insertion Sort":
        insertion_sort(data, draw_data, speed.get())

# Interfața grafică
root = tk.Tk()
root.title("Vizualizare Algoritmi de Sortare")
root.maxsize(900, 600)
root.config(bg="white")

data = []

# Frame pentru controale
ui_frame = tk.Frame(root, width=900, height=200, bg="grey")
ui_frame.grid(row=0, column=0, padx=10, pady=5)

canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.grid(row=1, column=0, padx=10, pady=5)

# Elemente UI
algorithm_label = tk.Label(ui_frame, text="Selectează Algoritmul:", bg="grey")
algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

algorithm_menu = ttk.Combobox(ui_frame, values=["Bubble Sort", "Insertion Sort"])
algorithm_menu.grid(row=0, column=1, padx=5, pady=5)
algorithm_menu.current(0)

speed_label = tk.Label(ui_frame, text="Selectează Viteza:", bg="grey")
speed_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

speed = tk.DoubleVar()
speed_slider = tk.Scale(ui_frame, from_=0.1, to=2.0, length=200, digits=2, resolution=0.1, orient="horizontal", variable=speed)
speed_slider.grid(row=1, column=1, padx=5, pady=5)

size_label = tk.Label(ui_frame, text="Număr Elemente:", bg="grey")
size_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

size = tk.IntVar()
size_slider = tk.Scale(ui_frame, from_=5, to=100, resolution=1, orient="horizontal", variable=size)
size_slider.grid(row=2, column=1, padx=5, pady=5)

generate_button = tk.Button(ui_frame, text="Generează Date", command=generate_data, bg="blue", fg="white")
generate_button.grid(row=0, column=2, padx=5, pady=5)

start_button = tk.Button(ui_frame, text="Start", command=start_algorithm, bg="green", fg="white")
start_button.grid(row=1, column=2, padx=5, pady=5)

exit_button = tk.Button(ui_frame, text="Ieșire", command=root.quit, bg="red", fg="white")
exit_button.grid(row=2, column=2, padx=5, pady=5)

root.mainloop()






