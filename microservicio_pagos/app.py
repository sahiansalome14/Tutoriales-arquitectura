from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/v2/comprar', methods=['GET', 'POST'], strict_slashes=False)
def realizar_compra():
    if request.method == 'GET':
        return jsonify({
            "mensaje": "Microservicio de Pagos (v2) está activo.",
            "especificacion": "Use POST /api/v2/comprar para realizar una compra enviando JSON.",
            "ejemplo_payload": {"producto_id": 1, "cantidad": 5}
        }), 200

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Falta el cuerpo JSON en la peticion POST"}), 400

    # Simulacion de logica de negocio extraida
    producto_id = data.get('producto_id')
    cantidad = data.get('cantidad', 1)

    if not producto_id:
        return jsonify({"error": "Falta el ID del producto"}), 400

    return jsonify({
        "mensaje": "Compra procesada exitosamente por el Microservicio Flask (v2)",
        "producto_id": producto_id,
        "cantidad": cantidad,
        "status": "Aprobado"
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)