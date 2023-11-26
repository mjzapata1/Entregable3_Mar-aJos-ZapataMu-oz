from PyQt5.QtCore import QObject
import pydicom
import matplotlib.pyplot as plt
import os

"""Se creará primero una clase base de datos, la cuál contendrá la información del ususario: nombre y contraseña, 
predeterminado en el entregable, para dejar ingresar únicamente si los datos ingresados son correctos."""

class BaseDatos:
    def __init__(self):
        self.__login = "medicoAnalitico"
        self.__password = "bio12345"

    def validarUsuario(self, l, p):
        return self.__login == l and self.__password == p

class ModeloDicom:
    def __init__(self):
        self.carpetas = ["Circle of Willis","Sarcoma","Prostata"]
        self.imagenesDicom = {}

    def cargarCarpetas(self):
        for carpeta in self.carpetas:
            imagenesDicom = [os.path.join(carpeta, imagen) for imagen in os.listdir(carpeta) if imagen.lower().endswith(".dcm")]
            self.imagenesDicom[carpeta] = imagenesDicom

        return self.carpetas
    
