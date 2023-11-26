from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QGraphicsScene, QGraphicsView,QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
import os
from Modelo import *
import matplotlib.pyplot as plt

class VentanaLogin(QMainWindow):
    def __init__(self, controlador):
        super().__init__()
        loadUi("Ingreso.ui", self)
        self.setup()
        self.__mi_controlador = controlador

    def setup(self):
        self.pushButton.clicked.connect(self.ingresar)
        self.salir.clicked.connect(self.close)
        self.label_image = self.findChild(QLabel, 'logo')
        self.label_logo = self.findChild(QLabel, 'UdeA')

        # Imágen para la ventana con el logo de la UdeA
        if self.label_image is not None:
            image_path = 'UdeAlogo.png'  
            pixmap = QPixmap(image_path)
            self.label_image.setPixmap(pixmap)
            self.label_image.setScaledContents(True)  

        if self.label_logo is not None:
            image_pathl = 'UdeA+simplificado+®-01.png'  
            pixmap = QPixmap(image_pathl)
            self.label_logo.setPixmap(pixmap)
            self.label_logo.setScaledContents(True)  

    def ingresar(self):
        login = self.user.text()
        password = self.password.text()
        resultado = self.__mi_controlador.validarUsuario(login, password)
        if resultado:
            self.__mi_controlador.mostrarVentanaDicom()
        else:
            texto = "Usuario o contraseña incorrecto."
            msj = QMessageBox(self)
            msj.setIcon(QMessageBox.Warning)
            msj.setText(texto)
            msj.setWindowTitle("Alerta")
            msj.show()

    def ventanaDicom(self):
        ventanad = VentanaDicom(self.__mi_controlador)  
        self.hide()
        ventanad.show()

    def setControlador(self, c):
        self.__mi_controlador = c

class VentanaDicom(QMainWindow):
    def __init__(self, controlador, modelo):
        super().__init__()
        loadUi("Dicom.ui", self)
        self.modelo = modelo
        self.__mi_coordinador = controlador

        self.modelo.cargarCarpetas()
        self.carpetas.addItems(self.modelo.carpetas)
        self.carpetas.currentIndexChanged.connect(self.cargarCarpetas)
        self.slider.valueChanged.connect(self.cambiarImagen)
        self.cerrar.clicked.connect(self.close)
        self.cargarCarpetas()

    def cargarCarpetas(self):
        carpeta_seleccionada = self.carpetas.currentText()
        imgsel = self.modelo.imagenesDicom.get(carpeta_seleccionada)
        self.slider.setRange(0, len(imgsel) - 1)
        rutaimg = os.path.join(os.getcwd(), imgsel[1])
        dicom = pydicom.dcmread(rutaimg)
        fab = dicom.get("Manufacturer", "Desconocido")
        mod = dicom.get("ManufacturerModelName", "Desconocido")
        gen = dicom.get("PatientSex", "Desconocido")
        esp = dicom.get("SliceThickness", "Desconocido")
        part = dicom.get("BodyPartExamined", "Desconocida")

        fabricante = self.findChild(QLabel, "fabricante")
        fabricante.setText(f"{fab}")
        modelo = self.findChild(QLabel, "modelo")
        modelo.setText(f"{mod}")
        genero = self.findChild(QLabel, "genero")
        genero.setText(f"{gen}")
        espesor = self.findChild(QLabel, "espesor")
        espesor.setText(f"{esp}")
        parte = self.findChild(QLabel, "parte")
        parte.setText(f"{part}")

        if imgsel:
            self.current_image_index = 0
            self.cambiarImagen(self.slider.value())

    def cambiarImagen(self,nuevoslider):
        carpeta_seleccionada = self.carpetas.currentText()
        imgsel = self.modelo.imagenesDicom.get(carpeta_seleccionada)
        if imgsel and 0 <= nuevoslider < len(imgsel):
            rutaimg = os.path.join(os.getcwd(), imgsel[nuevoslider])
            dicom = pydicom.dcmread(rutaimg)
            pixel_array = dicom.pixel_array
            self.label = self.findChild(QLabel, 'label')
            image = QImage(pixel_array, pixel_array.shape[1], pixel_array.shape[0],QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(image) 
            self.label.setPixmap(pixmap)

    def setControlador(self, c):
        self.__mi_coordinador = c

