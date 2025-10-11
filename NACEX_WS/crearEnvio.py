import requests
import hashlib
from datetime import datetime
import re
import win32print
import win32api
import re


def extraer_etiqueta(response_text):
    """
    Extrae y une todos los bloques de código de etiqueta en el response.
    Cada bloque tiene la forma {...|} y se unen en una cadena.
    """
    # Busca todos los bloques que empiecen con '{' y terminen con '|}'
    bloques = re.findall(r'\{[^}]+\|\}', response_text)
    # Une los bloques en una sola cadena
    etiqueta_codigo = "".join(bloques)
    return etiqueta_codigo

def imprimir_etiqueta(codigo_etiqueta, nombre_archivo=None, impresora="NACEX"):
    if not nombre_archivo:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"etiqueta_nacex_{timestamp}.txt"
    
    # Guarda el código en un archivo
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(codigo_etiqueta)
    
    # Abre la impresora (asegúrate de que el nombre es correcto)
    hPrinter = win32print.OpenPrinter(impresora)
    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta NACEX", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        with open(nombre_archivo, "rb") as f:
            raw_data = f.read()
            win32print.WritePrinter(hPrinter, raw_data)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
    
    print(f"Etiqueta guardada en: {nombre_archivo}")
    print("Etiqueta enviada a la impresora.")


# Datos de acceso
usuario = "INFO@MOTORCHESL.COM"
clave = "mKjj7yWwfBh"
clave_md5 = hashlib.md5(clave.encode()).hexdigest()

# Campos obligatorios y otros importantes
del_cli = "2901"  # delegación del cliente (4 dígitos)
num_cli = "03179"  # número cliente NACEX (5 dígitos)
tip_ser = "27"     # tipo de servicio (2 dígitos NACEX)
tip_cob = "O"      # tipo de cobro (O Origen y D Destino)
tip_env = "2"      # tipo de envase (2 = Caja cartón varias medidas)
bul = 1            # número de bultos (entero)
kil = 1.0          # kilos (float)
nom_ent = "Prueba API 3 con reembolso"
dir_ent = "Calle de prueba, 34"
pais_ent = "ES"
cp_ent = "29010"
pob_ent = "MALAGA"
tel_ent = "951472647"

# Campos opcionales
ree = "10.99"
tip_ree = "O"
ret = "S"
tip_pre1 = "S"
mod_pre1 = "S"
pre1 = "951472647"
ref_cli = ""
obs1 = "CER-014 - BOX"
etiqueta = "S"
modelo = "TECFV4_B"
seguimiento = "S"
fec = datetime.now().strftime("%d/%m/%Y")  # fecha actual

# Formato especial para bul y kil
bul_str = f"{bul:03d}"             # siempre 3 dígitos, ej. 001
kil_str = f"{kil:06.3f}"           # 5.3 dígitos, ej. 001.000

# Construcción del campo `data`
data_fields = {
    "del_cli": del_cli,
    "num_cli": num_cli,
    "fec": fec,
    "tip_ser": tip_ser,
    "tip_cob": tip_cob,
    "ref_cli": ref_cli,
    "tip_env": tip_env,
    "bul": bul_str,
    "kil": kil_str,
    "nom_ent": nom_ent,
    "dir_ent": dir_ent,
    "pais_ent": pais_ent,
    "cp_ent": cp_ent,
    "pob_ent": pob_ent,
    "tel_ent": tel_ent,
    "ree": ree,
    "tip_ree": tip_ree,
    "ret": ret,
    "tip_pre1": tip_pre1,
    "mod_pre1": mod_pre1,
    "pre1": pre1,
    "obs1": obs1,
    "etiqueta": etiqueta,
    "modelo": modelo,
    "seguimiento": seguimiento,
}

# Concatenar en formato key=value|key2=value2...
data = "|".join(f"{key}={value}" for key, value in data_fields.items())

# Enviar la petición
url = "https://pda.nacex.com/nacex_ws/ws"
params = {
    "method": "putExpedicion",
    "user": usuario,
    "pass": clave_md5,
    "data": data
}

response = requests.get(url, params=params)
respuesta = response.text

# Mostrar resultado
print("Respuesta completa:\n", respuesta)

# Extraer datos importantes si están presentes
tracking_match = re.search(r'^(\d{9})\|', respuesta)
albaran_match = re.search(r'\|(\d{4}/\d+)\|', respuesta)
link_match = re.search(r'\|(https://www\.nacex\.com//seguimientoDetalle\.do\?[^|]+)\|', respuesta)

if tracking_match and albaran_match and link_match:
    tracking = tracking_match.group(1)
    albaran = albaran_match.group(1)
    link = link_match.group(1)

    if albaran:
        print("\n=== Envío documentado correctamente ===")
        print(f"Tracking: {tracking}")
        print(f"Albarán: {albaran}")
        print(f"Link seguimiento: {link}")
    else:
        print("No se ha generado albarán. Fallo al documentar.")
else:
    print("No se pudieron extraer los datos de tracking, albarán o link. Verifica la respuesta.")

etiqueta_codigo = extraer_etiqueta(respuesta)
print("Código de etiqueta extraído:")
print(etiqueta_codigo)


printer_name = r"\\192.168.3.169\nacex"
imprimir_etiqueta(etiqueta_codigo, impresora=printer_name)