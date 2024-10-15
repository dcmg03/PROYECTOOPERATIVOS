import random
import time

# Definir las colas con sus quantums
colas = [
    {'nombre': 'Cola 1', 'quantum': 4, 'procesos': []},  # Prioridad más alta
    {'nombre': 'Cola 2', 'quantum': 8, 'procesos': []},
    {'nombre': 'Cola 3', 'quantum': 12, 'procesos': []}  # Prioridad más baja
]

procesos = []
completados = []
tiempo_inicial = time.time()  # Marca de tiempo de inicio de la simulación

def generar_procesos_random(n):
    global procesos
    procesos = []
    for i in range(1, n + 1):
        tiempo_ejecucion = random.randint(5, 20)
        tiempo_llegada = time.time() - tiempo_inicial  # Tiempo de llegada relativo
        procesos.append({
            'id': i,
            'nombre': f'Proceso {i}',
            'tiempo_restante': tiempo_ejecucion,
            'tiempo_total': tiempo_ejecucion,  # Tiempo de ejecución original
            'tiempo_espera': 0,  # Inicializamos el tiempo de espera en 0
            'estado': 'Nuevo',
            'nivel_cola': 0,  # Inician en la Cola 1
            'color': 'bg-primary',  # Color inicial
            'tiempo_retorno': 0,  # Inicializamos el tiempo de retorno en 0
            'tiempo_llegada': tiempo_llegada  # Guardamos el tiempo de llegada
        })
    colas[0]['procesos'] = procesos.copy()  # Todos los procesos inician en la Cola 1


def simular_mlfq():
    global procesos, completados
    # Vamos a procesar primero la Cola 1, luego la 2, y finalmente la 3
    for cola in colas:  # Procesa las colas en orden (1, 2, 3)
        if cola['procesos']:
            proceso = cola['procesos'][0]  # Tomamos el primer proceso de la cola
            quantum_actual = cola['quantum']

            # Actualizamos el estado a "En ejecución"
            proceso['estado'] = 'En ejecución'

            # Ejecutamos el proceso por un quantum o hasta que termine
            tiempo_ejecucion = min(quantum_actual, proceso['tiempo_restante'])
            proceso['tiempo_restante'] -= tiempo_ejecucion

            # Si el proceso termina
            if proceso['tiempo_restante'] <= 0:
                proceso['estado'] = 'Completado'

                # Tiempo de retorno correcto
                proceso['tiempo_retorno'] = proceso['tiempo_espera'] + proceso[
                    'tiempo_total']  # Tiempo de ejecución + Tiempo de espera

                completados.append(proceso)
                cola['procesos'].pop(0)  # Retiramos el proceso completado de la cola
            else:
                # Si no termina y no está en la última cola, lo movemos a la siguiente
                if cola != colas[-1]:  # Si no es la última cola
                    cola['procesos'].pop(0)  # Retiramos de la cola actual
                    proceso['nivel_cola'] += 1  # Aumenta el nivel de la cola
                    proceso['color'] = 'bg-warning' if proceso['nivel_cola'] == 1 else 'bg-danger'
                    colas[proceso['nivel_cola']]['procesos'].append(proceso)  # Lo movemos a la siguiente cola
                else:
                    # Si está en la última cola, lo movemos al final de esta cola
                    cola['procesos'].append(cola['procesos'].pop(0))

            # Actualizar el tiempo de espera de los procesos que no están en ejecución
            for c in colas:
                for p in c['procesos']:
                    if p != proceso:  # Si no es el proceso que está en ejecución
                        p['tiempo_espera'] += quantum_actual  # Incrementamos el tiempo de espera en el quantum actual

            # Solo procesamos un proceso por iteración, respetando la prioridad de las colas
            break


def reiniciar_simulacion():
    global procesos, completados, colas, tiempo_inicial

    # Reiniciar las colas y procesos
    for cola in colas:
        cola['procesos'] = []

    procesos = []
    completados = []
    tiempo_inicial = time.time()  # Reiniciar el tiempo inicial de la simulación

    # Generar nuevos procesos
    generar_procesos_random(5)
    colas[0]['procesos'] = procesos.copy()

    print("Simulación reiniciada correctamente.")

def obtener_estado_simulacion():
    return {
        'colas': colas,
        'completados': completados
    }

# Inicialización inicial
generar_procesos_random(5)
