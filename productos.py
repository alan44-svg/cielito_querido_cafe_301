#Miranda Martiez Alexys
import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_productos():
    productos = tk.Tk()
    productos.title("Gestión de Productos")
    productos.geometry("700x650")
    productos.config(bg= "#BEFDFF")
    
    campos = ["id_producto", "nom_producto", "tipo_producto", "costo", "id_proveedor"]
    entradas = {}
    
    for i, texto in enumerate(campos):
        tk.Label(productos,bg= "#7FF4FF" ,text=texto).grid(row=i, column=0, padx=10, pady=5, sticky="w")
        entradas[texto] = tk.Entry(productos)
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
        sql = "INSERT INTO productos (id_producto, nom_producto,  tipo_producto, costo, id_proveedor) VALUES (%s, %s, %s, %s, %s)"
        params = tuple(entradas[c].get() for c in campos)
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto registrado correctamente")

    def actualizar():
        if not entradas["id_producto"].get():
            messagebox.showwarning("Atención", "Seleccione un producto para actualizar")
            return
        sql = """
        UPDATE productos
        SET nom_producto=%s, tipo_producto=%s, costo=%s, id_proveedor=%s 
        WHERE id_producto=%s
        """
        params = (
            entradas["nom_producto"].get(),
            entradas["tipo_producto"].get(),
            entradas["costo"].get(),
            entradas["id_proveedor"].get(),
            entradas["id_producto"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            
    def eliminar():
        if not entradas["id_producto"].get():
            messagebox.showwarning("Atención", "Seleccione un empleado para eliminar")
            return
        sql = "DELETE FROM productos WHERE id_producto=%s"
        ejecutar_sql(sql, (entradas["id_producto"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)
                
    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM productos", fetch=True)
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
        tk.Button(productos,bg= "#4DE7FF", text=texto, width=12, command=cmd).grid(row=len(campos), column=i, padx=10, pady=10)
            
    columnas = ("id_producto", "nom_producto", "tipo_producto", "costo", "id_proveedor")
    tabla = ttk.Treeview(productos, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.grid(row=len(campos)+1, column=0, columnspan=5, padx=10, pady=20)
    tabla.bind("<<TreeviewSelect>>", seleccionar)
        
    tk.Button(productos,bg= "#5AE6EB", text="Regresar al Menú", width=20, command=lambda: [productos.destroy(), menu.abrir_menu()]).grid(row=len(campos)+2, column=0, columnspan=5, pady=10)
    
    mostrar_datos()
    productos.mainloop()

if __name__ == "__main__":
    abrir_productos()
