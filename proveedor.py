#Miranda Martiez Alexys
import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_proveedor():
    proveedor = tk.Tk()
    proveedor.title("Gestión de Proveedor")
    proveedor.geometry("750x650")
    proveedor.config(bg= "#0022E3")
    
    
    
    campos = ["id_proveedor", "nom_proveedor", "direccion", "e_mail", "no_telefono"]
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(proveedor,bg= "#7DFFE5", text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(proveedor)
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
        sql = "INSERT INTO proveedor (id_proveedor, nom_proveedor,  direccion, e_mail, no_telefono) VALUES (%s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Proveedor registrado correctamente")

    def actualizar():
        if not entradas["id_proveedor"].get():
            messagebox.showwarning("Atención", "Seleccione un proveedor para actualizar")
            return
        sql = """
        UPDATE proveedor
        SET nom_proveedor=%s, direccion=%s, e_mail=%s, no_telefono=%s 
        WHERE id_proveedor=%s
        """
        params = (
            entradas["nom_proveedor"].get(),
            entradas["direccion"].get(),
            entradas["e_mail"].get(),
            entradas["no_telefono"].get(),
            entradas["id_proveedor"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
            
    def eliminar():
        if not entradas["id_proveedor"].get():
            messagebox.showwarning("Atención", "Seleccione un empleado para eliminar")
            return
        sql = "DELETE FROM proveedor WHERE id_proveedor=%s"
        ejecutar_sql(sql, (entradas["id_proveedor"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
                
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM proveedor", fetch=True)
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
        tk.Button(proveedor,bg= "#29F8FF", text=texto, width=12, command=cmd).grid(row=len(campos), column=i, padx=10, pady=10)
            
    columnas = ("id_proveedor", "nom_proveedor", "direccion", "e_mail", "no_telefono")
    tabla = ttk.Treeview(proveedor, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.grid(row=len(campos)+1, column=0, columnspan=5, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
        
    tk.Button(proveedor,bg= "#ADFF29", text="Regresar al Menú", width=20, command=lambda: [proveedor.destroy(), menu.abrir_menu()]).grid(row=len(campos)+2, column=0, columnspan=5, pady=10)
    
    mostrar_datos()
    proveedor.mainloop()

if __name__ == "__main__":
    abrir_proveedor()
