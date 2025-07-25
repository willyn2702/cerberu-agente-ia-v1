print("Bienvenido a AgentesaAI.com 🚀")

import os
import json
import datetime
from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS

DATA_FOLDER = "data_web"
os.makedirs(DATA_FOLDER, exist_ok=True)

FILES_AND_DEFAULTS = {
    "visitas.json": {"visitas": 0},
    "descargas.json": {"descargas": 0},
    "comentarios.json": {"comentarios": []},
    "activaciones.json": {"usuarios": {}}  # IP o ID simulada como clave
}

for filename, default in FILES_AND_DEFAULTS.items():
    file_path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Función para obtener archivo como objeto JSON
def cargar_json(nombre):
    with open(os.path.join(DATA_FOLDER, nombre), "r", encoding="utf-8") as f:
        return json.load(f)

# Función para guardar JSON
def guardar_json(nombre, data):
    with open(os.path.join(DATA_FOLDER, nombre), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET"])
def inicio():
    return render_template("index.html")

@app.route("/visitar", methods=["POST"])
def aumentar_visitas():
    data = cargar_json("visitas.json")
    data["visitas"] += 1
    guardar_json("visitas.json", data)
    return jsonify({"mensaje": "Visita registrada", "total": data["visitas"]})

@app.route("/descargar", methods=["GET"])
def descargar_archivo():
    data = cargar_json("descargas.json")
    data["descargas"] += 1
    guardar_json("descargas.json", data)
    return send_file("cerberu-agente-ia.zip", as_attachment=True)

@app.route("/comentar", methods=["POST"])
def agregar_comentario():
    nuevo = request.get_json()
    data = cargar_json("comentarios.json")
    data["comentarios"].append(nuevo)
    guardar_json("comentarios.json", data)
    return jsonify({"mensaje": "Comentario agregado correctamente"})

@app.route("/comentarios", methods=["GET"])
def obtener_comentarios():
    data = cargar_json("comentarios.json")
    return jsonify(data)

@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    visitas = cargar_json("visitas.json")["visitas"]
    descargas = cargar_json("descargas.json")["descargas"]
    return jsonify({"visitas": visitas, "descargas": descargas})

# 🛡️ Sistema de activación
@app.route("/activar", methods=["POST"])
def activar_cliente():
    req = request.get_json()
    user_id = req.get("id", request.remote_addr)  # IP como respaldo

    activaciones = cargar_json("activaciones.json")
    usuarios = activaciones.get("usuarios", {})

    if user_id not in usuarios:
        hoy = datetime.date.today().isoformat()
        usuarios[user_id] = {"fecha_inicio": hoy}
        mensaje = (
            "🎁 ¡Bienvenido a AgentesaAI! Has activado tu prueba gratuita de 14 días. "
            "Disfruta del poder de la inteligencia artificial personalizada."
        )
    else:
        fecha_inicio = datetime.date.fromisoformat(usuarios[user_id]["fecha_inicio"])
        dias = (datetime.date.today() - fecha_inicio).days
        if dias < 14:
            if dias == 13:
                mensaje = (
                    "⚠️ ¡Último día de tu prueba gratuita! "
                    "Adquiere la suscripción mensual o licencia permanente para seguir usando AgentesaAI sin interrupciones."
                )
            else:
                mensaje = f"🧪 Estás en el día {dias+1} de tu prueba gratuita de AgentesaAI."
        else:
            mensaje = (
                "⛔ Tu prueba gratuita ha finalizado. "
                "Para seguir disfrutando de todas las funciones, suscríbete por $19.99 USD/mes o compra la licencia por $100 USD. "
                "Gracias por probar AgentesaAI."
            )

    activaciones["usuarios"] = usuarios
    guardar_json("activaciones.json", activaciones)

    return jsonify({"mensaje": mensaje})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))




