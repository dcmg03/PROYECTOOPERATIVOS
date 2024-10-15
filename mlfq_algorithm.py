import random

# Definir las colas con sus quantums
colas = [
    {'nombre': 'Cola 1', 'quantum': 4, 'procesos': []},
    {'nombre': 'Cola 2', 'quantum': 8, 'procesos': []},
    {'nombre': 'Cola 3', 'quantum': 12, 'procesos': []}
]

procesos = []
completados = []


def generar_procesos_random(n):
    global procesos
    procesos = []
    for i in range(1, n + 1):
        tiempo_ejecucion = random.randint(5, 20)
        procesos.append({
            'id': i,
            'nombre': f'Proceso {i}',
            'tiempo_restante': tiempo_ejecucion,
            'tiempo_total': tiempo_ejecucion,
            'estado': 'Nuevo',
            'nivel_cola': 0,  # Inician en la Cola 1
            'color': 'bg-primary'  # Color inicial
        })
    colas[0]['procesos'] = procesos.copy()  # Todos los procesos inician en la Cola 1


def simular_mlfq():
    global procesos, completados
    for i, cola in enumerate(colas):
        if cola['procesos']:
            proceso = cola['procesos'][0]
            quantum_actual = cola['quantum']

            # Actualizamos el estado a "En ejecución"
            proceso['estado'] = 'En ejecución'

            # Ejecutamos el proceso por un quantum o hasta que termine
            tiempo_ejecucion = min(quantum_actual, proceso['tiempo_restante'])
            proceso['tiempo_restante'] -= tiempo_ejecucion

            # Si el proceso termina
            if proceso['tiempo_restante'] <= 0:
                proceso['estado'] = 'Completado'
                completados.append(proceso)
                cola['procesos'].pop(0)
            else:
                # Si no termina y no está en la última cola, lo movemos a la siguiente
                if i < len(colas) - 1:
                    cola['procesos'].pop(0)
                    proceso['nivel_cola'] = i + 1
                    proceso['color'] = 'bg-warning' if i == 0 else 'bg-danger'
                    colas[i + 1]['procesos'].append(proceso)
                else:
                    # Si está en la última cola, lo movemos al final de esta cola
                    cola['procesos'].append(cola['procesos'].pop(0))

            # Solo procesamos un proceso por iteración
            break

    # Actualizamos el estado de los procesos en espera
    for cola in colas:
        for proceso in cola['procesos'][1:]:  # Todos excepto el primero
            proceso['estado'] = 'En espera'

    print(f"Procesos completados: {len(completados)}")
    for proceso in completados:
        print(f"  {proceso['nombre']} - Tiempo total: {proceso['tiempo_total']}")


def reiniciar_simulacion():
    global procesos, completados, colas

    print("Antes de reiniciar - Completados:", len(completados))

    # Reiniciar las colas
    for cola in colas:
        cola['procesos'] = []

    # Reiniciar los procesos y completados
    procesos = []
    completados = []

    # Generar nuevos procesos
    generar_procesos_random(5)

    # Asegurar que todos los nuevos procesos estén en la primera cola
    colas[0]['procesos'] = procesos.copy()

    print("Después de reiniciar - Completados:", len(completados))
    print("Procesos generados:", len(procesos))
    print("Procesos en Cola 1:", len(colas[0]['procesos']))
    print("Reinicio completado con éxito")


def obtener_estado_simulacion():
    return {
        'colas': colas,
        'completados': completados
    }


# Inicialización inicial
generar_procesos_random(5)