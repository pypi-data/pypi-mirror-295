import tkinter as tk

class DjungarikWidgets:
    def __init__(self, window):
        self.window = window

    def create_label(self, text, font=("Arial", 12), padx=10, pady=10):
        label = tk.Label(self.window, text=text, font=font)
        label.pack(padx=padx, pady=pady)
        return label

    def create_button(self, text, command=None, padx=10, pady=10):
        button = tk.Button(self.window, text=text, command=command)
        button.pack(padx=padx, pady=pady)
        return button

    def create_slider(self, from_=0, to=100, orient="horizontal", padx=10, pady=10):
        slider = tk.Scale(self.window, from_=from_, to=to, orient=orient)
        slider.pack(padx=padx, pady=pady)
        return slider

    def create_entry(self, placeholder_text="", padx=10, pady=10):
        entry = tk.Entry(self.window)
        entry.insert(0, placeholder_text)
        entry.pack(padx=padx, pady=pady)
        return entry

    def create_checkbox(self, text, padx=10, pady=10):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(self.window, text=text, variable=var)
        checkbox.pack(padx=padx, pady=pady)
        return checkbox, var
