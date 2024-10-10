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
        colas[0]['procesos'].append(procesos[-1])  # Agregar a la primera cola

def simular_mlfq():
    global procesos, completados
    for cola in colas:
        if cola['procesos']:
            proceso = cola['procesos'][0]
            quantum_actual = cola['quantum']

            # Ejecutamos el proceso por un quantum
            if proceso['tiempo_restante'] > 0:
                tiempo_ejecucion = min(quantum_actual, proceso['tiempo_restante'])
                proceso['tiempo_restante'] -= tiempo_ejecucion
                proceso['estado'] = 'En ejecución'

            # Si el proceso termina
            if proceso['tiempo_restante'] <= 0:
                proceso['estado'] = 'Completado'
                completados.append(proceso)
                cola['procesos'].remove(proceso)
            else:
                # Si no termina y está en la última cola
                if proceso['nivel_cola'] == 2:
                    cola['procesos'].remove(proceso)  # Se mantiene en la última cola
                else:
                    # Degradamos el proceso a la siguiente cola
                    cola['procesos'].remove(proceso)
                    proceso['nivel_cola'] += 1
                    proceso['color'] = 'bg-warning' if proceso['nivel_cola'] == 1 else 'bg-danger'
                    colas[proceso['nivel_cola']]['procesos'].append(proceso)
            break  # Solo simulamos un tick por cola
