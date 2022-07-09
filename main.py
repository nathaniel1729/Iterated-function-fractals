from simpletk import Window
from PIL import Image, ImageTk
import numpy as np
import math
import random

res = 4
width, height = 1200, 800
ROW, COL = height // res, height // res
zoom, center = 2, (-0.5, 0)
range_x, range_y = (center[0] - zoom//2, center[0] + zoom//2), (center[1] - zoom//2, center[1] + zoom//2)

root = Window(width, height, "Exploring the Mandelbrot Set")
canvas = root.add_canvas(height, height, 0, 0)

display = np.zeros((ROW, COL), dtype=np.uint8)
canvas_display = np.zeros((height, height, 3), dtype=np.uint8)
image = ImageTk.PhotoImage(image=Image.fromarray(canvas_display))

def map_range(num, num_lower, num_higher, new_lower, new_higher):
    return (num - num_lower) * (new_higher - new_lower) / (num_higher - num_lower) + new_lower

def translate_display(event):
    global zoom, center, range_x, range_y

    x = map_range(event.x, 0, height, range_x[0], range_x[1])
    y = map_range(event.y, 0, height, range_y[0], range_y[1])

    center = (x, y)
    range_x, range_y = (center[0] - zoom // 2, center[0] + zoom // 2), (center[1] - zoom // 2, center[1] + zoom // 2)

    _display = calculate_escape_values(display)
    image = colorize_display(_display)
    # _image = ImageTk.getimage(image)
    # _image.save("screenshot.png")

def f(Z, C):
    return Z**2 + C

def calc_f(row_col_elem):
    (row, col), elem = row_col_elem
    C_real = map_range(col, 0, COL - 1, range_x[0], range_x[1])
    C_imag = map_range(row, 0, ROW - 1, range_y[0], range_y[1])
    Z, C = complex(0, 0), complex(C_real, C_imag)
    infinity = 10

    escape_value = f(Z, C)
    for iteration in range(200):
        escape_value = f(escape_value, C)

        if abs(escape_value) > infinity:
            return iteration

    return 200

def calculate_escape_values(display):
    return np.reshape(list(map(calc_f, np.ndenumerate(display))), (ROW, COL))

def colorize_display(display):
    global image, canvas_display

    for j, row in enumerate(display):
        for i, col in enumerate(row):
            escape_value = display[j][i]
            color = np.array([escape_value, escape_value, escape_value], dtype=np.uint8)
            for k in range(res):
                canvas_display[j*res + k][i*res:(i + 1)*res] = color

    image = ImageTk.PhotoImage(image=Image.fromarray(canvas_display))
    canvas.delete("all")
    canvas.create_image(height // 2, height // 2, image=image)

display = calculate_escape_values(display)
colorize_display(display)

canvas.bind("<Button>", translate_display)
root.mainloop()