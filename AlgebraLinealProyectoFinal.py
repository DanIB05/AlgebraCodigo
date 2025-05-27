import numpy as np
import math
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas, Scrollbar

class AlgebraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra Lineal Avanzada")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', font=('Segoe UI', 10), padding=8, background='#4CAF50', foreground='white')
        self.style.map('TButton', background=[('active', '#45a049')])
        self.style.configure('TLabel', font=('Segoe UI', 10), background='#f0f0f0')
        self.style.configure('TEntry', font=('Segoe UI', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), background='#f0f0f0', foreground='#333333')

        self.matrix1_shape = (0, 0)
        self.matrix2_shape = (0, 0)
        self.eq_n = 0

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Calculadora de Álgebra Lineal", style='Header.TLabel')
        title_label.pack(pady=10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        self.matrix_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.matrix_tab, text="Matrices")
        self.setup_matrix_tab()

        self.equations_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.equations_tab, text="Sistemas de Ecuaciones")
        self.setup_equations_tab()

        self.vectors_tab = ttk.Frame(self.notebook, padding="15")
        self.notebook.add(self.vectors_tab, text="Vectores")
        self.setup_vectors_tab()

    def setup_matrix_tab(self):
        self.matrix_tab.grid_rowconfigure(0, weight=0)
        self.matrix_tab.grid_rowconfigure(1, weight=1)
        self.matrix_tab.grid_rowconfigure(2, weight=0)
        self.matrix_tab.grid_rowconfigure(3, weight=1)
        self.matrix_tab.grid_columnconfigure(0, weight=1)

        size_frame = ttk.LabelFrame(self.matrix_tab, text="Definir Tamaño de Matrices", padding="10")
        size_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        ttk.Label(size_frame, text="Matriz 1 - Filas:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.m1_rows_entry = ttk.Entry(size_frame, width=10)
        self.m1_rows_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(size_frame, text="Matriz 1 - Columnas:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.m1_cols_entry = ttk.Entry(size_frame, width=10)
        self.m1_cols_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(size_frame, text="Matriz 2 - Filas:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.m2_rows_entry = ttk.Entry(size_frame, width=10)
        self.m2_rows_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(size_frame, text="Matriz 2 - Columnas:").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.m2_cols_entry = ttk.Entry(size_frame, width=10)
        self.m2_cols_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Button(size_frame, text="Establecer y Llenar Matrices", command=self.set_matrix_sizes).grid(row=2, column=0, columnspan=4, pady=10)

        self.matrix_canvas_outer_frame = ttk.Frame(self.matrix_tab)
        self.matrix_canvas_outer_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.matrix_canvas = Canvas(self.matrix_canvas_outer_frame, bg='#f0f0f0')
        self.matrix_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.matrix_scrollbar_y = ttk.Scrollbar(self.matrix_canvas_outer_frame, orient=tk.VERTICAL, command=self.matrix_canvas.yview)
        self.matrix_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.matrix_scrollbar_x = ttk.Scrollbar(self.matrix_canvas_outer_frame, orient=tk.HORIZONTAL, command=self.matrix_canvas.xview)
        self.matrix_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.matrix_canvas.configure(yscrollcommand=self.matrix_scrollbar_y.set, xscrollcommand=self.matrix_scrollbar_x.set)
        self.matrix_canvas.bind('<Configure>', lambda e: self.matrix_canvas.configure(scrollregion = self.matrix_canvas.bbox("all")))

        self.matrix_input_frame = ttk.Frame(self.matrix_canvas, padding="10")
        self.matrix_canvas.create_window((0, 0), window=self.matrix_input_frame, anchor="nw")

        self.op_matrix_frame = ttk.Frame(self.matrix_tab, padding="10")
        self.op_matrix_frame.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        ttk.Button(self.op_matrix_frame, text="Sumar Matrices", command=self.sum_matrices).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.op_matrix_frame, text="Multiplicar Matrices", command=self.multiply_matrices).pack(side=tk.LEFT, padx=5)
        # Añadir botones para determinantes de ambas matrices
        ttk.Button(self.op_matrix_frame, text="Det. Matriz 1", command=self.calculate_determinant_m1).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.op_matrix_frame, text="Det. Matriz 2", command=self.calculate_determinant_m2).pack(side=tk.LEFT, padx=5)


        self.matrix_result_text = scrolledtext.ScrolledText(self.matrix_tab, wrap=tk.WORD, width=80, height=20, font=('Consolas', 10)) # Asumiendo height=20
        self.matrix_result_text.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

    def set_matrix_sizes(self):
        try:
            r1 = int(self.m1_rows_entry.get())
            c1 = int(self.m1_cols_entry.get())
            r2 = int(self.m2_rows_entry.get())
            c2 = int(self.m2_cols_entry.get())

            if not all(isinstance(x, int) and x > 0 for x in [r1, c1, r2, c2]):
                messagebox.showerror("Error de Tamaño", "El tamaño de las matrices debe ser un número entero positivo.")
                return

            for widget in self.matrix_input_frame.winfo_children():
                widget.destroy()
            self.matrix1_entries = []
            self.matrix2_entries = []

            self.matrix_input_frame.grid_columnconfigure(0, weight=0)
            for j in range(c1):
                self.matrix_input_frame.grid_columnconfigure(j + 1, weight=0)
            self.matrix_input_frame.grid_columnconfigure(c1 + 1, weight=0, minsize=50)
            self.matrix_input_frame.grid_columnconfigure(c1 + 2, weight=0)
            for j in range(c2):
                self.matrix_input_frame.grid_columnconfigure(c1 + 3 + j, weight=0)

            max_rows = max(r1, r2)
            for i in range(max_rows + 1):
                self.matrix_input_frame.grid_rowconfigure(i, weight=0)

            ttk.Label(self.matrix_input_frame, text="Matriz 1:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)
            for i in range(r1):
                row_entries = []
                for j in range(c1):
                    entry = ttk.Entry(self.matrix_input_frame, width=5)
                    entry.grid(row=i+1, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix1_entries.append(row_entries)

            start_col_m2 = c1 + 2
            ttk.Label(self.matrix_input_frame, text="Matriz 2:").grid(row=0, column=start_col_m2, padx=5, pady=5, sticky=tk.NW)
            for i in range(r2):
                row_entries = []
                for j in range(c2):
                    entry = ttk.Entry(self.matrix_input_frame, width=5)
                    entry.grid(row=i+1, column=start_col_m2 + j, padx=2, pady=2)
                    row_entries.append(entry)
                self.matrix2_entries.append(row_entries)

            self.matrix1_shape = (r1, c1)
            self.matrix2_shape = (r2, c2)

            self.matrix_input_frame.update_idletasks()
            self.matrix_canvas.config(scrollregion=self.matrix_canvas.bbox("all"))

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce números enteros para el tamaño de las matrices.")

    def get_matrix_from_entries(self, entries_list, rows, cols, matrix_name):
        matrix_data = []
        for i in range(rows):
            row_data = []
            for j in range(cols):
                try:
                    value = float(entries_list[i][j].get())
                    row_data.append(value)
                except ValueError:
                    messagebox.showerror("Error de Elemento", f"El elemento en {matrix_name} [{i+1}][{j+1}] no es un número real válido.")
                    return None
                except IndexError:
                    messagebox.showerror("Error de Datos", f"No se han establecido o llenado todos los elementos para {matrix_name}.")
                    return None
            matrix_data.append(row_data)
        return np.array(matrix_data)

    def sum_matrices(self):
        self.matrix_result_text.delete(1.0, tk.END)
        if self.matrix1_shape == (0,0) or self.matrix2_shape == (0,0):
             messagebox.showwarning("Advertencia", "Primero establece el tamaño y llena las matrices.")
             return

        matriz1 = self.get_matrix_from_entries(self.matrix1_entries, *self.matrix1_shape, "Matriz 1")
        matriz2 = self.get_matrix_from_entries(self.matrix2_entries, *self.matrix2_shape, "Matriz 2")

        if matriz1 is None or matriz2 is None:
            return

        self.matrix_result_text.insert(tk.END, "--- Matrices de Entrada ---\n")
        self.matrix_result_text.insert(tk.END, "Matriz 1:\n" + str(matriz1) + "\n\n")
        self.matrix_result_text.insert(tk.END, "Matriz 2:\n" + str(matriz2) + "\n\n")

        if matriz1.shape == matriz2.shape:
            suma_matrices = matriz1 + matriz2
            self.matrix_result_text.insert(tk.END, "--- Suma de Matrices ---\n")
            self.matrix_result_text.insert(tk.END, "Resultado de la suma:\n" + str(suma_matrices) + "\n")
        else:
            self.matrix_result_text.insert(tk.END, "Las matrices no se pueden sumar (tamaños diferentes).\n")

    def multiply_matrices(self):
        self.matrix_result_text.delete(1.0, tk.END)
        if self.matrix1_shape == (0,0) or self.matrix2_shape == (0,0):
             messagebox.showwarning("Advertencia", "Primero establece el tamaño y llena las matrices.")
             return

        matriz1 = self.get_matrix_from_entries(self.matrix1_entries, *self.matrix1_shape, "Matriz 1")
        matriz2 = self.get_matrix_from_entries(self.matrix2_entries, *self.matrix2_shape, "Matriz 2")

        if matriz1 is None or matriz2 is None:
            return

        self.matrix_result_text.insert(tk.END, "--- Matrices de Entrada ---\n")
        self.matrix_result_text.insert(tk.END, "Matriz 1:\n" + str(matriz1) + "\n\n")
        self.matrix_result_text.insert(tk.END, "Matriz 2:\n" + str(matriz2) + "\n\n")

        if matriz1.shape[1] == matriz2.shape[0]:
            try:
                producto_matrices = np.dot(matriz1, matriz2)
                self.matrix_result_text.insert(tk.END, "--- Multiplicación de Matrices ---\n")
                self.matrix_result_text.insert(tk.END, "Resultado de la multiplicación:\n" + str(producto_matrices) + "\n")
            except ValueError as e:
                self.matrix_result_text.insert(tk.END, f"Error al multiplicar matrices: {e}\n")
        else:
            self.matrix_result_text.insert(tk.END, "Las matrices no se pueden multiplicar (columnas de la primera deben ser igual a filas de la segunda).\n")

    def calculate_determinant_m1(self):
        self.matrix_result_text.delete(1.0, tk.END)
        if self.matrix1_shape == (0,0):
            messagebox.showwarning("Advertencia", "Primero establece el tamaño y llena la Matriz 1.")
            return

        matriz1 = self.get_matrix_from_entries(self.matrix1_entries, *self.matrix1_shape, "Matriz 1")

        if matriz1 is None:
            return

        self.matrix_result_text.insert(tk.END, "--- Matriz de Entrada ---\n")
        self.matrix_result_text.insert(tk.END, "Matriz 1:\n" + str(matriz1) + "\n\n")

        if matriz1.shape[0] != matriz1.shape[1]:
            self.matrix_result_text.insert(tk.END, "La Matriz 1 no es cuadrada, no se puede calcular el determinante.\n")
        else:
            try:
                det = np.linalg.det(matriz1)
                self.matrix_result_text.insert(tk.END, "--- Determinante de Matriz 1 ---\n")
                self.matrix_result_text.insert(tk.END, f"Determinante(|M1|) = {det:.4f}\n")
            except np.linalg.LinAlgError:
                self.matrix_result_text.insert(tk.END, "Error: No se pudo calcular el determinante de la Matriz 1.\n")

    def calculate_determinant_m2(self): # NUEVA FUNCIÓN PARA EL DETERMINANTE DE LA MATRIZ 2
        self.matrix_result_text.delete(1.0, tk.END)
        if self.matrix2_shape == (0,0):
            messagebox.showwarning("Advertencia", "Primero establece el tamaño y llena la Matriz 2.")
            return

        matriz2 = self.get_matrix_from_entries(self.matrix2_entries, *self.matrix2_shape, "Matriz 2")

        if matriz2 is None:
            return

        self.matrix_result_text.insert(tk.END, "--- Matriz de Entrada ---\n")
        self.matrix_result_text.insert(tk.END, "Matriz 2:\n" + str(matriz2) + "\n\n")

        if matriz2.shape[0] != matriz2.shape[1]:
            self.matrix_result_text.insert(tk.END, "La Matriz 2 no es cuadrada, no se puede calcular el determinante.\n")
        else:
            try:
                det = np.linalg.det(matriz2)
                self.matrix_result_text.insert(tk.END, "--- Determinante de Matriz 2 ---\n")
                self.matrix_result_text.insert(tk.END, f"Determinante(|M2|) = {det:.4f}\n")
            except np.linalg.LinAlgError:
                self.matrix_result_text.insert(tk.END, "Error: No se pudo calcular el determinante de la Matriz 2.\n")


    def setup_equations_tab(self):
        self.equations_tab.grid_rowconfigure(0, weight=0)
        self.equations_tab.grid_rowconfigure(1, weight=1)
        self.equations_tab.grid_rowconfigure(2, weight=0)
        self.equations_tab.grid_rowconfigure(3, weight=1)
        self.equations_tab.grid_columnconfigure(0, weight=1)

        eq_size_frame = ttk.LabelFrame(self.equations_tab, text="Definir Tamaño del Sistema (NxN)", padding="10")
        eq_size_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        ttk.Label(eq_size_frame, text="Tamaño (N):").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.eq_n_entry = ttk.Entry(eq_size_frame, width=10)
        self.eq_n_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(eq_size_frame, text="Establecer y Llenar Sistema", command=self.set_equation_system_size).grid(row=0, column=2, padx=10)

        self.eq_canvas_frame = ttk.Frame(self.equations_tab)
        self.eq_canvas_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

        self.eq_canvas = Canvas(self.eq_canvas_frame, bg='#f0f0f0')
        self.eq_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.eq_scrollbar_y = ttk.Scrollbar(self.eq_canvas_frame, orient=tk.VERTICAL, command=self.eq_canvas.yview)
        self.eq_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.eq_scrollbar_x = ttk.Scrollbar(self.eq_canvas_frame, orient=tk.HORIZONTAL, command=self.eq_canvas.xview)
        self.eq_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)


        self.eq_canvas.configure(yscrollcommand=self.eq_scrollbar_y.set, xscrollcommand=self.eq_scrollbar_x.set)
        self.eq_canvas.bind('<Configure>', lambda e: self.eq_canvas.configure(scrollregion = self.eq_canvas.bbox("all")))

        self.eq_input_frame = ttk.Frame(self.eq_canvas, padding="10")
        self.eq_canvas.create_window((0, 0), window=self.eq_input_frame, anchor="nw")

        self.A_entries = []
        self.B_entries = []

        op_frame = ttk.Frame(self.equations_tab, padding="10")
        op_frame.grid(row=2, column=0, pady=5, padx=10, sticky="ew")
        ttk.Button(op_frame, text="Resolver por Cramer", command=self.solve_cramer).pack(side=tk.LEFT, padx=5)
        ttk.Button(op_frame, text="Resolver por Inversa", command=self.solve_inverse).pack(side=tk.LEFT, padx=5)

        self.eq_result_text = scrolledtext.ScrolledText(self.equations_tab, wrap=tk.WORD, width=80, height=15, font=('Consolas', 10))
        self.eq_result_text.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

    def set_equation_system_size(self):
        try:
            n = int(self.eq_n_entry.get())
            if not isinstance(n, int) or n <= 0:
                messagebox.showerror("Error de Tamaño", "El tamaño (N) debe ser un número entero positivo.")
                return

            for widget in self.eq_input_frame.winfo_children():
                widget.destroy()
            self.A_entries = []
            self.B_entries = []
            self.eq_n = n

            for j in range(n):
                self.eq_input_frame.grid_columnconfigure(j, weight=0)
            self.eq_input_frame.grid_columnconfigure(n, weight=0, minsize=30)
            self.eq_input_frame.grid_columnconfigure(n + 1, weight=0)

            ttk.Label(self.eq_input_frame, text="Matriz A:").grid(row=0, column=0, columnspan=n, pady=5, sticky=tk.W)
            for i in range(n):
                row_entries = []
                for j in range(n):
                    entry = ttk.Entry(self.eq_input_frame, width=5)
                    entry.grid(row=i+1, column=j, padx=2, pady=2)
                    row_entries.append(entry)
                self.A_entries.append(row_entries)

            ttk.Label(self.eq_input_frame, text="Vector B:").grid(row=0, column=n + 1, pady=5, sticky=tk.W)
            for i in range(n):
                entry = ttk.Entry(self.eq_input_frame, width=5)
                entry.grid(row=i+1, column=n + 1, padx=2, pady=2)
                self.B_entries.append(entry)

            self.eq_input_frame.update_idletasks()
            self.eq_canvas.config(scrollregion=self.eq_canvas.bbox("all"))

        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce un número entero para el tamaño del sistema.")

    def get_system_matrices(self):
        try:
            n = self.eq_n
            if n == 0:
                messagebox.showwarning("Advertencia", "Primero establece el tamaño del sistema.")
                return None, None

            A_data = []
            for i in range(n):
                row_data = []
                for j in range(n):
                    value = float(self.A_entries[i][j].get())
                    row_data.append(value)
                A_data.append(row_data)
            A = np.array(A_data)

            B_data = []
            for i in range(n):
                value = float(self.B_entries[i].get())
                B_data.append(value)
            B = np.array(B_data).reshape(n, 1)

            return A, B
        except AttributeError:
            messagebox.showwarning("Advertencia", "Primero establece el tamaño del sistema.")
            return None, None
        except ValueError:
            messagebox.showerror("Error de Elemento", "Por favor, asegúrate de que todos los coeficientes sean números reales.")
            return None, None
        except IndexError:
            messagebox.showwarning("Advertencia", "Asegúrate de llenar todos los elementos del sistema de ecuaciones.")
            return None, None

    def solve_cramer(self):
        self.eq_result_text.delete(1.0, tk.END)
        A, B = self.get_system_matrices()
        if A is None or B is None: return

        if A.shape[0] != A.shape[1]:
            self.eq_result_text.insert(tk.END, "Introduzca un sistema de ecuaciones cuadrado.\n")
            return

        det_A = np.linalg.det(A)
        self.eq_result_text.insert(tk.END, f"\nDeterminante de A (|A|): {det_A:.4f}\n")

        if abs(det_A) < 1e-9:
            self.eq_result_text.insert(tk.END, "El sistema de ecuaciones no tiene solución |A| = 0.\n")
        else:
            soluciones_cramer = []
            for i in range(self.eq_n):
                A_cramer = A.copy()
                A_cramer[:, i] = B.flatten()
                det_cramer = np.linalg.det(A_cramer)
                solucion_x = det_cramer / det_A
                soluciones_cramer.append(solucion_x)
                self.eq_result_text.insert(tk.END, f"\nMatriz A{chr(120+i)}:\n{A_cramer}\n")
                self.eq_result_text.insert(tk.END, f"Determinante de A{chr(120+i)} (|A{chr(120+i)}|): {det_cramer:.4f}\n")

            self.eq_result_text.insert(tk.END, "\nSolución del sistema por Cramer:\n")
            for i, sol in enumerate(soluciones_cramer):
                self.eq_result_text.insert(tk.END, f"x{i+1} = {sol:.4f}\n")

    def solve_inverse(self):
        self.eq_result_text.delete(1.0, tk.END)
        A, B = self.get_system_matrices()
        if A is None or B is None: return

        if A.shape[0] != A.shape[1]:
            self.eq_result_text.insert(tk.END, "Introduzca un sistema de ecuaciones cuadrado.\n")
            return

        det_A = np.linalg.det(A)
        self.eq_result_text.insert(tk.END, f"\nDeterminante de A (|A|): {det_A:.4f}\n")

        if abs(det_A) < 1e-9:
            self.eq_result_text.insert(tk.END, "El sistema de ecuaciones no tiene solución |A| = 0 y la matriz A no tiene inversa.\n")
        else:
            try:
                A_inversa = np.linalg.inv(A)
                self.eq_result_text.insert(tk.END, "\nMatriz Inversa A^-1:\n" + str(A_inversa) + "\n")
                solucion_inversa = np.dot(A_inversa, B)
                self.eq_result_text.insert(tk.END, "\nSolución del sistema por Matriz Inversa:\n")
                for i, sol in enumerate(solucion_inversa):
                    self.eq_result_text.insert(tk.END, f"x{i+1} = {sol[0]:.4f}\n")
            except np.linalg.LinAlgError:
                self.eq_result_text.insert(tk.END, "Error: La matriz no tiene inversa (es singular).\n")

    def setup_vectors_tab(self):
        vec_input_frame = ttk.LabelFrame(self.vectors_tab, text="Introducir Vectores (Magnitud y Ángulo)", padding="10")
        vec_input_frame.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(vec_input_frame, text="Vector 1 - Magnitud:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.v1_mag_entry = ttk.Entry(vec_input_frame, width=15)
        self.v1_mag_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(vec_input_frame, text="Vector 1 - Ángulo (grados):").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.v1_angle_entry = ttk.Entry(vec_input_frame, width=15)
        self.v1_angle_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(vec_input_frame, text="Vector 2 - Magnitud:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.v2_mag_entry = ttk.Entry(vec_input_frame, width=15)
        self.v2_mag_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(vec_input_frame, text="Vector 2 - Ángulo (grados):").grid(row=1, column=2, padx=5, pady=2, sticky=tk.W)
        self.v2_angle_entry = ttk.Entry(vec_input_frame, width=15)
        self.v2_angle_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Button(vec_input_frame, text="Calcular Componentes", command=self.calculate_vector_components).grid(row=2, column=0, columnspan=4, pady=10)

        op_frame = ttk.Frame(self.vectors_tab, padding="10")
        op_frame.pack(pady=5, padx=10, fill=tk.X)
        ttk.Button(op_frame, text="Sumar Vectores", command=self.sum_vectors).pack(side=tk.LEFT, padx=5)
        ttk.Button(op_frame, text="Producto Punto y Ángulo", command=self.dot_product_and_angle).pack(side=tk.LEFT, padx=5)
        ttk.Button(op_frame, text="Producto Cruz", command=self.cross_product).pack(side=tk.LEFT, padx=5)

        self.vector_result_text = scrolledtext.ScrolledText(self.vectors_tab, wrap=tk.WORD, width=80, height=15, font=('Consolas', 10))
        self.vector_result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def get_vectors_polar(self):
        try:
            mag1 = float(self.v1_mag_entry.get())
            ang1_grados = float(self.v1_angle_entry.get())
            mag2 = float(self.v2_mag_entry.get())
            ang2_grados = float(self.v2_angle_entry.get())

            if mag1 < 0 or mag2 < 0:
                messagebox.showerror("Error de Magnitud", "Las magnitudes no pueden ser negativas.")
                return None, None, None, None

            return mag1, ang1_grados, mag2, ang2_grados
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, introduce números reales para magnitud y ángulo.")
            return None, None, None, None

    def polar_to_rectangular(self, magnitude, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        component_x = magnitude * math.cos(angle_radians)
        component_y = magnitude * math.sin(angle_radians)
        return component_x, component_y, angle_radians

    def rectangular_to_polar(self, component_x, component_y):
        magnitude = math.sqrt(component_x**2 + component_y**2)
        angle_radians = math.atan2(component_y, component_x)
        angle_degrees = math.degrees(angle_radians)
        return magnitude, angle_degrees

    def calculate_vector_components(self):
        self.vector_result_text.delete(1.0, tk.END)
        mag1, ang1_grados, mag2, ang2_grados = self.get_vectors_polar()
        if mag1 is None: return

        x1, y1, rad1 = self.polar_to_rectangular(mag1, ang1_grados)
        x2, y2, rad2 = self.polar_to_rectangular(mag2, ang2_grados)

        self.vec1_rect = np.array([x1, y1])
        self.vec2_rect = np.array([x2, y2])
        self.v1_mag, self.v1_ang_grados = mag1, ang1_grados
        self.v2_mag, self.v2_ang_grados = mag2, ang2_grados

        self.vector_result_text.insert(tk.END, "--- Componentes Rectangulares ---\n")
        self.vector_result_text.insert(tk.END, f"Vector 1:\n")
        self.vector_result_text.insert(tk.END, f"  Magnitud: {mag1:.4f}, Ángulo (grados): {ang1_grados:.2f}, Ángulo (radianes): {rad1:.4f}\n")
        self.vector_result_text.insert(tk.END, f"  Componentes rectangulares: V1 = ({x1:.4f}, {y1:.4f})\n\n")
        self.vector_result_text.insert(tk.END, f"Vector 2:\n")
        self.vector_result_text.insert(tk.END, f"  Magnitud: {mag2:.4f}, Ángulo (grados): {ang2_grados:.2f}, Ángulo (radianes): {rad2:.4f}\n")
        self.vector_result_text.insert(tk.END, f"  Componentes rectangulares: V2 = ({x2:.4f}, {y2:.4f})\n")

    def sum_vectors(self):
        self.vector_result_text.delete(1.0, tk.END)
        if not hasattr(self, 'vec1_rect') or not hasattr(self, 'vec2_rect'):
            messagebox.showwarning("Advertencia", "Primero calcula las componentes de los vectores.")
            return

        suma_vectores = self.vec1_rect + self.vec2_rect
        mag_suma, ang_suma_grados = self.rectangular_to_polar(suma_vectores[0], suma_vectores[1])

        self.vector_result_text.insert(tk.END, "\n--- Suma de Vectores ---\n")
        self.vector_result_text.insert(tk.END, f"Suma de vectores (componentes rectangulares): V_suma = ({suma_vectores[0]:.4f}, {suma_vectores[1]:.4f})\n")
        self.vector_result_text.insert(tk.END, f"Magnitud de la suma: {mag_suma:.4f}\n")
        self.vector_result_text.insert(tk.END, f"Dirección de la suma (grados): {ang_suma_grados:.2f}°\n")

    def dot_product_and_angle(self):
        self.vector_result_text.delete(1.0, tk.END)
        if not hasattr(self, 'vec1_rect') or not hasattr(self, 'vec2_rect'):
            messagebox.showwarning("Advertencia", "Primero calcula las componentes de los vectores.")
            return

        producto_punto = np.dot(self.vec1_rect, self.vec2_rect)

        if self.v1_mag == 0 or self.v2_mag == 0:
            self.vector_result_text.insert(tk.END, "\n--- Producto Punto y Ángulo entre Vectores ---\n")
            self.vector_result_text.insert(tk.END, "No se puede calcular el ángulo si una de las magnitudes es cero.\n")
        else:
            cos_theta = producto_punto / (self.v1_mag * self.v2_mag)
            cos_theta = max(-1.0, min(1.0, cos_theta))
            angulo_entre_vectores_radianes = math.acos(cos_theta)
            angulo_entre_vectores_grados = math.degrees(angulo_entre_vectores_radianes)

            self.vector_result_text.insert(tk.END, "\n--- Producto Punto y Ángulo entre Vectores ---\n")
            self.vector_result_text.insert(tk.END, f"Producto Punto (V1 . V2): {producto_punto:.4f}\n")
            self.vector_result_text.insert(tk.END, f"Ángulo entre vectores (grados): {angulo_entre_vectores_grados:.2f}°\n")

    def cross_product(self):
        self.vector_result_text.delete(1.0, tk.END)
        if not hasattr(self, 'vec1_rect') or not hasattr(self, 'vec2_rect'):
            messagebox.showwarning("Advertencia", "Primero calcula las componentes de los vectores.")
            return

        x1, y1 = self.vec1_rect[0], self.vec1_rect[1]
        x2, y2 = self.vec2_rect[0], self.vec2_rect[1]
        producto_cruz_z = x1 * y2 - y1 * x2

        self.vector_result_text.insert(tk.END, "\n--- Producto Cruz de Vectores (Componente Z para 2D) ---\n")
        self.vector_result_text.insert(tk.END, f"Producto Cruz (V1 x V2): {producto_cruz_z:.4f} (Este es el componente z del vector resultante en 3D)\n")
        self.vector_result_text.insert(tk.END, f"El vector resultante del producto cruz en 3D sería (0, 0, {producto_cruz_z:.4f})\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgebraApp(root)
    root.mainloop()