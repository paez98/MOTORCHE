import hashlib
import requests

def get_agencia_nacex(user: str, password: str, cp: str, poblacion: str) -> dict:
    # Codificar la contraseña en MD5
    pass_md5 = hashlib.md5(password.encode()).hexdigest()

    # Construir la URL (usando la forma de "posición")
    data = f"{cp}|{poblacion}"
    url = f"https://pda.nacex.com/nacex_ws/ws?method=getAgencia&data={data}&user={user}&pass={pass_md5}"

    # Realizar la petición GET
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error en la petición: {response.status_code}")

    # Parsear la respuesta
    parts = response.text.strip().split("|")
    if len(parts) < 4:
        raise Exception(f"Respuesta inválida o error de la API: {response.text}")

    return {
        "codigo_agencia": parts[0],
        "nombre_agencia": parts[1],
        "direccion_agencia": parts[2],
        "telefono_agencia": parts[3],
    }



user = "INFO@MOTORCHESL.COM"
password = "mKjj7yWwfBh"
cp = "08206"
poblacion = "SABADELL"

agencia = get_agencia_nacex(user, password, cp, poblacion)

print("Datos de la agencia:")
for clave, valor in agencia.items():
    print(f"{clave}: {valor}")
