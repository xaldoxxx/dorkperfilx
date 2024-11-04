# vista.py

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class Vista:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Perfiles")
        self.root.geometry("600x400")

        # Campo de entrada para el correo electrónico
        tk.Label(root, text="Correo electrónico:").pack(pady=5)
        self.entrada_correo = tk.Entry(root, width=50)
        self.entrada_correo.pack(pady=5)

        # Botón de selección de archivo de salida
        tk.Button(root, text="Seleccionar archivo de salida", command=self.seleccionar_archivo_salida).pack(pady=5)

        # Botón para activar modo verbose
        self.verbose_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Modo Verbose", variable=self.verbose_var).pack(pady=5)

        # Área de visualización de resultados
        tk.Label(root, text="Resultados:").pack(pady=5)
        self.resultados_texto = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
        self.resultados_texto.pack(pady=5)

        # Botones de búsqueda y salida
        tk.Button(root, text="Buscar Perfiles", command=self.buscar_perfiles).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(root, text="Salir", command=root.quit).pack(side=tk.RIGHT, padx=5, pady=5)

    def seleccionar_archivo_salida(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo de salida.
        """
        archivo_salida = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if archivo_salida:
            self.archivo_salida = archivo_salida
        else:
            self.archivo_salida = None

    def mostrar_resultados(self, texto):
        """
        Muestra los resultados en el área de texto.
        """
        self.resultados_texto.delete(1.0, tk.END)
        self.resultados_texto.insert(tk.END, texto)

    def obtener_datos(self):
        """
        Devuelve los datos ingresados por el usuario.
        """
        correo = self.entrada_correo.get()
        verbose = self.verbose_var.get()
        return correo, verbose, getattr(self, 'archivo_salida', None)

    def buscar_perfiles(self):
        """
        Llama al método buscar_perfiles del controlador.
        """
        messagebox.showinfo("Iniciar búsqueda", "Iniciando búsqueda de perfiles. Esto puede tardar unos segundos.")
