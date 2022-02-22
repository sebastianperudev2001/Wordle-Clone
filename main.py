# -*- coding: utf-8 -*-

#Librerias necesarias
import requests as req
from random import randint
import os
import json
import datetime
import colored
from colored import stylize 

#Variables Globales
teclado = ""

"""
Estas estructuras de datos me serán útiles principalmente para poder 
hacer referencia como el estado de cada letra de las palabras ingresadas
y así poder generar la tabla de respuestas y el teclado
"""
#Diccionario, porque se pueden repetir letras en distintas ubicaciones
right_words = {}
#Por lo demas sets para evitar valores repetidos
misplaced_words = set()
wrong_words = set()

intentos = 0
tablaRespuesta = ["+---+---+---+---+---+"] 

palabrasFiltradas = []

resumen = []


"""
Se utiliza una librería para poder así descargar el contenido txt del repo 
github en formato raw (no directamente de GH)
Se crea un archivo en el que se escrite todo el texto conseguido
"""
def descargarPalabras():
    """
    https://stackoverflow.com/questions/14120502/how-to-download-and-write-a-file-from-github-using-requests
    """
    url = 'https://raw.githubusercontent.com/javierarce/palabras/master/listado-general.txt'
    res = req.get(url)
    file = open("filename.txt", "w")
    file.write(res.text)
    file.close()

"""
A partir del primer filtro se utiliza randint para elegir un numero al azar
dentro del rango de 0 a la longitud de la lista, 
así se pueden seleccionar palabras al azar de 
la lista generada y se retorna una lista de 365 elementos al azar
"""
def seleccionarPalabras(lista):
    with open("palabras5.txt", "w") as f:
        for i in range (0, 365):
            value = randint(0, len(lista)-1)
            element = lista[value]
            f.write(element + '\n')

    f.close()


"""
Se abre el archivo generado y se crea una lista en la que se agregan todas las
palabras de 5 letras (quitando el salto de linea) y se retorna el primer filtro
"""
def filtrarPalabras():
    palabras = open("filename.txt","r")
    palabrasSeleccionadas = []
    for line in palabras:
        sizeWord = len(line) - 1
        if (sizeWord ==5):
            palabrasSeleccionadas.append(quitarTildes(line.rstrip('\n'))) 
    return palabrasSeleccionadas
            

def generarListaPalabrasJuego():
    palabras = open("palabras5.txt","r")
    palabrasJuego = []
    for line in palabras:
        palabrasJuego.append(line.rstrip('\n'))
    return palabrasJuego

def seleccionarPalabraAlAzar(lista):
   
    fecha = datetime.datetime.today().strftime('%Y-%m-%d')  
    archivo = 'palabras_por_fecha.json'
    
    with open(archivo, "r") as file:
        data = json.load(file)
    
    fechas_json = list(data.keys())
    
    if(fecha in fechas_json):
        return data[fecha]
    else:
        palabras_usadas = list(data.values())
        while (True):
            numero = randint(0, len(lista) - 1)
            potencial_palabra = lista[numero]
            if(potencial_palabra not in palabras_usadas):
                break
        data[fecha] = potencial_palabra
        with open(archivo, 'w') as palabrasFecha:
            json.dump(data,palabrasFecha)
        
    return potencial_palabra

def solicitarInputUsuario():
    global palabrasFiltradas
    #Normalizar ambas palabras
    
    while(True):
        try:
            palabra = input("Ingrese palabra: ").strip()
            palabra = quitarTildes(palabra)
            if(len(palabra)== 5 and palabra.isalpha()):
                if (palabra in palabrasFiltradas):
                    break
                else: 
                    print("{} no es una palabra en la Base de datos".format(palabra))
            else:
                print("{} no es una palabra de 5 letras valida".format(palabra))
        except ValueError as errorValor:
            print("{} no es una palabra valida".format(errorValor))
    return palabra
    


