import tkinter as tk

class Window:
    def __init__(self, width, height, title=None):
        self.root = tk.Tk()

        self.root.title(title)
        self.root.geometry(f"{width}x{height}")

    def mainloop(self):
        self.root.mainloop()

    def add_canvas(self, width, height, row, col, row_span=1, col_span=1, background=None):
        label = tk.Label(self.root)
        label.grid(row=row, column=col, rowspan=row_span, columnspan=col_span)
        canvas = tk.Canvas(label, width=width, height=height, highlightthickness=0, background=background)
        canvas.pack()

        return canvas

    def add_button(self, width, height, row, col, text, command=None, row_span=1, col_span=1):
        button = tk.Button(self.root, width=width, height=height, text=text, command=command)
        button.grid(row=row, column=col, rowspan=row_span, columnspan=col_span)

        return button

    def add_label(self, row, col, text=None, image=None, row_span=1, col_span=1):
        label = tk.Label(self.root, text=text)
        label.grid(row=row, column=col, rowspan=row_span, columnspan=col_span)

        return label

    def image(self, width=None, height=None, file=None, data=None):
        return tk.PhotoImage(width=width, height=height, file=file, data=data)