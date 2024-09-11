import tkinter as tk

def add_button(window, text="Button", command=None):
    button = tk.Button(window, text=text, command=command)
    button.pack()
    return button

def add_slider(window, from_=0, to=100):
    slider = tk.Scale(window, from_=from_, to=to)
    slider.pack()
    return slider

def add_text(window, text="Hello!"):
    label = tk.Label(window, text=text)
    label.pack()
    return label
