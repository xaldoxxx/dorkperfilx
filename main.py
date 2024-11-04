# main.py

import tkinter as tk
from vista import Vista
from controlador import Controlador

def main():
    root = tk.Tk()
    vista = Vista(root)
    Controlador(vista)
    root.mainloop()

if __name__ == '__main__':
    main()