def imprimirTabla():
    global tablaRespuesta
    counter = 0
    for linea in tablaRespuesta:
        if(linea != "+---+---+---+---+---+"):
            counter += 1
        print(linea)
    if(counter != 6):
        diferencia = 6 - counter
        for i in range(0, diferencia):
            print("|   |   |   |   |   |")
            print("+---+---+---+---+---+")



def generarTablaRespuestas(palabra):
    global tablaRespuesta
    global resumen
    global right_words
    global intentos
    counter = 0
    lineaTabla = "|"
    linea_resumen = ""
    
    marron = u"\U0001F7EB"
    amarillo = u"\U0001f7e8"
    verde = u"\U0001f7e9"

    for letra in palabra:
        if ((letra in right_words) and (counter in right_words[letra])):
            lineaTabla  += stylize("{}{}{}".format("=",letra,"="),colored.bg("green")+ colored.fg("black"))+"|"
            linea_resumen += verde
        elif(letra in misplaced_words):
            lineaTabla  += stylize("{}{}{}".format("<",letra,">"), colored.bg("yellow")+ colored.fg("black")) + "|"
            linea_resumen += amarillo
        elif(letra in wrong_words):
            lineaTabla  += stylize("{}{}{}".format(">",letra,"<"),colored.bg("dark_gray")+ colored.fg("black")) + "|"
            linea_resumen += marron

        counter += 1
    resumen.append(linea_resumen)
    tablaRespuesta.append(lineaTabla)
    tablaRespuesta.append("+---+---+---+---+---+")
   
    

"""
El enfoque que se debe dar es tener listas globales en las que se
almacene las letras las letras segun su condicion y a partir de esas
generar un output bonito asi
"""
def generarTeclado(): 
    
    alfabeto = ['Q','W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 
                'A', 'S','D','F','G','H','J','K','L','Ñ',
                'Z','X','C','V','B','N','M']
    global teclado
    teclado = ""
    
    global right_words
    global misplaced_words
    global wrong_words
    
    
    counter = 0
    for letra in alfabeto:
        if (counter%10 ==0):
            teclado += '\n'
        if(letra == 'Z'):
            teclado += '\t'
        if (letra in right_words):
            teclado += stylize(" [={}=] ".format(letra), colored.bg("green") + colored.fg("black"))
        elif(letra in misplaced_words):
            teclado += stylize(" [<{}>] ".format(letra), colored.bg("yellow") + colored.fg("black"))
        elif(letra in wrong_words):
            teclado += stylize(" [>{}<] ".format(letra), colored.bg("dark_gray") + colored.fg("black"))
        else:
            teclado += stylize(" [ {} ] ".format(letra), colored.bg("white") + colored.fg("black") )
        counter += 1

      
          
def quitarTildes(palabra):
    reemplazos = (
        ('á','a'),
        ('é','e'),
        ('í','i'),
        ('ó','o'),
        ('ú','u'),
        )
    for a,b in reemplazos:
        palabra= palabra.replace(a,b).replace(a.upper(), b.upper())
    return palabra.upper()


def verificacionPalabras(palabraUsuario, palabraOculta):
   
    global resumen
    global right_words
    global misplaced_words
    global wrong_words
        
    listaUsuario = list(palabraUsuario)
    listaOculta = list(palabraOculta)
    lenOculto = len(listaOculta)
    lenUsuario = len(listaUsuario)
    
    
    for j in range(0, lenUsuario):
        letraUser = listaUsuario[j]
        for i in range(0, lenOculto):    
            letraOculta = listaOculta[i]   
            if (letraOculta == letraUser) and (i == j):
                #En caso ya exista un valor se appendea
                if(letraUser in right_words):
                    right_words[letraUser].add(j)
                #Sino se crea
                else:
                    right_words[letraUser] = {j}
                break
            elif(listaUsuario[j] in listaOculta):
                misplaced_words.add(letraUser)
            else: 
                wrong_words.add(letraUser)
                break

    os.system('cls')
    generarTeclado()
    generarTablaRespuestas(palabraUsuario)
    imprimirTabla()
    print(teclado) 
    
    if (palabraUsuario == palabraOculta):
        return 1

    

