#Miranda Martiez Alexys
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import Tk, Label, Entry, Button, Frame, messagebox
import tkinter.font as tkFont
import conexion
import menu

def abrir_empleados():
    empleados = tk.Tk()
    empleados.title("Gestión de Empleados")
    empleados.geometry("700x800")
    empleados.config(bg= "#CFFFF4")
    
    
    campos = ["id_empleados", "nom_empleados", "cargo", "edad", "sexo", "no_telefono", "id_sucursal"]
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(empleados,bg= "#55F4FF", text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(empleados)
        entradas[texto].grid(row=i, column=1, padx=10, pady=5)
        
    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd()
        cursor = con.cursor()
        cursor.execute(sql, params)
        if fetch:
            resultado = cursor.fetchall()
            con.close()
            return resultado
        else:
            con.commit()
            con.close()

    def insertar():
        if any(not entradas[c].get() for c in campos):
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
            return
        sql = "INSERT INTO empleados (id_empleados, nom_empleados, cargo, edad, sexo, no_telefono, id_sucursal) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Empleado registrado correctamente")

    def actualizar():
        if not entradas["id_empleados"].get():
            messagebox.showwarning("Atención", "Seleccione un empleado para actualizar")
            return
        sql = """
        UPDATE empleados 
        SET nom_empleados=%s, cargo=%s, edad=%s, sexo=%s, no_telefono=%s, id_sucursal=%s 
        WHERE id_empleados=%s
        """
        params = (
            entradas["nom_empleados"].get(),
            entradas["cargo"].get(),
            entradas["edad"].get(),
            entradas["sexo"].get(),
            entradas["no_telefono"].get(),
            entradas["id_sucursal"].get(),
            entradas["id_empleados"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Empleado actualizado correctamente")
            
    def eliminar():
        if not entradas["id_empleados"].get():
            messagebox.showwarning("Atención", "Seleccione un empleado para eliminar")
            return
        sql = "DELETE FROM empleados WHERE id_empleados=%s"
        ejecutar_sql(sql, (entradas["id_empleados"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
            
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
                
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM empleados", fetch=True)
        for fila in datos:
            tabla.insert("", tk.END, values=fila)
        
    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, c in enumerate(campos):
                entradas[c].delete(0, tk.END)
                entradas[c].insert(0, valores[i])
                
    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar", eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        tk.Button(empleados,bg= "#AFF8FF", text=texto, width=12, command=cmd).grid(row=len(campos), column=i, padx=10, pady=10)
            
    columnas = ("id_empleados", "nom_empleados", "cargo", "edad", "sexo", "no_telefono", "id_sucursal")
    tabla = ttk.Treeview(empleados, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.grid(row=len(campos)+1, column=0, columnspan=7, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
        
    tk.Button(empleados,bg= "#FFDCF4", text="Regresar al Menú", width=20, command=lambda: [empleados.destroy(), menu.abrir_menu()]).grid(row=len(campos)+2, column=0, columnspan=7, pady=10)
    
    mostrar_datos()
    empleados.mainloop()

if __name__ == "__main__":
    abrir_empleados()
