from Tkinter import *
import Tkinter as tk
import tkMessageBox
import os, sys
from PIL import Image
import tensorflow as tf
import time
import picamera
root = Tk()
def Informacion():
    text1 = Text(root, height=20, width=30)
    photo=PhotoImage(file='./foto.gif')
    text1.insert(END,'\n')
    text1.image_create(END, image=photo)
    text1.pack(side=LEFT)
    text2 = Text(root, height=20, width=50)
    scroll = Scrollbar(root, command=text2.yview)
    text2.configure(yscrollcommand=scroll.set)
    text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    text2.tag_configure('big', font=('Verdana', 20, 'bold'))
    text2.tag_configure('color', foreground='#476042', 
                            font=('Arial', 12, 'bold'))
    text2.tag_bind('follow', '<1>', lambda e, t=text2: t.insert(END, "Not now, maybe later!"))
    text2.insert(END,'\n\tModo de uso\n', 'big')
    quote = """
    Para la utilizacion del programa usted 
    debera permanecer quieto, tendra 7 segundos 
    para acomodarse frente a la camara
    procure tener la distancia recomendada para 
    fotos como se muestra a la izquierda
    y acomodar la cara lo mas al centro posible
    mirando de frente a la camara
    """
    text2.insert(END, quote, 'bold_italics')
    text2.insert(END, 'Link del proyecto:\n https://github.com/BrayanSalas/IdentifyFaces"', 'follow')
    text2.pack(side=LEFT)
    scroll.pack(side=RIGHT, fill=Y)

    root.mainloop()
def TomarFoto():
    with picamera.PiCamera() as picam:
	ruta = "foto.jpg"
	picam.start_preview()
	time.sleep(5)
	picam.capture(ruta)
	picam.stop_preview()
	picam.close()
	time.sleep(5)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    try:
        abrirImagen = Image.open(ruta)
        abrirImagen.show()    
    except OSError as err:
        print("OS error: {0}".format(err))
        print("NO SE ENCUENTRA EL ARCHIVO SOLICITADO")

    
    image_data = tf.gfile.FastGFile(ruta, 'rb').read()

    label_lines = [line.rstrip() for line 
                    in tf.gfile.GFile("retrained_labels.txt")]

    
    with tf.gfile.FastGFile("retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')

    
    with tf.Session() as sess:
    
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})
        
    
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
    
        i = 0
        auxPuntuacion = 0
        nombre = []
        puntuacion = []
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            nombre.append(human_string)
            puntuacion.append(score)
            i = i + 1
    
        for i in range(0, 3):
            if(puntuacion[i] > auxPuntuacion):
                auxPuntuacion = puntuacion[i]
                auxNombre = nombre[i]
    
        print('La persona es: %s y su porcentaje de acierto es de: %.5f' % (auxNombre.capitalize(), auxPuntuacion))
	if(auxPuntuacion < 0.95):
			tkMessageBox.showerror("Error", "Usuario no autorizado, intente denuevo")
	else:
			usuario.set(auxNombre.capitalize())
			tkMessageBox.showinfo("Bienvenido", "Usuario autorizado")
ventana = Frame(height=150, width=375)
ventana.pack(padx=20,pady=20)
textViewUser = Label(text="Bienvenido al sistema de reconocimiento facial", font=("Arial", 15)).place(x=205,y=15, anchor="center")

usuario = StringVar()
editTextUser = Entry(ventana, textvariable=usuario).place(x=130, y=40)

btnTomarFoto = Button(ventana, command=TomarFoto,text="Reconocimiento Facial").place(x=126, y=70)
btnInformacion = Button(ventana, command=Informacion, text="Leeme").place(x=167, y=120)

ventana.mainloop()
