from flask import Flask, render_template, request, jsonify
from mlfq_algorithm import Proceso, Cola

app = Flask(__name__)

# Inicializar colas del MLFQ
colas = [Cola(quantum=4), Cola(quantum=8), Cola(quantum=12)]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recibir los datos del formulario
        nombre = request.form['nombre']
        tiempo_ejecucion = int(request.form['tiempo_ejecucion'])
        nivel_cola = int(request.form['nivel_cola'])

        # Crear un nuevo proceso y agregarlo a la cola correspondiente
        nuevo_proceso = Proceso(nombre, tiempo_ejecucion, nivel_cola)
        colas[nivel_cola].agregar_proceso(nuevo_proceso)

        # Renderizar la página con el nuevo proceso
        return render_template('index.html', colas=colas)

    # Si el método es GET, simplemente renderiza la página
    return render_template('index.html', colas=colas)


# Nueva ruta para devolver el estado de los procesos en formato JSON
@app.route('/estado_procesos')
def estado_procesos():
    procesos_estado = []
    for cola in colas:
        for proceso in cola.procesos:
            procesos_estado.append({
                'nombre': proceso.nombre,
                'tiempo_restante': proceso.tiempo_restante,
                'nivel_cola': proceso.nivel_cola,
                'estado': proceso.estado
            })
    return jsonify(procesos_estado)


# Ruta para simular la ejecución cada segundo (sincrónica)
@app.route('/simular_tick')
def simular_tick():
    for cola in colas:
        cola.ejecutar_procesos()
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