def registrarPartida(palabra, palabrasUsuario):
 
    archivo = 'partidas.json'
    with open(archivo, "r") as file:
        data = json.load(file)
    
    horaDia = datetime.datetime.now(datetime.timezone.utc)
    horaDia.isoformat()
    horaDia = str(horaDia)
    data[horaDia] = {'PalabraAdivinar': palabra,
                     'PalabrasIntentos': palabrasUsuario}
    
    with open(archivo, 'w') as palabrasFecha:
        json.dump(data,palabrasFecha)

    
def generarJsonPartida():
    with open('partidas.json', 'w') as f:
        json.dump({},f)
    

def generarResumen(resumen): 
    print("##########  RESUMEN DE PARTIDA   ##########")
    counter = 0
    for element in resumen:
        print(element)
        counter += 1

    diferencia = 6-counter
    marron = u"\U0001F7EB"
    relleno = marron*5
    for i in range(0, diferencia):    
        print(relleno)
    
    print("GRACIAS POR JUGAR")

def jugarPartida():
    #Generas una lista a partir del txt con las 365 palabras al azar
    listaPalabras = generarListaPalabrasJuego()
    
    
    #Se selecciona la palabra misteriosa
    palabraDescubrir = seleccionarPalabraAlAzar(listaPalabras)
    #print(palabraDescubrir)
    #El usuario ingresa su palabra
    global intentos 
    palabrasUsuario = []
    for i in range(0,6):
        intentos += 1
        inputUsuario = solicitarInputUsuario()
        
        palabrasUsuario.append(inputUsuario)
        if (verificacionPalabras(inputUsuario,palabraDescubrir) == 1):
            break
    registrarPartida(palabraDescubrir, palabrasUsuario)
    generarResumen(resumen)

        



def generarJSON():
    
    archivo = 'palabras_por_fecha.json'
    data_ejemplo = {'2022-01-19':'ALDEA', '2022-01-18':'AUTOR', 
                    '2022-01-17':'CREDO', '2022-01-16':'OJETE',
                    '2022-01-15':'SARDA', '2022-01-14':'FUGAR',
                    '2022-01-13':'FERAZ', '2022-01-12':'ADIVE',
                    '2022-01-11':'POEMA', '2022-01-10':'POLLA'}
    with open(archivo, 'w') as palabrasFecha:
        json.dump(data_ejemplo,palabrasFecha)

def main():
    global palabrasFiltradas
    os.system('cls')
    print("""
    #####################################################

        WELCOME TO WORDLE
        made by: Sebastián Chávarry

    #####################################################""")
    while (True):
        try:
            configuracion_inicial = input(""" 
            ¿Qué opción le gustaría tomar?
            [1] Jugar desde 0
            [2] Jugar usando archivos existentes \n""")
            if(configuracion_inicial == '1'):
                #Descargas palabras de la URL y creas un txt con todas
                descargarPalabras()
                #Creas JSON con archivos de prueba
                generarJSON()
                generarJsonPartida()
                break 
            elif(configuracion_inicial == '2'):
                if(os.path.isfile('filename.txt') and os.path.isfile('partidas.json') and os.path.isfile('palabras_por_fecha.json')):    
                    break
                else:
                    print("No se puede elegir esta opción, porque no existe todavía la BD")
            else: 
                print("Ingrese 1 o 2 >:(")
        except ValueError as error:
            print("{} no es una opción válida".format(error))
    
    #Filtras todas las palabras que cumplen con el requisito
    palabrasFiltradas = filtrarPalabras()
    #Generas un txt al azar de 365 palabras
    seleccionarPalabras(palabrasFiltradas)    
    jugarPartida()


main()