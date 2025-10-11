
import requests

# URL de login y credenciales
login_url = "https://www.partslink24.com/partslink24/login-ajax!login.action"
logout_url = "https://www.partslink24.com/partslink24/user/logout.do"
authorize_url = "https://www.partslink24.com/auth/ext/api/1.1/authorize"
consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"


# Headers para simular un navegador real
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.partslink24.com",
    "Referer": "https://www.partslink24.com/partslink24/user/login.do",
    "X-Requested-With": "XMLHttpRequest"
}

authorize_payload = {
    "serviceNames": ["bmw_parts"],
    "serviceCategoryNames": [],
    "withLogin": True
}


# Datos de inicio de sesión
login_data = {
    "loginBean.accountLogin": "es-415353",
    "loginBean.userLogin": "MOTORCHE 0",
    "loginBean.sessionSqueezeOut": "true",
    "loginBean.password": "Motorche2018",
    "loginBean.userOffsetSec": "3600",
    "loginBean.code2f": ""
}

# Iniciar sesión
session = requests.Session()

logout_response = session.get(
    logout_url, headers=headers, allow_redirects=False)
print("Logout realizado. Respuesta:", logout_response.status_code)

session = requests.Session()
response = session.post(login_url, data=login_data, headers=headers)

if response.status_code == 200:
    # print("Login exitoso.")
    print("Respuesta del servidor:", response.text)
    cookies = session.cookies.get_dict()
    print("Cookies después del login:", session.cookies.get_dict())
    token = cookies.get("PL24TOKEN")  # Obtener el token de las cookies

    authorize_headers = {
        "Content-Type": "application/json",
        "Cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()])
    }

    authorize_response = session.post(
        authorize_url, json=authorize_payload, headers=authorize_headers)
    auth_data = authorize_response.json()
    access_token = auth_data.get("access_token")

    if access_token:
        # print("access_token obtenido:", access_token)

        # Headers para la consulta
        consulta_headers = headers.copy()
        consulta_headers.update({
            "Authorization": f"Bearer {access_token}",
            "Referer": "https://www.partslink24.com/p5/latest/p5.html"
        })

        # Parámetros de la consulta
        params = {
            # "btnr": "41_1634",
            # "hg": "41",
            "lang": "es",
            "serviceName": "bmw_parts",
            # "upds": "2025-01-15--07-42",
            # "vin": "WBAVC31010VC65882",
            "vin": "WBAJH510103G25529",
            # "vin": "WBA1C91030J195436",
            "q": "sistema de cerradura",
            # "_": "1739292233367"
        }

        consulta_response = session.get(
            consulta_url, headers=consulta_headers, params=params)

        if consulta_response.status_code == 200:
            # print("Consulta exitosa.")
            response_data = consulta_response.json()

            # Extraemos solo la información que nos interesa
            records = response_data.get('data', {}).get('records', [])

            for record in records:
                partno = record.get('values', {}).get('partno')
                name = record.get('values', {}).get('name')

                bt_page = record.get('recordContext', {}).get('bt_page')

                # Extraemos el primer id dentro de group_hierarchy (si existe)
                group_hierarchy = record.get(
                    'recordContext', {}).get('group_hierarchy', [])
                group_id = group_hierarchy[0].get(
                    'id') if group_hierarchy else None

                # Imprimimos la información relevante
                if partno and name:
                    # print(f"Partno: {partno}, Name: {name}")
                    # print(f"Partno: {partno}, Name: {name}, bt_page: {bt_page}, Group ID: {group_id}")

                    # Parámetros de la consulta
                    params_producto = {
                        "btnr": bt_page,
                        "hg": group_id,
                        "lang": "es",
                        "serviceName": "bmw_parts",
                        # "upds": "2025-01-15--07-42",
                        # "vin": "WBAVC31010VC65882",
                        "vin": "WBAJH510103G25529",
                        # "vin": "WBA1C91030J195436",
                        # "q": "sistema de cerradura",
                        # "_": "1739292233367"
                    }

                    consulta_producto = session.get(
                        producto_url, headers=consulta_headers, params=params_producto)
                    if consulta_producto.status_code == 200:
                        # print("Consulta producto exitosa.")
                        response_data_product = consulta_producto.json()
                        # print(response_data_product)
                        crumbs = response_data_product.get("crumbs", [])
                        name_bt_page = None

                        for crumb in crumbs:
                            crumb_name = crumb.get("name", "")
                            # Comparamos con el bt_page
                            if crumb_name.startswith(bt_page):
                                name_bt_page = crumb_name
                                break  # Salimos del loop en cuanto lo encontramos

                        # Verificamos si el partno está en la respuesta de consulta_producto
                        valid_partno = None
                        productos = response_data_product.get(
                            "data", {}).get("records", [])
                        for producto in productos:
                            values = producto.get("values", {})
                            producto_partno = values.get("partno")
                            unavailable = producto.get("unavailable", False)

                            if producto_partno == partno and not unavailable:
                                valid_partno = producto_partno
                                break  # Encontramos un partno válido, salimos del loop

                        if valid_partno:
                            print(
                                f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}")
                        # else:
                        #     print(f"El partno {partno} está marcado como no disponible o no coincide.")

                        # Imprimimos la información relevante
                        # print(f"REF: {partno}, Nombre: {name}, Grupo: {name_bt_page}")

        else:
            print("Error en la consulta:",
                  consulta_response.status_code, consulta_response.text)

    else:
        print("No se encontró el token.")
else:
    print("Error en el login:", response.status_code, response.text)
