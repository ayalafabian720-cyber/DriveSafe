import json
import os
from pathlib import Path

#para leer los archivos json

def leer_json(ruta):

    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = Path(__file__).resolve().parent / ruta
    if not ruta.exists():
        return[]

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
 #definimos la funcion para guardar cambios en los archivos json   

def guardar_json (ruta, datos):

    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = Path(__file__).resolve().parent / ruta
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos ,archivo, indent=4, ensure_ascii=False)

#vamos a definir la funcion para validar documentos

def validar_documento(ruta, documento):
    #estoy haciendo la lista con los datos del json para compararlo con el documento
    lista=leer_json(ruta)
    #lo que hacemos es filtrar y tomar unicamente el documento
    lista_documento=[i['documento'] for i in lista ]

    while documento in lista_documento :
        print("¡EY! documento ya registrado")
        documento=int(input("Por favor ingrese nuevamente el documento"))

    return documento

#Esta función es para validar el documento, para ver que esté registrado

def validar_documento_registrado(ruta,documento):
    lista=leer_json(ruta)
    documentos=[i['documento']for i in lista]
    while documento not in documentos:
        print("No hay documentos registrados")
        documento=int(input("Por favor ingrese nuevamente el documento: "))

    return documento

# fUNCIONES PARA VALIDAR LAS PLACAS que no esten duplicadas

def validar_placa (ruta,placa):
    #Leemos el archivo de los vehiculos
    lista=leer_json(ruta)
    #Listar las placas
    placas=[p["placa"] for p in lista]
    while placa in placas:
        print(f"'--- YA SE ENCUENTRA REGISTRADO UN VEHICULO CON LA PLACA: '{placa}")
        placa = input("Ingrese una placa valida: ").upper()

    return placa

#Funcion para validar que la placa si este registrada
def validar_placa_registrada(ruta,placa):
    #Leemos los vehiculos
    lista=leer_json(ruta)
    #Filtramos solo por placas
    placas=[i["placa"]for i in lista]
    #validamos que este registrada la placa
    while placa not in placas:
        print(f"La placa: {placa}, no se encuentra registrada")
        placa=input("Ingrese una placa que este registrada: ").upper()
    return placa

#Funcion para validar fecha

def validar_fecha_y_hora (ruta,fecha,hora):
    lista=leer_json(ruta)

    #Se crea una lista con los horarios disponibles
    horarios={(p["fecha"], p["hora"]) for p in lista}

    #Validamos la disponibilidad de la fecha
    while (fecha,hora) in horarios :
        print("---- HORARIO NO DISPONIBLE ----")
        print(f"'La fecha:'{fecha}' No se encuentra disponible en la hora: '{hora} ' ")
        fecha= input ("Ingrese una fecha valida: ")
        hora= input("Ingrese una hora valida: ")

    return fecha,hora,

#Funcion para validar disponibilidad del vehiculo 
def validar_dia_vehiculo (ruta,fecha,hora,placa):
    lista=leer_json(ruta)
    #Creamos la lista de los vehiculos que estan ocupados 
    vehiculos_ocupados= {(p["fecha"],p["hora"],p["placa"])for p in lista}

    # Validamos la disponibilidad del vehiculo
    while (fecha,hora,placa) in vehiculos_ocupados:
        print("---- VEHICULO NO DISPONIBLE ----")
        print(f"'El vehiculo de placa: '{placa} 'No se encuentra disponible en la fecha:' {fecha} 'En la hora: '{hora} ")
        fecha = input("Ingrese una fecha valida: ")
        hora = input("Ingrese una hora valida: ")

    return fecha, hora, placa 

# Alias de compatibilidad con la importacion de citas
def validar_dis_vehiculo(ruta, fecha, hora, placa):
    return validar_dia_vehiculo(ruta, fecha, hora, placa)

# Funcion para filtrar un usuario por documento
def filtrar_usuario(ruta, documento):
    lista=leer_json(ruta)
    for usuario in lista:
        if usuario.get("documento") == documento:
            return usuario
    return None

# Funcion para filtrar un vehiculo por placa
def fitrar_vehiculo(ruta, placa):
    lista=leer_json(ruta)
    for vehiculo in lista:
        if vehiculo.get("placa") == placa:
            return vehiculo
    return None



