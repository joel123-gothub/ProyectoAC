#                  deteccion de textos en img para su traducción requerida utilizando OpenCV + pytessseract

import cv2
import numpy as np
import pytesseract #reconocimiento de caracteres(texto)
from googletrans import Translator
translator = Translator()

pytesseract.pytesseract.tesseract_cmd = r'D:\ING.SISTEMAS\Tesseract-OCR\tesseract.exe'
#ordenación 4 vertices
def ordenar_puntos(puntos):
    n_puntos = np.concatenate([puntos[0], puntos[1], puntos[2], puntos[3]]).tolist()

    y_order = sorted(n_puntos, key=lambda n_puntos: n_puntos[1]) #vert. Y (iz->der.)

    x1_order = y_order[:2] #2 primeros puntos(coordenadas) son vert. sup.
    x1_order = sorted(x1_order, key=lambda x1_order: x1_order[0]) #vert. sup. X (iz->der.)

    x2_order = y_order[2:4] #2 ultimos puntos son vert. inf.
    x2_order = sorted(x2_order, key=lambda x2_order: x2_order[0]) #vert. inf. X (iz->der.)
    
    return [x1_order[0], x1_order[1], x2_order[0], x2_order[1]]

image = cv2.imread('img_01.jpeg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #escala grises
#cv2.imshow('gray' ,gray)

canny = cv2.Canny(gray, 10, 150) #deteccion bordes
canny = cv2.dilate(canny, None, iterations=1)
#cv2.imshow('canny' ,canny)

cnts = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #deteccion contornos img
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

for c in cnts:
    epsilon = 0.01*cv2.arcLength(c,True) #delimitar figura(rect.) de contorno img
    approx = cv2.approxPolyDP(c,epsilon,True) #num. vertices rect.
    
    if len(approx)==4: #if detección rect.
        cv2.drawContours(image, [approx], 0, (0,255,255),2) #dibujar contorno
        
        puntos = ordenar_puntos(approx)

        #dibujar circunferencias en coordenadas ordenados
        cv2.circle(image, tuple(puntos[0]), 7, (255,0,0), 2) #azul
        cv2.circle(image, tuple(puntos[1]), 7, (0,255,0), 2) #verde
        cv2.circle(image, tuple(puntos[2]), 7, (0,0,255), 2) #rojo
        cv2.circle(image, tuple(puntos[3]), 7, (255,255,0), 2) #celeste    
        
        #perpectiva
        pts1 = np.float32(puntos) #arr = 4 coord. originales
        pts2 = np.float32([[0,0],[270,0],[0,310],[270,310]]) #arr = 4 coord. destino (270=ancho; 310=alto)
        M = cv2.getPerspectiveTransform(pts1,pts2) #obtencion matriz
        dst = cv2.warpPerspective(gray,M,(270,310)) #transformación de perspectiva(img alineada)
        cv2.imshow('dst', dst)

        #reconocimiento de texto
        texto = pytesseract.image_to_string(dst, lang='spa') #extraccion txt
        
        print('texto: ', texto) #imprime

        info = translator.translate(texto,dest='en') #almacena txt traducido segun dest
        print('Traduccion: ', info.text) #imprime

cv2.imshow('Image' ,image)
cv2.waitKey(0)
cv2.destroyAllWindows()