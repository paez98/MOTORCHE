import hashlib
import requests

def get_puntos_nacex(user: str, password: str, direccion: str, codigo_postal: str, poblacion: str, pais: str = "ES"):
    """
    Consulta los 10 puntos NACEX más cercanos a una dirección.
    
    :param user: Usuario proporcionado por NACEX
    :param password: Contraseña (se convierte a MD5 automáticamente)
    :param direccion: Dirección completa
    :param codigo_postal: Código postal
    :param poblacion: Nombre de la ciudad/población
    :param pais: Código del país (por defecto "ES")
    :return: Lista de diccionarios con los datos de cada punto NACEX cercano
    """
    # Generar hash MD5
    md5_pass = hashlib.md5(password.encode()).hexdigest()

    # Construcción del array de dirección
    data = f"{direccion}|{codigo_postal}|{poblacion}|{pais}"
    
    # Construcción de la URL
    url = f"https://pda.nacex.com/nacex_ws/ws"
    params = {
        "method": "getPuntosNacex",
        "data": data,
        "user": user,
        "pass": md5_pass
    }

    # Realizar la solicitud GET
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error al conectarse al servicio NACEX: {response.status_code}")
    
    raw_data = response.text.strip()

    if not raw_data or raw_data.startswith("ERROR"):
        raise Exception(f"Error en la respuesta de NACEX: {raw_data}")

    # Parsear respuesta
    puntos_raw = raw_data.split("|")
    puntos = []
    fields = [
        "codigo", "direccion", "poblacion", "codigo_postal", "telefono",
        "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo",
        "shop_alias", "latitud", "longitud", "nombre", "provincia", "iso_provincia"
    ]
    
    for i in range(0, len(puntos_raw), len(fields)):
        punto = dict(zip(fields, puntos_raw[i:i+len(fields)]))
        puntos.append(punto)
    
    return puntos




user = "INFO@MOTORCHESL.COM"
password = "mKjj7yWwfBh"
direccion = "CARRER DE L'ARCÀDIA, 42"
cp = "08206"
poblacion = "SABADELL"

puntos = get_puntos_nacex(user, password, direccion, cp, poblacion)

for i, punto in enumerate(puntos, 1):
    print(f"Punto #{i}:")
    for clave, valor in punto.items():
        print(f"  {clave}: {valor}")
    print("-" * 40)