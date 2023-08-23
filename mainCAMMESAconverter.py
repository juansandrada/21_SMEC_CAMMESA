import csv
from datetime import datetime, timedelta

#########################################
# Software: "mainCAMMESAconverter.py"   #
# Autor: Juan Segundo Andrada           #
# Version: 1.00                         #
# Fecha de creación: 28/07/2020         #
# Descripción: convierte los archivos   #
# crudos bajados de los SMEC al         #
# formato requerido por CAMMESA         #
#########################################



def convertirArchivo(archivo):

    # Abrir el archivo en modo lectura
    contLinea = 0
    datos = []
    fecha = ""
    cadena_fecha = ""
    archivoSalida = ""
    nombre_archivo = "Archivos de Entrada/" + archivo
    #Esta es una modificacion
    
    with open(nombre_archivo, "r") as archivo:
        linea = archivo.readline()
        while linea:
            linea = archivo.readline()
            lineaAux = linea.split("\t")
            contLinea += 1
            if (contLinea==1):
                datos.append([lineaAux[1],"Kwh",""])
                archivoSalida = "Archivos de Salida/" + lineaAux[1] + ".txt"
            if (contLinea==2):
                datos.append(["Fecha","CANAL 1","CANAL 2"])
                ## Convertir la cadena en un objeto datetime
                aux = lineaAux[0]
                aux = aux[1:]
                MesDia = aux.split("/")
                mes = int(MesDia[0])
                dia = int(MesDia[1])
                yyhh = MesDia[2].split(" ")
                anio = int(yyhh[0])
                cadena_fecha = f'{dia:02d}'
                cadena_fecha += f'/{mes:02d}'
                cadena_fecha += f'/{anio+2000:04d}'
                datos.append([cadena_fecha + " " + yyhh[1],lineaAux[1],lineaAux[2]])
            if (contLinea>2) and (contLinea<97):
                datos.append([cadena_fecha + " " + lineaAux[0],lineaAux[1],lineaAux[2]])
            if (contLinea==97):
                # Definir el formato de la cadena de fecha
                formato = '%d/%m/%Y'
                # Convertir la cadena en un objeto datetime
                fecha = datetime.strptime(cadena_fecha, formato)
                fecha = fecha + timedelta(days=1)
                cadena_fecha = f'{fecha.day:02d}/{fecha.month:02d}/{fecha.year:04d}'
                datos.append([cadena_fecha + " 00:00",lineaAux[1],lineaAux[2]])

    # Abrir el archivo en modo escritura
    with open(archivoSalida, mode="w", newline="") as archivo_csv:
        # Crear un objeto escritor CSV
        escritor = csv.writer(archivo_csv, delimiter="\t")
        # Escribir los datos en el archivo CSV
        for fila in datos:
            escritor.writerow(fila)

    print("Datos escritos en el archivo CSV: " + archivoSalida)        


convertirArchivo("SMNEM21P.txt")
convertirArchivo("SMNEM22P.txt")
convertirArchivo("SMNEM23P.txt")
convertirArchivo("SMNEM24P.txt")
convertirArchivo("SMNEC25P.txt")

