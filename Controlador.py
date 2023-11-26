from PyQt5.QtWidgets import QApplication
from Modelo import *
from Vista import *
import sys

class Controlador:
    def __init__(self, vista_login, vista_dicom, modelo_bd, modelo_dicom):
        self.__mi_vista_login = vista_login
        self.__mi_vista_dicom = vista_dicom
        self.__mi_modelo_bd = modelo_bd
        self.__mi_modelo_dicom = modelo_dicom

    def validarUsuario(self, l, p):
        return self.__mi_modelo_bd.validarUsuario(l, p)

    def mostrarVentanaDicom(self):
        self.__mi_vista_dicom.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    modelo_dicom = ModeloDicom()
    modelo_bd = BaseDatos()

    vista_login = VentanaLogin(None)  # El controlador se establecerá más tarde
    vista_dicom = VentanaDicom(None, modelo_dicom)  # El controlador se establecerá más tarde

    controlador_login = Controlador(vista_login, vista_dicom, modelo_bd, modelo_dicom)
    vista_login.setControlador(controlador_login)
    vista_dicom.setControlador(controlador_login)

    controlador_login.mostrarVentanaDicom = lambda: vista_dicom.show()  # Sobrescribe el método para mostrar VentanaDicom

    vista_login.show()

    sys.exit(app.exec_())