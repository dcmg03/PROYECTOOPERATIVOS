from flask import Flask, jsonify, request, render_template
from mlfq_algorithm import generar_procesos_random, simular_mlfq, procesos, colas, completados

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_procesos', methods=['POST'])
def generar_procesos():
    generar_procesos_random(5)  # Generar 5 procesos aleatorios por defecto
    return jsonify({'status': 'ok', 'procesos': procesos}), 200

@app.route('/estado_procesos', methods=['GET'])
def estado_procesos():
    return jsonify({
        'colas': colas,
        'completados': completados
    })

@app.route('/simular_tick', methods=['GET'])
def simular_tick():
    simular_mlfq()  # Ejecutamos un tick de la simulación
    return jsonify({'status': 'ok', 'procesos': procesos}), 200

@app.route('/reiniciar_simulacion', methods=['POST'])
def reiniciar_simulacion():
    global procesos, completados
    procesos = []
    completados = []
    for cola in colas:
        cola['procesos'] = []
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True)
