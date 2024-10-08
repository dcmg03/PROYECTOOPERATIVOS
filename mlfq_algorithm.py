class Proceso:
    def __init__(self, nombre, tiempo_ejecucion, nivel_cola):
        self.nombre = nombre
        self.tiempo_restante = tiempo_ejecucion
        self.nivel_cola = nivel_cola
        self.estado = 'Nuevo'
        self.tiempo_total = tiempo_ejecucion


class MLFQ:
    def __init__(self, colas):
        self.colas = colas  # Cada cola tiene un quantum asignado
        self.procesos = []

    def agregar_proceso(self, nombre, tiempo_ejecucion, nivel_cola):
        proceso = Proceso(nombre, tiempo_ejecucion, nivel_cola)
        self.procesos.append(proceso)

    def ejecutar_procesos(self):
        # Iterar sobre los procesos y simular la ejecución según el quantum de la cola
        for proceso in self.procesos:
            if proceso.estado != 'Completado':
                quantum_actual = self.colas[proceso.nivel_cola]['quantum']

                # Simular la ejecución del proceso según el quantum
                if proceso.tiempo_restante > 0:
                    tiempo_ejecutado = min(quantum_actual, proceso.tiempo_restante)
                    proceso.tiempo_restante -= tiempo_ejecutado
                    proceso.estado = 'En ejecución'

                # Si el proceso se ha completado
                if proceso.tiempo_restante <= 0:
                    proceso.estado = 'Completado'
                else:
                    # Si el proceso no ha sido completado y puede bajar a una cola inferior
                    if proceso.nivel_cola < len(self.colas) - 1:
                        proceso.nivel_cola += 1
                break  # Simular un tick por cada proceso, en cada llamada

    def reiniciar(self):
        # Reiniciar la lista de procesos
        self.procesos = []
