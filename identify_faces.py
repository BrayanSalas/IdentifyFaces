from tkinter import *
import os, sys
from PIL import Image
import tensorflow as tf
import cv2
import time
def Cerrar():
    exit()
def TomarFoto():
    
    #Declarando el grado de mensajes que mandará la consola, el nivel 2 añade "WARNING" como filtro de los log error.
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # Obtiene el valor ingresado por el usuario despues de la ejecución
    # Por ejemplo: python identify_guitars.py image.jpg
    # El argumento de ruta sería image.jpg
    ruta = "foto.jpg"
    #Abre la imagen, en caso de que no se encuentre, manda el tipo de error y dice el error al usuario.
    try:
        abrirImagen = Image.open(ruta)
        abrirImagen.show()    
    except OSError as err:
        print("OS error: {0}".format(err))
        print("NO SE ENCUENTRA EL ARCHIVO SOLICITADO")

    # Se lee la imagen dicha anteriormente con la ejecución del código
    image_data = tf.gfile.FastGFile(ruta, 'rb').read()

    # Se lee el archivo que contiene las carpetas, este archivo se crea cuando se entrena con el machine learning de retrain.py
    # Por ejemplo en este contiene lo que son las marcas de guitarra Jackson Fender Epiphone Schecter
    label_lines = [line.rstrip() for line 
                    in tf.gfile.GFile("retrained_labels.txt")]

    # Abriendo el grafico re-entrenado
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    #Se abre una sesion de tensorflow, la neurona principal
    with tf.Session() as sess:
        # Comprueba la imagen dada con los grafico y hace una predicción
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})
        
        # Ordena las predicciones en orden de puntuacion
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        # Codigo para imprimir el resultado de la predición con su puntuación
        i = 0
        auxPuntuacion = 0
        nombre = []
        puntuacion = []
        #Almacena el nombre de la carpeta en human_string y la puntuacion obtenida en score, luego estas son almacenadas en arreglos
        #para su comparacion
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            nombre.append(human_string)
            puntuacion.append(score)
            i = i + 1
        #Comparacion de puntuaciones segun la predicción(SI SE AGREGAN MAS CARPETAS, CAMBIAR EL NUMERO DE 0 HASTA EL NUMERO DE CARPETAS)
        for i in range(0, 2):
            if(puntuacion[i] > auxPuntuacion):
                auxPuntuacion = puntuacion[i]
                auxNombre = nombre[i]
        #Imprime la marca 
        print('La persona es: %s y su porcentaje de acierto es de: %.5f' % (auxNombre.capitalize(), auxPuntuacion))
        usuario.set(auxNombre.capitalize())

ventana = Frame(height=150, width=300)
ventana.pack(padx=20,pady=20)
textViewUser = Label(text="Usuario: ", font=("Arial", 15)).place(x=0,y=15)

usuario = StringVar()
editTextUser = Entry(ventana, textvariable=usuario).place(x=70, y=0)

btnTomarFoto = Button(ventana, command=TomarFoto,text="Reconocimiento Facial").place(x=0, y=70)
btnAceptar = Button(ventana, command=Cerrar, text="Cerrar").place(x=0, y=120)



ventana.mainloop()