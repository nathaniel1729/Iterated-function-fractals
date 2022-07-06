from simpletk import Window
from PIL import Image, ImageTk
import numpy as np
import math
import random

res = 20
width, height = 1200, 800
ROW, COL = height // res, width // res
range_x, range_y = (-2, 2), (-1.5, 1.5)

root = Window(width, height, "Exploring the Mandelbrot Set")
canvas = root.add_canvas(height, height, 0, 0)

display = np.zeros((ROW, COL), dtype=np.uint8)
C = complex(1/3, 0)

def f(Z, C):
    return Z**2 + C

def calc_f(Z, C):
    infinity = 10

    escape_value = f(Z, C)
    for iteration in range(200):
        escape_value = f(escape_value, C)

        if abs(escape_value) > infinity:
            return iteration

    return 200

def map(num, num_lower, num_higher, new_lower, new_higher):
    return (num - num_lower) * (new_higher - new_lower) / (num_higher - num_lower) + new_lower

for j, row in enumerate(display):
    for i, col in enumerate(row):
        C_real = map(i, 0, COL - 1, range_x[0], range_x[1])
        C_imag = map(j, 0, ROW - 1, range_y[0], range_y[1])
        escape_value = calc_f(complex(0), complex(C_real, C_imag))
        display[j][i] = escape_value

canvas_display = np.zeros((height, height, 3), dtype=np.uint8)
for j, row in enumerate(display):
    for i, col in enumerate(row):
        escape_value = display[j][i]
        color = np.array([escape_value, escape_value, escape_value], dtype=np.uint8)
        for k in range(res):
            canvas_display[j*res + k][i*res:(i + 1)*res] = color

image = ImageTk.PhotoImage(image=Image.fromarray(canvas_display))
canvas.create_image(height//2, height//2, image=image)

root.mainloop()