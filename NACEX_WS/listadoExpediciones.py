import hashlib
import requests

# Configura tus datos de acceso
usuario = "MTCENTRALCH"
password = "Motorche2034"
fecha_ini = "25/06/2025"
fecha_fin = "25/06/2025"
campos = "agencia_cliente;fecha_alta;remitente;referencia;consignatario;direccion_entrega;cp_entrega;ciudad_entrega;pais_entrega;telefono_entrega;bultos;tipo_reembolso;importe_reembolso;observaciones_datos;servicio;tracking;agencia_estado;fecha_objetivo"

# Hashea la contraseña con MD5
md5_pass = hashlib.md5(password.encode()).hexdigest()

# Construye la URL
base_url = "https://pda.nacex.com/nacex_ws/ws"
params = {
    "method": "getListadoExpediciones",
    "data": f"fecha_ini={fecha_ini}|fecha_fin={fecha_fin}|campos={campos}",
    "user": usuario,
    "pass": md5_pass
}

# Realiza la solicitud GET
response = requests.get(base_url, params=params)

# Verifica la respuesta
if response.status_code == 200:
    print("---------------")
    # Divide por líneas
    response_text = response.text
    # print(response_text)
    lineas = response_text.strip().split('|')
    # Muestra cada expedición en columnas
    for linea in lineas:
        campos = linea.split('~')
        print(f"Agencia origen (fijo): {campos[0]}")
        print(f"Número expedición (fijo): {campos[1]}")
        print(f"Código digitalización (fijo): {campos[2]}")
        print(f"Agencia cliente: {campos[3]}")
        print(f"Fecha alta: {campos[4]}")
        print(f"Remitente: {campos[5]}")
        print(f"Referencia: {campos[6]}")
        print(f"Consignatario: {campos[7]}")
        print(f"Dirección entrega: {campos[8]}")
        print(f"Código postal entrega: {campos[9]}")
        print(f"Ciudad entrega: {campos[10]}")
        print(f"País entrega: {campos[11]}")
        print(f"Teléfono entrega: {campos[12]}")
        print(f"Bultos: {campos[13]}")
        print(f"Tipo reembolso: {campos[14]}")
        print(f"Importe reembolso: {campos[15]}")
        print(f"Observaciones datos: {campos[16]}")
        print(f"Servicio: {campos[17]}")
        print(f"Tracking: {campos[18]}")
        print(f"Agencia estado: {campos[19]}")
        print(f"Fecha objetivo: {campos[20]}")
        print("---------------")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
