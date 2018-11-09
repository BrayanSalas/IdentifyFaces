from tkinter import messagebox
import requests
import pyrebase
import urllib
import os

class StorageFb:
    # Configuracion para el llamado de las funciones
    config = {
        "apiKey": "AIzaSyCz1KXOrNVVmy0RI-dvOhkTPUo0NemBzlg",
        "authDomain": "identify-faces.firebaseapp.com",
        "databaseURL": "https://identify-faces.firebaseio.com",
        "projectId": "identify-faces",
        "storageBucket": "identify-faces.appspot.com",
        "messagingSenderId": "327186042515",
        "serviceAccount": "C:/Users/braya/Documents/Archive-9a29/prueba/serviceAccount.json"
    }
    firebase = pyrebase.initialize_app(config)
    global storage
    storage = firebase.storage()
    
    def get_files():
        try:
            array = []
            files = storage.list_files()
            for file in files:
                archivo = file.name
                formatName = archivo.replace("Archivos/", "")
                if (formatName == ""):
                    None
                else:
                    array.append(formatName)
        except:
            messagebox.showerror("Borrar archivo", "No se pudo realizar, revise su conexion a internet")
        return array

    def delete_file(filename):
        #%20 para archivos con espacios, si no tienen espacios nombre normal
        formatName = filename.replace(" ", "%20")
        my_url = "https://firebasestorage.googleapis.com/v0/b/identify-faces.appspot.com/o/Archivos%2F" + formatName
        try:
            r = requests.delete(my_url)
            messagebox.showinfo("Borrar archivo", "Archivo borrado exitosamente")
        except:
            messagebox.showerror("Borrar archivo", "No se pudo realizar, revise su conexion a internet")
        

    def upload_file(filename):
        try:
            file = os.path.basename(filename)
            try:
                my_file = open(filename, "rb")
                my_bytes = my_file.read()
            except:
                messagebox.showerror("Subir archivo", "No se pudo realizar, revise que tenga un archivo valido")
            my_url = 'https://firebasestorage.googleapis.com/v0/b/identify-faces.appspot.com/o/Archivos%2F' + file
            r = requests.post(my_url, files= { 'file': my_bytes })
            print(r.json())
            messagebox.showinfo("Subir archivo", "Subido con exito")
        except:
            messagebox.showerror("Subir archivo", "No se pudo realizar, revise su conexion a internet")

    def download_file(filename):
        try:
            storage.child("Archivos/" + filename).download("C:/Users/braya/Downloads/" + filename)
            messagebox.showinfo("Descarga de archivo", "Archivo descargado con exito en Downloads")
        except:
            messagebox.showerror("Descarga de archivo", "No se pudo realizar, revise su conexion a internet")