import bcrypt
import json
import os

def generar_usuario():
    if os.path.exists("user.json"):  # ← No regenerar si ya existe
        return
    usuario = {
        "admin": {"password": "admin123", "role": "administrador"}
    }

    #Encriptar la password
    for registro in usuario:
        clave_sin_encriptar = usuario[registro]["password"]
        clave_encriptada = bcrypt.hashpw(clave_sin_encriptar.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        usuario[registro]["password"] = clave_encriptada

    #Genero un archivo json que me encripta y genera el usuario
    with open("user.json", "w") as archivo:
        json.dump(usuario, archivo, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    generar_usuario()