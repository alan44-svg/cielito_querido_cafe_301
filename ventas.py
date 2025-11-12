#Miranda Martinez Alexys
import tkinter as tk
from tkinter import ttk, messagebox
import conexion
import menu

def abrir_ventas():
    ventas = tk.Tk() 
    ventas.title("Gestión de Ventas") 
    ventas.geometry("1300x1000")
    ventas.config(bg= "#FFFFC1")
    
    campos = [
        ("id_ventas", 0, 0),
        ("fecha_ventas (YYYY-MM-DD)", 1, 0),
        ("id_producto", 2 , 0),
        ("id_empleados", 3, 0),
        ("id_sucursal", 4, 0),
        ("cantidad_producto", 0, 2),
        ("precio_unitario", 1, 2),
        ("subtotal", 2, 2),
        ("iva", 3, 2),
        ("total", 4, 2)
    ]
    entradas = {}
    for texto, fila, col in campos:
        tk.Label(ventas,bg= "#FAFFB4", text=texto).grid(row=fila, column=col, padx=10, pady=5,sticky="w")
        entrada = tk.Entry(ventas)
        entrada.grid(row=fila, column=col+1, padx=10, pady=5)
        entradas[texto] = entrada
        
    def ejecutar_sql(sql, params=(), fetch=False):
        con = conexion.conectar_bd()
        cursor = con.cursor()
        cursor.execute(sql, params) 
        if fetch: 
            datos = cursor.fetchall()
            con.close()
            return datos
        else:
            con.commit()
            con.close()
                
    def calcular_totales(event=None):
        try:
            cantidad_producto = float(entradas["cantidad_producto"].get())
            precio_unitario = float(entradas["precio_unitario"].get())
            subtotal = cantidad_producto * precio_unitario
            iva = subtotal * 0.16
            total = subtotal + iva
            entradas["subtotal"].delete(0, tk.END)
            entradas["subtotal"].insert(0, f"{subtotal:.2f}")
            entradas["iva"].delete(0, tk.END)
            entradas["iva"].insert(0, f"{iva:.2f}")
            entradas["total"].delete(0, tk.END)
            entradas["total"].insert(0, f"{total:.2f}")
        except ValueError:
            for campo in ("subtotal", "iva", "total"):
                entradas[campo].delete(0, tk.END)
        
    entradas["cantidad_producto"].bind("<KeyRelease>", calcular_totales)
    entradas["precio_unitario"].bind("<KeyRelease>", calcular_totales)
        
    def insertar():
        if not entradas["id_ventas"].get() or not entradas["fecha_ventas (YYYY-MM-DD)"].get() or not entradas["id_producto"].get() or not entradas["id_empleados"].get() or not entradas["id_sucursal"].get():
            messagebox.showwarning("Campos vacíos", "cantidad_producto y precio_unitario son obligatorios")
            return
        sql = """INSERT INTO ventas (id_ventas, fecha_ventas, id_producto, id_empleados, id_sucursal, cantidad_producto, precio_unitario, subtotal, iva, total)
                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = tuple(entradas[c].get() for c in ["id_ventas", "fecha_ventas (YYYY-MM-DD)", "id_producto", "id_empleados", "id_sucursal","cantidad_producto",
                                                   "precio_unitario", "subtotal", "iva", "total"])
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Ventas registrada correctamente")
    
    def actualizar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una venta paraactualizar")
            return
        sql = """UPDATE ventas SET fecha_ventas=%s, id_producto=%s, id_empleados=%s, id_sucursal=%s, id_producto=%s, precio_unitario=%s, subtotal=%s, iva=%s, total=%s WHERE id_ventas=%s"""
        params = (
            entradas["fecha_ventas (YYYY-MM-DD)"].get(),
            entradas["id_producto"].get(),
            entradas["id_empleados"].get(),
            entradas["id_sucursal"].get(),
            entradas["cantidad_producto"].get(),
            entradas["precio_unitario"].get(),
            entradas["subtotal"].get(),
            entradas["iva"].get(),
            entradas["total"].get(),
            entradas["id_ventas"].get()
        )
        ejecutar_sql(sql, params)
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta actualizada correctamente")
        
    def eliminar():
        if not entradas["id_ventas"].get():
            messagebox.showwarning("Atención", "Seleccione una venta para eliminar")
            return
        ejecutar_sql("DELETE FROM ventas WHERE id_ventas=%s", (entradas["id_ventas"].get(),))
        mostrar_datos()
        limpiar()
        messagebox.showinfo("Éxito", "Venta eliminada correctamente")
    
    def limpiar():
        for e in entradas.values():
            e.delete(0, tk.END)

    def mostrar_datos():
        for row in tabla.get_children():
            tabla.delete(row)
        datos = ejecutar_sql("SELECT * FROM ventas", fetch=True) 
        #datos = ejecutar_sql("SELECT `id_ventas`,`fecha_ventas`,`nom_producto`,`cantidad_producto`,`precio_unitario`,`subtotal`,`iva`,`total` FROM ventas INNER JOIN productos on ventas.id_ventas=productos.id_producto", fetch=True)
        for fila in datos: 
            tabla.insert("", tk.END, values=fila)
    
    def seleccionar(event):
        seleccionado = tabla.selection()
        if seleccionado:
            valores = tabla.item(seleccionado[0], "values")
            for i, campo in enumerate(["id_ventas", "fecha_ventas (YYYY-MM-DD)", "id_producto", "id_empleados","id_sucursal","cantidad_producto","precio_unitario", "subtotal", "iva", "total"]):
                entradas[campo].delete(0, tk.END)
                entradas[campo].insert(0, valores[i])
    botones = [("Agregar", insertar), ("Actualizar", actualizar), ("Eliminar",eliminar), ("Limpiar", limpiar)]
    for i, (texto, cmd) in enumerate(botones):
        tk.Button(ventas,bg= "#FF9393", text=texto, width=12, command=cmd).grid(row=5, column=i,padx=10, pady=10)
        columnas = ("id_ventas", "fecha_ventas", "id_producto", "id_empleados", "id_sucursal", "cantidad_producto", "precio_unitario", "subtotal", "iva", "total")
        tabla = ttk.Treeview(ventas, columns=columnas, show="headings", height=12)
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=110)
        tabla.grid(row=6, column=0, columnspan=10, padx=10, pady=20)
        tabla.bind("<<TreeviewSelect>>", seleccionar)
        
        tk.Button(ventas,bg= "#FFF9C2", text="Regresar al Menú", width=20,command=lambda: [ventas.destroy(), menu.abrir_menu()]).grid(row=7,column=0, columnspan=10, pady=10)
        
    mostrar_datos()
    ventas.mainloop()
        
if __name__ == "__main__":
    abrir_ventas()
