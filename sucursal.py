#Miranda Martiez Alexys
import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_sucursal():
    sucursales = tk.Tk()
    sucursales.title("Gestión de Sucursales")
    sucursales.geometry("800x700")
    sucursales.config(bg= "#96FCFF")
    
    campos = ["id_sucursal", "nom_sucursal", "direccion_sucursal", "horario", "no_contacto"]
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(sucursales,bg= "#CCFFFE", text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(sucursales)
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
        sql = "INSERT INTO sucursal (id_sucursal,  nom_sucursal, direccion_sucursal, horario, no_contacto) VALUES (%s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "sucursal registrado correctamente")

    def actualizar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione un empleado para actualizar")
            return
        sql = """
        UPDATE sucursal
        SET nom_sucursal=%s, direccion_sucursal=%s, horario=%s, no_contacto=%s 
        WHERE id_sucursal=%s
        """
        params = (
            entradas["nom_sucursal"].get(),
            entradas["direccion_sucursal"].get(),
            entradas["horario"].get(),
            entradas["no_contacto"].get(),
            entradas["id_sucursal"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal actualizada correctamente")
            
    def eliminar():
        if not entradas["id_sucursal"].get():
            messagebox.showwarning("Atención", "Seleccione una sucursal para eliminar")
            return
        sql = "DELETE FROM sucursal WHERE id_sucursal=%s"
        ejecutar_sql(sql, (entradas["id_sucursal"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Sucursal eliminada correctamente")
            
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
                
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM sucursal", fetch=True)
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
        tk.Button(sucursales,bg= "#FFDCF4", text=texto, width=12, command=cmd).grid(row=len(campos), column=i, padx=10, pady=10)
            
    columnas = ("id_sucursal", "nom_sucursal", "direccion_sucursal", "horario", "no_contacto")
    tabla = ttk.Treeview(sucursales, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.grid(row=len(campos)+1, column=0, columnspan=5, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
        
    tk.Button(sucursales,bg= "#B7E3FF" ,text="Regresar al Menú", width=20, command=lambda: [sucursales.destroy(), menu.abrir_menu()]).grid(row=len(campos)+2, column=0, columnspan=5, pady=10)
    
    mostrar_datos()
    sucursales.mainloop()

if __name__ == "__main__":
    abrir_sucursal()
