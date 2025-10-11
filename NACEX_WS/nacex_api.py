import requests
import hashlib
from datetime import datetime
import re
import os
import win32print


def extraer_etiqueta(response_text):
    bloques = re.findall(r'\{[^}]+\|\}', response_text)
    return "".join(bloques)

def imprimir_etiqueta(nombre_archivo, impresora):

    posibles_impresoras = [
        impresora,  # La impresora que se pasó por parámetro tiene prioridad
        r"\\192.168.3.169\nacex",
        "nacex",
        "nacex en red"
    ]

    hPrinter = None
    for nombre in posibles_impresoras:
        if not nombre:
            continue
        try:
            hPrinter = win32print.OpenPrinter(nombre)
            impresora = nombre  # Esta es la impresora válida que usaremos
            print(f"Impresora conectada correctamente: {nombre}")
            break
        except Exception as e:
            print(f"No se pudo abrir la impresora '{nombre}': {e}")

    if not hPrinter:
        print("❌ No se pudo conectar a ninguna impresora válida.")
        return

    try:
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Etiqueta NACEX", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        with open(nombre_archivo, "rb") as f:
            raw_data = f.read()
            win32print.WritePrinter(hPrinter, raw_data)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        print(f"✅ Etiqueta enviada a la impresora: {impresora}")
        return True
    except Exception as e:
        print(f"❌ Error al imprimir: {e}")
        return False
    finally:
        win32print.ClosePrinter(hPrinter)

def imprimir_etiqueta_2(nombre_archivo, impresora):
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
    print(f"Etiqueta enviada a la impresora: {impresora}")

def guardar_log(albaran, data, response_text):
    hoy = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join("logs_nacex", hoy)
    os.makedirs(log_dir, exist_ok=True)
    
    with open(os.path.join(log_dir, f"{albaran}.txt"), "w", encoding="utf-8") as f:
        f.write("DATA ENVIADO:\n")
        f.write(data + "\n\n")
        f.write("RESPUESTA RECIBIDA:\n")
        f.write(response_text)

def documentar_nacex(nom_ent, dir_ent, cp_ent, pob_ent, pais_ent, tel_ent, reembolso, ret, obs1, impresora=r"\\\\192.168.3.169\\nacex"):
    usuario = "INFO@MOTORCHESL.COM"
    clave = "mKjj7yWwfBh"
    clave_md5 = hashlib.md5(clave.encode()).hexdigest()

    data_fields = {
        "del_cli": "9992",
        "num_cli": "03179",
        "fec": datetime.now().strftime("%d/%m/%Y"),
        "tip_ser": "27",
        "tip_cob": "O",
        "ref_cli": "",
        "tip_env": "2",
        "bul": f"{1:03d}",
        "kil": f"{1.0:06.3f}",
        "nom_ent": nom_ent,
        "dir_ent": dir_ent,
        "pais_ent": pais_ent,
        "cp_ent": cp_ent,
        "pob_ent": pob_ent,
        "tel_ent": tel_ent,
        "ree": f"{reembolso:.2f}",
        "tip_ree": "O" if reembolso > 0 else "",
        "ret": ret,
        "tip_pre1": "S",
        "mod_pre1": "S",
        "pre1": tel_ent,
        "obs1": obs1,
        "etiqueta": "S",
        "modelo": "TECFV4_B",
        "seguimiento": "S"
    }

    data = "|".join(f"{k}={v}" for k, v in data_fields.items())

    url = "https://pda.nacex.com/nacex_ws/ws"
    params = {
        "method": "putExpedicion",
        "user": usuario,
        "pass": clave_md5,
        "data": data
    }

    response = requests.get(url, params=params)
    respuesta = response.text

    tracking_match = re.search(r'^(\d{9})\|', respuesta)
    albaran_match = re.search(r'\|(\d{4}/\d+)\|', respuesta)
    link_match = re.search(r'\|(https://www\\.nacex\\.com//seguimientoDetalle\\.do\\?[^|]+)\|', respuesta)

    if tracking_match and albaran_match:
        tracking = tracking_match.group(1)
        albaran = albaran_match.group(1)
        link = link_match.group(1) if link_match else ""
        
        etiqueta_codigo = extraer_etiqueta(respuesta)
        nombre_etiqueta = f"etiqueta_{albaran.replace('/', '')}.txt"

        with open(nombre_etiqueta, "w", encoding="utf-8") as f:
            f.write(etiqueta_codigo)

        etiqueta_impresa = imprimir_etiqueta(nombre_etiqueta, impresora)
        guardar_log(albaran, data, respuesta)

        return {
            "estado": "OK",
            "tracking": tracking,
            "albaran": albaran,
            "seguimiento": link,
            "etiqueta": nombre_etiqueta,
            "etiqueta_impresa": etiqueta_impresa
        }
    else:
        return {
            "estado": "ERROR",
            "respuesta": respuesta
        }
