import PySimpleGUI as sg
import googletrans
from googletrans import Translator
import threading
import webbrowser
from deteccionTextos import texto
#import cv2
translator = Translator()
class traductor:
    def __init__(self):
        self.datos_lenguajes = googletrans.LANGUAGES
      
        self.frame_de = [
            [sg.Multiline(default_text=texto, disabled=True, size=(40, 20), key='-txt_a_traducir_')]
        ]
        frame_a = [
            [sg.Multiline(disabled=True, size=(40, 20), key= '-txt_traduccion_0')]
        ]
        lenguajesA = ['Detectar idioma']
        lenguajesB = []
        for lenguaje in self.datos_lenguajes.values():
            lenguajesA.append(lenguaje)
            lenguajesB.append(lenguaje)
        #lenguajes= self.lenguajes.keys()
        #print(lenguajes)
        frame_lenguajes = [
            [sg.Text('De')],
            [sg.Combo(values= lenguajesA, key='-lenguaje_de-', default_value='Detectar idioma')],
            [sg.Text('A')],
            [sg.Combo(values=lenguajesB, key='-lenguaje_a-', default_value= 'english')],
            [sg.Button('Traducir', key='-traducir-')]
        ]

        self.layout_traductor = [[sg.Text('Traductor')],
                                 [sg.Frame('Texto a traducir', self.frame_de,  ), sg.Frame('Lenguajes', frame_lenguajes),  sg.Frame('Texto Traducido', frame_a)
                                 ], 
                                 ]
        self.frame_about = [
            [sg.Text('Generales', font='Any 20', justification='c')],
            [sg.Text(
                'Información de la app\n'
                'Forma De uso: Ingresar img y luego elegir el idioma de la img y el idioma a traducir requerido.\n'
                '', )],
        ]

        self.estado_traduccion =  False
        self.texto_traduccion = ''

    def traducir(self, texto, de, a):
        self.estado_traduccion =  True
        try:
            traduccion = translator.translate(text=texto, src=de, dest = a)
            self.estado_traduccion = False
            return traduccion.text
        except:
            self.estado_traduccion = False
            self.texto_traduccion = "Error en la traduccion"
        #for translation in traduccion:
        #    return translation.text

    def getKeyIdioma(self, lenguaje):
        for valores in self.datos_lenguajes.items():
            if valores[1]==lenguaje:
                return valores[0]
    def detectar_idioma(self, texto, a):
        self.estado_traduccion =  True
        try:
            traduccion =  translator.translate(text=texto, dest = a)
            self.estado_traduccion = False
            self.texto_traduccion = traduccion.text
        except:
            self.estado_traduccion = False
            self.texto_traduccion = "Error en la traduccion"

    def iniciar_ejecucion(self):
        tab3 = sg.Tab('Traductor', self.layout_traductor, tooltip='Eventos', title_color='red')
        tab4 = sg.Tab('Acerca de', self.frame_about , tooltip="Aclaraciones", title_color='red')
        layout = [
            [sg.TabGroup([[tab3, tab4]], key='_TAB_GROUP_', )]
        ]
        window = sg.Window('Traductor IMG', layout)
        traduccion = window['-txt_traduccion_0']

        while True:
            event, value = window.read(10)
            #print(value)
            #print("dasdasd")
            if event in ('Exit', None):
                window.close()
                break

            if self.texto_traduccion != '':
                #print("asdasd")
                traduccion.update(self.texto_traduccion)
                self.texto_traduccion = ''
            if event == '-traducir-':
                if value['-lenguaje_de-'] == 'Detectar idioma':
                    a = self.getKeyIdioma(value['-lenguaje_a-'])
                    #texto_traduccion = self.detectar_idioma(value['-txt_a_traducir_'], a = a)
                    #traduccion.update(texto_traduccion)
                    d = threading.Thread(target=self.detectar_idioma, args=(value['-txt_a_traducir_'], a,),
                                         daemon=False)
                    d.start()
                else:
                    de = self.getKeyIdioma(value['-lenguaje_de-'])
                    a = self.getKeyIdioma(value['-lenguaje_a-'])
                    #texto_traduccion = self.traducir(value['-txt_a_traducir_'], de = de, a = a)
                    #traduccion.update(texto_traduccion)
                    d = threading.Thread(target=self.traducir, args=(value['-txt_a_traducir_'],de, a,),
                                         daemon=False)
                    d.start()             
           
traductor = traductor()
traductor.iniciar_ejecucion()