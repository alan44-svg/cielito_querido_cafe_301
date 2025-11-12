#Miranda Martinez Alexys
import tkinter as tk 
import login
import empleados
import productos
import productos
import proveedor
import sucursal
import ventas

def abrir_menu():
    menu = tk.Tk()
    menu.title("menu principal")
    menu.geometry("300x350")
    menu.config(bg= "#000000")
    
    def regresar_a_login():
        menu.destroy()
        login.mostrar_login()
        
    def abrir_empleados():
        menu.withdraw()
        ventana_empleados = empleados.abrir_empleados()
        ventana_empleados.wait_window()
        menu.deiconify()


    def abrir_productos():
        menu.withdraw()
        ventana_productos = productos.abrir_productos()
        ventana_productos.wait_window()
        menu.deiconify()
        
    def abrir_proveedor():
        menu.withdraw()
        ventana_proveedor = proveedor.abrir_proveedor()
        ventana_proveedor.wait_window()
        menu.deiconify()
    
    def abrir_sucursal():
        menu.withdraw()
        ventana_sucursales = sucursal.abrir_sucursal()
        ventana_sucursales.wait_window()
        menu.deiconify()
        
    def abrir_ventas():
        menu.withdraw()
        ventana_ventas= ventas.abrir_ventas()
        ventana_ventas.wait_window()
        menu.deiconify()
        
        
    tk.Label(menu, text="bienvenido al menu principal",bg="#ACF7FF", font=("Arial", 14)).pack(pady=20)
    tk.Button(menu, text="empleados",bg= "#DCFFA4", width=25, command=abrir_empleados).pack(pady=5)
    tk.Button(menu, text="productos",bg= "#DCFFA4", width=25, command=abrir_productos).pack(pady=5)
    tk.Button(menu, text="proveedor",bg= "#DCFFA4", width=25, command=abrir_proveedor).pack(pady=5)
    tk.Button(menu, text="sucursal",bg= "#DCFFA4", width=25, command=abrir_sucursal).pack(pady=5)
    tk.Button(menu, text="ventas",bg= "#DCFFA4", width=25, command=abrir_ventas).pack(pady=5)
    tk.Button(menu, text="cerrar sesion",bg= "#FFEBAA", width=25, command=regresar_a_login).pack(pady=20)
        
    menu.mainloop()
        
if __name__ == "__main__":
    abrir_menu() 