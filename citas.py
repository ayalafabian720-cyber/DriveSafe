"""Módulo de citas de DriveSafe. Datos guardados en Data/citas.json."""
from datetime import datetime, timedelta
from pathlib import Path
from funciones import leer_json, guardar_json, filtrar_usuario, fitrar_vehiculo

DATA = Path(__file__).resolve().parent / "Data"
RUTA_CITAS = DATA / "citas.json"
RUTA_CLIENTES = DATA / "cliente.json"
RUTA_INSTRUCTORES = DATA / "instructor.json"
RUTA_VEHICULOS = DATA / "vehiculos.json"


def pedir_entero(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje).strip())
            if valor >= minimo:
                return valor
        except ValueError:
            pass
        print(f"Ingrese un número entero mayor o igual a {minimo}.")


def pedir_documento(ruta, rol):
    """Busca un registro; si es cliente, permite crearlo sin salir de la cita."""
    while True:
        documento = pedir_entero(f"Documento del {rol} (0 para cancelar): ", minimo=0)
        if documento == 0:
            print("Operación cancelada.")
            return None
        usuario = filtrar_usuario(ruta, documento)
        if usuario:
            return usuario
        if rol != "cliente":
            print(f"No existe un {rol} con ese documento. Regístrelo primero en su módulo o ingrese otro documento.")
            continue
        print("Este cliente aún no está registrado.")
        opcion = input("¿Desea registrarlo ahora? (S/N): ").strip().lower()
        if opcion not in ("s", "si", "sí"):
            print("Puede ingresar otro documento, o 0 para cancelar.")
            continue
        nombre = input("Nombre del nuevo cliente: ").strip()
        while not nombre:
            nombre = input("El nombre no puede estar vacío. Nombre: ").strip()
        while True:
            tipo = input("Tipo de vehículo (1. carro / 2. moto): ").strip()
            if tipo in ("1", "2"):
                break
            print("Seleccione 1 o 2.")
        # Releer antes de guardar para no sobrescribir otros registros.
        clientes = leer_json(ruta)
        usuario = next((u for u in clientes if str(u.get("documento")) == str(documento)), None)
        if usuario is None:
            usuario = {"documento": documento, "nombre": nombre,
                       "vehiculo": "carro" if tipo == "1" else "moto"}
            clientes.append(usuario)
            guardar_json(ruta, clientes)
            print("Cliente registrado correctamente. Continuamos con la cita.")
        return usuario


def pedir_vehiculo():
    vehiculos = leer_json(RUTA_VEHICULOS)
    if not vehiculos:
        print("No hay vehículos registrados. Registre uno primero.")
        return None
    while True:
        placa = input("Placa del vehículo: ").strip().upper()
        vehiculo = next((v for v in vehiculos if v['placa'].upper() == placa), None)
        if vehiculo:
            return vehiculo
        print("Esa placa no está registrada. Intente nuevamente.")


