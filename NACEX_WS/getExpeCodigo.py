import requests
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('USER')
pswd = os.getenv('PSWD')


md5_pass = hashlib.md5(pswd.encode()).hexdigest()

base_url = os.getenv('NACEX_BASE_URL')


params = {
    "method": "getExpeCodigo",
    "user": user,
    "pass": md5_pass
}

try:
    response = requests.get(base_url, params=params)
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
except Exception as e:
    print(f"Error al realizar la solicitud: {e}")



if response.status_code == 200:
    print("Respuesta exitosa:")
    print(response.json())
    print(response.text)
