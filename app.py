from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Definir las colas y sus quantums
colas = [
    {'nombre': 'Cola 1', 'quantum': 4},
    {'nombre': 'Cola 2', 'quantum': 8},
    {'nombre': 'Cola 3', 'quantum': 12}
]

# Aquí se guardarán los procesos agregados por el usuario
procesos = []

@app.route('/')
def index():
    # Extraer solo los quantums para pasarlos a la plantilla
    quantumColas = [cola['quantum'] for cola in colas]
    return render_template('index.html', colas=colas, quantumColas=quantumColas)

@app.route('/agregar_proceso', methods=['POST'])
def agregar_proceso():
    nombre = request.form['nombre']
    tiempo_ejecucion = int(request.form['tiempo_ejecucion'])
    nivel_cola = int(request.form['nivel_cola'])

    # Crear un proceso nuevo
    proceso = {
        'nombre': nombre,
        'tiempo_restante': tiempo_ejecucion,
        'nivel_cola': nivel_cola,
        'estado': 'Nuevo',
        'tiempo_total': tiempo_ejecucion
    }
    procesos.append(proceso)

    # Retornar un status ok en formato JSON
    return jsonify({'status': 'ok'}), 200

@app.route('/estado_procesos')
def estado_procesos():
    return jsonify(procesos)

@app.route('/simular_tick')
def simular_tick():
    global procesos
    for proceso in procesos:
        if proceso['estado'] != 'Completado':
            quantum_actual = colas[proceso['nivel_cola']]['quantum']
            if proceso['tiempo_restante'] > 0:
                proceso['tiempo_restante'] -= min(quantum_actual, proceso['tiempo_restante'])
                proceso['estado'] = 'En ejecución'
            if proceso['tiempo_restante'] <= 0:
                proceso['estado'] = 'Completado'
            break  # Simula un tick por proceso

    return jsonify({'status': 'ok'}), 200

@app.route('/reiniciar_simulacion', methods=['POST'])
def reiniciar_simulacion():
    global procesos
    procesos = []
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
