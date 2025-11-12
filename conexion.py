#Miranda Martinez Alexys
import mysql.connector
#sql.connector sirve para que python realice conexiones con BD
from tkinter import messagebox
#messagebox es una funcion de la libreria tkinter

def conectar_bd(): # Defenimos nuestra funcion para conectar
    try:
        conn = mysql.connector.connect(
            host ="localhost", #Nombre del servidor
            user ="root", # Nombre del usuario
            password = "12345678", # Contrseña
            database= "cielo_querido_cafe" #Nombre de la base de datos
        )
        return conn #Retornamos la conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo establecer la conexion con la BD\n{err}")
        return None
    # Si algo sale mal, err guardara exactamente que error se genero
    #mysql.connector.Error indica exactamente cual es el error
    #f"No se pudo establecer la conexion con la BD\n{err}"
    #  se muestra ese mensaje de error, junto con el error encontrado 
    # return None, si existe un error, devuelve None, asi el resto
    # del programa sabra que algo fallo
        
             