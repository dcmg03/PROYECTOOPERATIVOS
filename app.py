from flask import Flask, jsonify, request, render_template
from mlfq_algorithm import simular_mlfq, reiniciar_simulacion, obtener_estado_simulacion, generar_procesos_random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_procesos', methods=['POST'])
def generar_procesos():
    num_procesos = request.json.get('num_procesos', 5)  # Por defecto, genera 5 procesos
    generar_procesos_random(num_procesos)
    return jsonify(obtener_estado_simulacion()), 200

@app.route('/estado_simulacion', methods=['GET'])
@app.route('/estado_procesos', methods=['GET'])
def estado_simulacion():
    return jsonify(obtener_estado_simulacion())

@app.route('/simular_tick', methods=['GET', 'POST'])  # Permitimos tanto GET como POST
def simular_tick():
    simular_mlfq()
    return jsonify(obtener_estado_simulacion()), 200

@app.route('/reiniciar_simulacion', methods=['POST'])
def reiniciar():
    reiniciar_simulacion()
    return jsonify(obtener_estado_simulacion()), 200

if __name__ == '__main__':
    app.run(debug=True)