def fecha_hora(fecha, hora):
    """Admite horas de 12 h (2:00 pm) y de 24 h (14:00)."""
    fecha = fecha.strip()
    hora = ' '.join(hora.strip().lower().split())
    for formato in ("%d/%m/%Y %I:%M %p", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(f"{fecha} {hora}", formato)
        except ValueError:
            continue
    raise ValueError("Fecha u hora inválida. Use dd/mm/aaaa y 2:00 pm o 14:00.")


def hay_conflicto(citas, fecha, hora, duracion, id_instructor, placa, omitir_id=None):
    inicio = fecha_hora(fecha, hora)
    fin = inicio + timedelta(hours=duracion)
    for cita in citas:
        if cita['id'] == omitir_id:
            continue
        try:
            otro_inicio = fecha_hora(cita['fecha'], cita['hora'])
        except ValueError:
            continue
        otro_fin = otro_inicio + timedelta(hours=int(cita['duracion']))
        if inicio < otro_fin and otro_inicio < fin:
            if int(cita['id_instructor']) == int(id_instructor):
                return "El instructor ya tiene una cita en ese horario."
            if cita['placa'].upper() == placa.upper():
                return "El vehículo ya tiene una cita en ese horario."
    return None


def pedir_horario(citas, instructor, vehiculo, omitir_id=None, actuales=None):
    while True:
        fecha = input("Fecha (dd/mm/aaaa): ").strip()
        hora = input("Hora (ej. 2:00 pm o 14:00): ").strip()
        duracion = pedir_entero("Duración en horas: ")
        try:
            fecha_hora(fecha, hora)
            error = hay_conflicto(citas, fecha, hora, duracion, instructor['documento'], vehiculo['placa'], omitir_id)
            if error:
                print(error + " Pruebe otro horario.")
                continue
            return fecha, hora, duracion
        except ValueError as error:
            print(error)


def mostrar_cita(cita):
    print(f"ID: {cita['id']} | Cliente: {cita['nombre_usuario']} ({cita['id_usuario']}) | "
          f"Instructor: {cita['nombre_instructor']} ({cita['id_instructor']})")
    print(f"  Vehículo: {cita['placa']} ({cita['tipo']}) | "
          f"{cita['fecha']} a las {cita['hora']} | {cita['duracion']} h | "
          f"Asistencia: {cita['asistencia']} | Observaciones: {cita['observaciones']}")


def listar_citas():
    citas = leer_json(RUTA_CITAS)
    if not citas:
        print("No hay citas registradas.")
        return
    print("\n==== CITAS REGISTRADAS ====")
    for cita in citas:
        mostrar_cita(cita)


def buscar_cita():
    citas = leer_json(RUTA_CITAS)
    if not citas:
        print("No hay citas registradas.")
        return
    opcion = pedir_entero("Buscar por 1. Cliente / 2. Instructor: ")
    while opcion not in (1, 2):
        opcion = pedir_entero("Ingrese 1 o 2: ")
    rol = "cliente" if opcion == 1 else "instructor"
    ruta = RUTA_CLIENTES if opcion == 1 else RUTA_INSTRUCTORES
    usuario = pedir_documento(ruta, rol)
    if usuario is None:
        return
    campo = "id_usuario" if opcion == 1 else "id_instructor"
    resultados = [c for c in citas if c[campo] == usuario['documento']]
    if not resultados:
        print("No hay citas relacionadas con ese usuario.")
    for cita in resultados:
        mostrar_cita(cita)


def registrar_cita():
    citas = leer_json(RUTA_CITAS)
    print("\n---- REGISTRO DE CITA ----")
    cliente = pedir_documento(RUTA_CLIENTES, "cliente")
    if cliente is None:
        return
    instructor = pedir_documento(RUTA_INSTRUCTORES, "instructor")
    if instructor is None:
        return
    vehiculo = pedir_vehiculo()
    if vehiculo is None:
        return
    if instructor['especialidad'].lower() != vehiculo['vehiculo'].lower():
        print("El instructor no está habilitado para ese tipo de vehículo.")
        return
    fecha, hora, duracion = pedir_horario(citas, instructor, vehiculo)
    asistencia = input("¿Asistió? (SI/NO, Enter = NO): ").strip().upper() or "NO"
    while asistencia not in ("SI", "NO"):
        asistencia = input("Responda SI o NO: ").strip().upper()
    observaciones = input("Observaciones: ").strip()
    nueva = {
        "id": max((int(c['id']) for c in citas), default=0) + 1,
        "id_usuario": cliente['documento'], "nombre_usuario": cliente['nombre'],
        "id_instructor": instructor['documento'], "nombre_instructor": instructor['nombre'],
        "placa": vehiculo['placa'].upper(), "tipo": vehiculo['vehiculo'],
        "fecha": fecha, "hora": hora, "duracion": duracion,
        "asistencia": asistencia, "observaciones": observaciones,
    }
    citas.append(nueva)
    guardar_json(RUTA_CITAS, citas)
    print(f"--- CITA #{nueva['id']} REGISTRADA CORRECTAMENTE ---")


def seleccionar_cita(citas, verbo):
    if not citas:
        print("No hay citas registradas.")
        return None
    listar_citas()
    id_cita = pedir_entero(f"ID de la cita para {verbo}: ")
    cita = next((c for c in citas if c['id'] == id_cita), None)
    if cita is None:
        print("No existe una cita con ese ID.")
    return cita


def actualizar_cita():
    citas = leer_json(RUTA_CITAS)
    cita = seleccionar_cita(citas, "actualizar")
    if cita is None:
        return
    print("Enter conserva el dato actual.")
    cliente = filtrar_usuario(RUTA_CLIENTES, cita['id_usuario'])
    instructor = filtrar_usuario(RUTA_INSTRUCTORES, cita['id_instructor'])
    vehiculo = fitrar_vehiculo(RUTA_VEHICULOS, cita['placa'])
    nuevo_cliente = input(f"Documento cliente ({cita['id_usuario']}): ").strip()
    if nuevo_cliente:
        cliente_nuevo = filtrar_usuario(RUTA_CLIENTES, int(nuevo_cliente)) if nuevo_cliente.isdigit() else None
        if not cliente_nuevo:
            print("Cliente no registrado. No se realizaron cambios.")
            return
        cliente = cliente_nuevo
    nuevo_instructor = input(f"Documento instructor ({cita['id_instructor']}): ").strip()
    if nuevo_instructor:
        instructor_nuevo = filtrar_usuario(RUTA_INSTRUCTORES, int(nuevo_instructor)) if nuevo_instructor.isdigit() else None
        if not instructor_nuevo:
            print("Instructor no registrado. No se realizaron cambios.")
            return
        instructor = instructor_nuevo
    nueva_placa = input(f"Placa ({cita['placa']}): ").strip().upper()
    if nueva_placa:
        vehiculo_nuevo = next((v for v in leer_json(RUTA_VEHICULOS) if v['placa'].upper() == nueva_placa), None)
        if not vehiculo_nuevo:
            print("Vehículo no registrado. No se realizaron cambios.")
            return
        vehiculo = vehiculo_nuevo
    if not cliente or not instructor or not vehiculo:
        print("Los datos originales ya no existen. Registre las entidades antes de editar.")
        return
    if instructor['especialidad'].lower() != vehiculo['vehiculo'].lower():
        print("El instructor no está habilitado para ese vehículo. No se realizaron cambios.")
        return
    fecha = input(f"Fecha ({cita['fecha']}): ").strip() or cita['fecha']
    hora = input(f"Hora ({cita['hora']}): ").strip() or cita['hora']
    duracion_texto = input(f"Duración en horas ({cita['duracion']}): ").strip()
    try:
        duracion = int(duracion_texto) if duracion_texto else int(cita['duracion'])
        if duracion < 1:
            raise ValueError("La duración debe ser mayor que cero.")
        fecha_hora(fecha, hora)
        error = hay_conflicto(citas, fecha, hora, duracion, instructor['documento'], vehiculo['placa'], cita['id'])
        if error:
            print(error + " No se realizaron cambios.")
            return
    except ValueError as error:
        print(f"Fecha, hora o duración inválida: {error}. No se realizaron cambios.")
        return
    asistencia = input(f"Asistencia ({cita['asistencia']}): ").strip().upper() or cita['asistencia']
    if asistencia not in ('SI', 'NO'):
        print("Asistencia inválida. No se realizaron cambios.")
        return
    observaciones = input(f"Observaciones ({cita['observaciones']}): ").strip() or cita['observaciones']
    cita.update(id_usuario=cliente['documento'], nombre_usuario=cliente['nombre'],
                id_instructor=instructor['documento'], nombre_instructor=instructor['nombre'],
                placa=vehiculo['placa'].upper(), tipo=vehiculo['vehiculo'],
                fecha=fecha, hora=hora, duracion=duracion,
                asistencia=asistencia, observaciones=observaciones)
    guardar_json(RUTA_CITAS, citas)
    print("--- CITA ACTUALIZADA CORRECTAMENTE ---")


def eliminar_cita():
    citas = leer_json(RUTA_CITAS)
    cita = seleccionar_cita(citas, "eliminar")
    if cita is None:
        return
    guardar_json(RUTA_CITAS, [c for c in citas if c['id'] != cita['id']])
    print("--- CITA ELIMINADA CORRECTAMENTE ---")


# Alias por compatibilidad con nombres del proyecto original.
bucar_cita = buscar_cita
editar_cita = actualizar_cita


def menu_citas():
    while True:
        print("\n---- MÓDULO CITAS ----")
        print("1. Listar citas\n2. Buscar citas de un usuario\n3. Registrar cita")
        print("4. Editar cita\n5. Eliminar cita\n6. Volver")
        op = pedir_entero("Ingrese su opción: ")
        if op == 1:
            listar_citas()
        elif op == 2:
            buscar_cita()
        elif op == 3:
            registrar_cita()
        elif op == 4:
            actualizar_cita()
        elif op == 5:
            eliminar_cita()
        elif op == 6:
            return
        else:
            print("Opción no válida (1-6).")
