#Miranda Martiez Alexys 
import tkinter as tk
from tkinter import messagebox
import menu
from tkinter import Tk, Label, Entry, Button, Frame, messagebox
import tkinter.font as tkFont


usuario_correcto = "cafe de altura"
pass_correcto ="395487"

def mostrar_login():
    ventana_login = tk.Tk()
    ventana_login.title("login")
    ventana_login.geometry("400x200")
    ventana_login.config(bg= "#0649FF")
    


    def verificar_login():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        
        if not usuario or not contraseña:
            messagebox.showwarning("campos vacios", "por favor, ingrese usuario y contraseña. ")
            return
        
        if usuario == usuario_correcto and contraseña == pass_correcto:
            messagebox.showinfo("Datos corecto", f"¡Bienvenido, {usuario}!")
            ventana_login.destroy()
            menu.abrir_menu()
        else:
            messagebox.showerror("Error", "usuario o contraseña incorrectos.")
            
    tk.Label(ventana_login, text="usuario:",bg= "#5C9DFF").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()
    entry_usuario.focus()
    
    tk.Label(ventana_login, text="contraseña:", bg= "#C7C7B4").pack(pady=5)
    entry_contraseña = tk.Entry(ventana_login, show="*")
    entry_contraseña.pack()
    
    0
    tk.Button(ventana_login, text="iniciar sesion", command=verificar_login, bg= "#D68F8F").pack(pady=10)
    
    tk.Button(ventana_login, text="salir", command=ventana_login.destroy,bg= "#80F116").pack(pady=5)
    ventana_login.mainloop()
    
    


if __name__ =="__main__":
    mostrar_login()
    

            