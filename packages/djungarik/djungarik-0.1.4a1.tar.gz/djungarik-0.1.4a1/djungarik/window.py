import tkinter as tk

def create_window(title="Djungarik Window", width=300, height=300):
    window = tk.Tk()
    window.title(title)
    window.geometry(f"{width}x{height}")

    label = tk.Label(window, text="Hello, Djungarik!", font=("Arial", 14))
    label.pack(pady=20)

    button = tk.Button(window, text="Click me!", command=lambda: print("Button clicked!"))
    button.pack(pady=10)

    slider = tk.Scale(window, from_=0, to=100, orient="horizontal")
    slider.pack(pady=10)

    window.mainloop()
