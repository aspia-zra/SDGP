import tkinter as tk
from gui.sidebar import create_sidebar
from gui.payments_page import create_payments_page


class MainWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Paragon Apartments")
        self.root.geometry("1100x650")

        create_sidebar(self.root)

        main_area = tk.Frame(self.root)
        main_area.pack(side="right", fill="both", expand=True)

        create_payments_page(main_area)

    def run(self):

        self.root.mainloop()