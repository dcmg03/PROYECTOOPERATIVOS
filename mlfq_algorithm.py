class Proceso:
    def __init__(self, nombre, tiempo_ejecucion, nivel_cola):
        self.nombre = nombre
        self.tiempo_restante = tiempo_ejecucion
        self.tiempo_total = tiempo_ejecucion
        self.nivel_cola = nivel_cola
        self.estado = "Nuevo"  # Estado inicial del proceso

    def __repr__(self):
        return f'Proceso({self.nombre}, Tiempo Restante: {self.tiempo_restante}, Nivel Cola: {self.nivel_cola}, Estado: {self.estado})'


class Cola:
    def __init__(self, quantum):
        self.procesos = []
        self.quantum = quantum

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def ejecutar_procesos(self):
        for proceso in list(self.procesos):
            if proceso.tiempo_restante > 0:
                if proceso.tiempo_restante > self.quantum:
                    proceso.tiempo_restante -= self.quantum
                    proceso.estado = "En Progreso"
                else:
                    proceso.tiempo_restante = 0
                    proceso.estado = "Completado"

                # Si el proceso no ha terminado y está en una cola inferior, lo pasamos a la siguiente cola
                if proceso.tiempo_restante > 0 and proceso.nivel_cola < len(colas) - 1:
                    proceso.nivel_cola += 1
                    colas[proceso.nivel_cola].agregar_proceso(proceso)
                    self.procesos.remove(proceso)
            else:
                proceso.estado = "Completado"


# Inicializa las colas de MLFQ (esto será manejado desde el archivo app.py)
colas = [Cola(quantum=4), Cola(quantum=8), Cola(quantum=12)]
