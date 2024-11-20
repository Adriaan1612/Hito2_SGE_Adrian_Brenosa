import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

import self

from Encuesta import Encuesta
from conexionBD import ConexionBD

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Encuestas")
        self.root.geometry("800x600")
        self.root.state('zoomed')  # Iniciar en pantalla completa

        # Conexión a la base de datos
        self.db_connection = ConexionBD('localhost', 'root', 'curso', 'encuestas')
        self.encuesta = Encuesta(self.db_connection)

        # Crear un Frame para contener el Treeview y el Scrollbar
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Crear el Treeview para mostrar las encuestas
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana",
                                                      "Bebidas/FinSemana", "Destiladas/Semana", "Vinos/Semana",
                                                      "PerdidasControl", "DiversionAlcohol", "ProblemasDigestivos",
                                                      "TensionAlta", "DolorCabeza"), show='headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear el Scrollbar y asociarlo al Treeview
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Definir los encabezados de las columnas
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.cargar_encuestas()

        # Botones para agregar, actualizar, eliminar, filtrar, exportar encuestas
        self.boton_agregar = tk.Button(self.root, text="Agregar Encuesta", command=self.agregar_encuesta)
        self.boton_agregar.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_actualizar = tk.Button(self.root, text="Actualizar Encuesta", command=self.editar_encuesta)
        self.boton_actualizar.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_eliminar = tk.Button(self.root, text="Eliminar Encuesta", command=self.eliminar_encuesta)
        self.boton_eliminar.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_filtrar = tk.Button(self.root, text="Filtrar Encuestas", command=self.filtrar_encuestas)
        self.boton_filtrar.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_exportar = tk.Button(self.root, text="Exportar a Excel", command=self.exportar_a_excel)
        self.boton_exportar.pack(side=tk.LEFT, padx=10, pady=10)

        self.boton_grafico = tk.Button(self.root, text="Mostrar Gráfico", command=self.mostrar_opciones_grafico)
        self.boton_grafico.pack(side=tk.LEFT, padx=10, pady=10)

    def cargar_encuestas(self, query=None, params=None):
        """Carga todas las encuestas de la base de datos y las muestra en el Treeview"""
        encuestas = self.encuesta.obtener_encuestas(query, params)
        # Limpiar el Treeview antes de cargar las nuevas encuestas
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Mostrar todas las encuestas
        for encuesta in encuestas:
            self.tree.insert("", tk.END, values=encuesta)

    def agregar_encuesta(self):
        # Crear una nueva ventana para agregar la encuesta
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Agregar Encuesta")

        # Crear campos de entrada para cada dato de la encuesta
        labels = ["Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas/FinSemana",
                  "Destiladas/Semana", "Vinos/Semana", "PerdidasControl", "DiversionAlcohol",
                  "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        self.entries = []

        for i, label in enumerate(labels):
            tk.Label(self.add_window, text=label).grid(row=i, column=0)
            entry = tk.Entry(self.add_window)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        # Botón para guardar la nueva encuesta
        tk.Button(self.add_window, text="Guardar", command=self.guardar_nueva_encuesta).grid(row=len(labels), columnspan=2)

    def guardar_nueva_encuesta(self):
        try:
            # Obtener los datos ingresados de los campos de entrada y convertirlos a los tipos correctos
            edad = int(self.entries[0].get())
            sexo = self.entries[1].get()
            bebidas_semana = int(self.entries[2].get())
            cervezas_semana = int(self.entries[3].get())
            bebidas_fin_semana = int(self.entries[4].get())
            destiladas_semana = int(self.entries[5].get())
            vinos_semana = int(self.entries[6].get())
            perdidas_control = self.entries[7].get()
            diversion_alcohol = self.entries[8].get()
            problemas_digestivos = self.entries[9].get()
            tension_alta = self.entries[10].get()
            dolor_cabeza = self.entries[11].get()

            # Crear la nueva encuesta en la base de datos
            encuesta_data = (
                edad, sexo, bebidas_semana, cervezas_semana, bebidas_fin_semana,
                destiladas_semana, vinos_semana, perdidas_control, diversion_alcohol,
                problemas_digestivos, tension_alta, dolor_cabeza
            )
            self.encuesta.crear_encuesta(encuesta_data)
            self.cargar_encuestas()
            self.add_window.destroy()
            messagebox.showinfo("Éxito", "Encuesta agregada correctamente")
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def editar_encuesta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una encuesta para actualizar.")
            return

        encuesta_info = self.tree.item(selected_item[0], "values")
        encuesta_id = int(encuesta_info[0])

        # Crear una nueva ventana para editar la encuesta
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Editar Encuesta")

        # Crear campos de entrada para cada dato de la encuesta
        labels = ["Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas/FinSemana",
                  "Destiladas/Semana", "Vinos/Semana", "PerdidasControl", "DiversionAlcohol",
                  "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        self.entries = []

        for i, label in enumerate(labels):
            tk.Label(self.edit_window, text=label).grid(row=i, column=0)
            entry = tk.Entry(self.edit_window)
            entry.grid(row=i, column=1)
            self.entries.append(entry)

        # Cargar los datos actuales de la encuesta en los campos de entrada
        for i, value in enumerate(encuesta_info[1:]):
            self.entries[i].insert(0, value)

        # Botón para guardar los cambios
        tk.Button(self.edit_window, text="Guardar", command=lambda: self.guardar_cambios(encuesta_id)).grid(row=len(labels), columnspan=2)

    def guardar_cambios(self, encuesta_id):
        # Obtener los datos actualizados de los campos de entrada
        encuesta_data = tuple(entry.get() for entry in self.entries)

        # Actualizar la encuesta en la base de datos
        self.encuesta.actualizar_encuesta(encuesta_id, encuesta_data)
        self.cargar_encuestas()
        self.edit_window.destroy()
        messagebox.showinfo("Éxito", "Encuesta actualizada correctamente")

    def eliminar_encuesta(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona una encuesta para eliminar.")
            return

        encuesta_info = self.tree.item(selected_item[0], "values")
        encuesta_id = int(encuesta_info[0])

        # Eliminar la encuesta de la base de datos
        self.encuesta.eliminar_encuesta(encuesta_id)
        self.cargar_encuestas()
        messagebox.showinfo("Éxito", f"Encuesta con ID {encuesta_id} eliminada correctamente")

    def filtrar_encuestas(self):
        # Crear una nueva ventana para filtrar las encuestas
        self.filter_window = tk.Toplevel(self.root)
        self.filter_window.title("Filtrar Encuestas")

        # Crear campos de entrada para cada criterio de filtrado
        labels = ["Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas/FinSemana",
                  "Destiladas/Semana", "Vinos/Semana", "PerdidasControl", "DiversionAlcohol",
                  "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]
        self.filter_entries = []

        for i, label in enumerate(labels):
            tk.Label(self.filter_window, text=label).grid(row=i, column=0)
            entry = tk.Entry(self.filter_window)
            entry.grid(row=i, column=1)
            self.filter_entries.append(entry)

        # Botón para aplicar el filtro
        tk.Button(self.filter_window, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=len(labels), columnspan=2)

    def aplicar_filtro(self):
        # Construir la consulta SQL dinámica basada en los criterios de filtrado
        query = "SELECT * FROM ENCUESTA WHERE 1=1"
        params = []

        labels = ["edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                  "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol",
                  "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]

        for i, entry in enumerate(self.filter_entries):
            value = entry.get()
            if value:
                query += f" AND {labels[i]} = %s"
                params.append(value)

        self.cargar_encuestas(query, params)
        self.filter_window.destroy()

    def exportar_a_excel(self):
    # Obtener los datos actuales del Treeview
    data = [self.tree.item(item)["values"] for item in self.tree.get_children()]
    columns = ["ID", "Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana", "Bebidas/FinSemana", "Destiladas/Semana", "Vinos/Semana",
               "PerdidasControl", "DiversionAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]

    # Crear un DataFrame y exportar a Excel
    df = pd.DataFrame(data, columns=columns)
    df.to_excel("C:/path/to/your/directory/encuestas_filtradas.xlsx", index=False)
    messagebox.showinfo("Éxito", "Datos exportados a encuestas_filtradas.xlsx")

    def mostrar_opciones_grafico(self):
        # Crear una ventana emergente para seleccionar el tipo de gráfico y el campo
        self.grafico_window = tk.Toplevel(self.root)
        self.grafico_window.title("Seleccionar Gráfico")

        tk.Label(self.grafico_window, text="Tipo de Gráfico").grid(row=0, column=0)
        self.tipo_grafico = ttk.Combobox(self.grafico_window, values=["Barras", "Pastel"])
        self.tipo_grafico.grid(row=0, column=1)

        tk.Label(self.grafico_window, text="Campo").grid(row=1, column=0)
        self.campo_grafico = ttk.Combobox(self.grafico_window, values=["Edad", "Sexo", "Bebidas/Semana", "Cervezas/Semana",
                                                                       "Bebidas/FinSemana", "Destiladas/Semana", "Vinos/Semana",
                                                                       "PerdidasControl", "DiversionAlcohol", "ProblemasDigestivos",
                                                                       "TensionAlta", "DolorCabeza"])
        self.campo_grafico.grid(row=1, column=1)

        tk.Button(self.grafico_window, text="Mostrar", command=self.mostrar_grafico).grid(row=2, columnspan=2)

    def mostrar_grafico(self):
        tipo = self.tipo_grafico.get()
        campo = self.campo_grafico.get()

        if tipo and campo:
            if tipo == "Barras":
                self.mostrar_grafico_barras(campo)
            elif tipo == "Pastel":
                self.mostrar_grafico_pastel(campo)
            self.grafico_window.destroy()
        else:
            messagebox.showwarning("Advertencia", "Selecciona el tipo de gráfico y el campo.")

    def mostrar_grafico_barras(self, campo):
        # Obtener los datos del Treeview
        data = [self.tree.item(item)["values"] for item in self.tree.get_children()]
        campo_index = self.tree["columns"].index(campo)
        valores = [item[campo_index] for item in data]

        # Contar la frecuencia de cada valor
        contador_valores = Counter(valores)
        etiquetas = list(contador_valores.keys())
        frecuencias = list(contador_valores.values())

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(etiquetas, frecuencias, color='skyblue')
        plt.xlabel(campo)
        plt.ylabel('Frecuencia')
        plt.title(f'Distribución de {campo}')
        plt.show()

    def mostrar_grafico_pastel(self, campo):
        # Obtener los datos del Treeview
        data = [self.tree.item(item)["values"] for item in self.tree.get_children()]
        campo_index = self.tree["columns"].index(campo)
        valores = [item[campo_index] for item in data]

        # Contar la frecuencia de cada valor
        contador_valores = Counter(valores)
        etiquetas = list(contador_valores.keys())
        tamanos = list(contador_valores.values())

        # Crear el gráfico de pastel
        plt.figure(figsize=(8, 8))
        plt.pie(tamanos, labels=etiquetas, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        plt.title(f'Distribución de {campo}')
        plt.axis('equal')  # Asegurar que el gráfico sea un círculo
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()