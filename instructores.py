#importamos las funciones
from funciones import guardar_json, leer_json, validar_documento, validar_documento_registrado
RUTA_INSTRUCTOR="Data/instructor.json"

# definimos la funcion para instructores 
def listar_instructores():
    instructores= leer_json(RUTA_INSTRUCTOR)
    if not instructores:
            print("No hay instructores registrados")
    print(f"\n {'documento' :<20}{'nombre' :<20}{'especialidad' :<8}")
    print("-"*50)
    
    for i in instructores:
            print(f"{i['documento']:<20}{i['nombre']:<20}{i['especialidad']:<8}")

def actualizar_instructor():
   lista_cliente=leer_json(RUTA_INSTRUCTOR)
   listar_instructores()

   print("===Por favor ingrese los datos del instructor que desea actualizar===")
   documento=int(input("Por favor ingrese el documento: "))
   validar_documento_registrado(RUTA_INSTRUCTOR, documento)
   for i in lista_cliente:
       if i['documento']==documento:
           print("Por favor ingrese los datos que vas a actualizar")
           documento=input(f"Su actual documento es: ({i['documento']}), o enter para dejar igual: ")
           documento=validar_documento(RUTA_INSTRUCTOR, documento)
           nombre=input(f"Su actual nombre es: ({i['nombre']}), o enter para dejar igual: ")
           tipo=int(input("Ingrese 1. si es carro 2. si es moto"))
           while tipo <1 or tipo >2:
               print("¡EY estas ingresando un numero no valido")
               print("Vuelva a ingresar un dato correcto 1 / 2 :")
               tipo=int(input("Ingrese otra vez el tipo de vehiculo: "))
           if tipo==1:
             especialidad="carro"
           else:
              especialidad="moto"
        
           i["documento"]=documento if documento else i["documento"]
           i["nombre"]=nombre if nombre else i["nombre"]
           i["especialidad"]=especialidad if especialidad else i["especialidad"]

           guardar_json(RUTA_INSTRUCTOR, lista_cliente)
           print("===¡HA SIDO ACTUALIZADO CORRECTAMENTE!===")

def guardar_instructor():
    datos_instructor=leer_json(RUTA_INSTRUCTOR)

    print("===DATOS INSTRUCTOR===")
    documento=int(input("Por favor ingrese su documento: "))
    documento=int(validar_documento(RUTA_INSTRUCTOR, documento))
    nombre=str(input("Por favor ingrese su nombre: "))
    print("Para el tipo de especialidad ingrese")
    op=int(input("1. carro / 2. moto: "))

    while op < 1 or op >2 :
        print("Ingreso una opcion no valida")
        op=int(input("1. carro / 2. moto: "))
    if op ==1:

        tipo="carro"
    else:
        tipo="moto"
    
    datos_instructor.append ({
        "documento": int (documento),
        "nombre": nombre,
        "especialidad": tipo
    })

    guardar_json(RUTA_INSTRUCTOR, datos_instructor)

def eliminar_instructor():
    lista_cliente=leer_json(RUTA_INSTRUCTOR)
    listar_instructores()
    documento=int(input("Por favor ingrese el documento del instructor que desea eliminar: "))
    documento=validar_documento_registrado(RUTA_INSTRUCTOR, documento)
    #aqui van a estar todos los usuarios excepto al que voy a eliminar
    lista_filtrada=[i for i in lista_cliente if i["documento"] != documento]
    guardar_json(RUTA_INSTRUCTOR, lista_filtrada)
    print("¡Instructor eliminado exitosamente!")

def menu_instructor():
    while True:
        print("===Ingrese la opción segun lo que deseas realizar===")
        print("1. Listar instructor")
        print("2. Guardar instructor")
        print("3. Actualizar instructor")
        print("4. Eliminar instructor")
        print("5. salir")
        op=int(input("Por favor ingrese su opcion: "))

        match op:
            case 1:
                listar_instructores()
            case 2:
                guardar_instructor()
            case 3:
                actualizar_instructor()
            case 4: 
                eliminar_instructor()
            case 5:
                print("Gracias por usar el sistema...saliendo")
                break
                
            case _:
                print("Has ingresado una aopcion no valida")
                op=int(input("Por favor ingrese una opción valida (1-5)"))

