from flask import Flask, request, redirect, url_for, session, render_template
from flask_restful import Api
from jinja2 import ChoiceLoader, FileSystemLoader
from generar_usuarios import generar_usuario
import bcrypt
import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, "../frontend"),
            static_url_path="/frontend")

app.secret_key = os.environ.get("SECRET_KEY", "clave_secreta_123")

app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    FileSystemLoader(os.path.join(BASE_DIR, "../frontend")),
    FileSystemLoader(os.path.join(BASE_DIR, "../frontend/pages")),
])

api = Api(app)  # ← SIEMPRE AL FINAL


def cargar_usuarios():
    with open("user.json", "r") as archivo:
        return json.load(archivo)
    
@app.route ("/")
def home():
    return render_template("login.html")

@app.route ("/panel")
def panel():
    return render_template("panel.html")

@app.route("/acceso-login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        usuarios = cargar_usuarios()

        if username in usuarios and bcrypt.checkpw(
            password.encode("utf-8"),
            usuarios[username]["password"].encode("utf-8")
        ):
            session["usuario"] = username  # ← GUARDAR sesión
            return redirect(url_for("panel"))  # ← REDIRIGIR correctamente
        else:
            return render_template("login.html")

    return render_template("login.html")

if __name__ == "__main__":
    generar_usuario()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))