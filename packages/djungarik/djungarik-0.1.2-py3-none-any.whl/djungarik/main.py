import tkinter as tk

class DjungarikApp:
    def __init__(self, width=300, height=300, title="Djungarik"):
        self.window = tk.Tk()
        self.window.geometry(f"{width}x{height}")
        self.window.title(title)

        self.label = tk.Label(self.window, text="Welcome to Djungarik!", cursor="pointer")
        self.label.pack()

        self.button = tk.Button(self.window, text="Click Me", command=self.on_click, cursor="pointer")
        self.button.pack()

        self.slider = tk.Scale(self.window, from_=0, to=100, orient="horizontal")
        self.slider.pack()

        self.textbox = tk.Entry(self.window)
        self.textbox.pack()

    def on_click(self):
        print(f"Button clicked! Slider value: {self.slider.get()}, Text: {self.textbox.get()}")

    def run(self):
        self.window.mainloop()

def create_window(width=300, height=300, title="Djungarik"):
    app = DjungarikApp(width, height, title)
    app.run()
