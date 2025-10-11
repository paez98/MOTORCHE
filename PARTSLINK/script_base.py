import requests
import os
import re
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()
account = os.getenv("Account")
user = os.getenv("User")
password = os.getenv("Password")

# Clase General De Partlink


class PartsLink24API:
    def __init__(
        self,
        account,
        user,
        password,
        vin,
        marca,
        query,
        serviceNames,
        consulta_url,
        producto_url,
    ):
        self.logout_session = requests.Session()  # Sesión para logout
        self.login_session = requests.Session()  # Sesión para login

        self.login_url = (
            "https://www.partslink24.com/partslink24/login-ajax!login.action"
        )
        self.logout_url = "https://www.partslink24.com/partslink24/user/logout.do"
        self.authorize_url = "https://www.partslink24.com/auth/ext/api/1.1/authorize"

        self.login_data = {
            "loginBean.accountLogin": account,
            "loginBean.userLogin": user,
            "loginBean.sessionSqueezeOut": "true",
            "loginBean.password": password,
            "loginBean.userOffsetSec": "3600",
            "loginBean.code2f": "",
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.partslink24.com",
            "Referer": "https://www.partslink24.com/partslink24/user/login.do",
            "X-Requested-With": "XMLHttpRequest",
        }

        self.vin = vin
        self.marca = marca
        self.query = query
        self.serviceNames = serviceNames

        self.consulta_url = consulta_url
        self.producto_url = producto_url

        self.token = None
        self.access_token = None

    def login(self):
        # Iniciar sesión
        if self.logout():

            response = self.login_session.post(
                self.login_url, data=self.login_data, headers=self.headers
            )
            if response.status_code == 200:
                cookies = self.login_session.cookies.get_dict()
                self.token = cookies.get("PL24TOKEN")
                return True
            return False

    def logout(self):
        # Cerrar sesión
        logout_response = self.logout_session.get(
            self.logout_url, headers=self.headers, allow_redirects=False
        )
        if logout_response.status_code == 302:
            return True
        return False

    def authorize(self):
        if self.token:
            authorize_payload = {
                "serviceNames": [f"{self.serviceNames}"],
                "serviceCategoryNames": [],
                "withLogin": True,
            }
            authorize_headers = {
                "Content-Type": "application/json",
                "Cookie": "; ".join(
                    [
                        f"{key}={value}"
                        for key, value in self.login_session.cookies.get_dict().items()
                    ]
                ),
            }
            authorize_response = self.login_session.post(
                self.authorize_url, json=authorize_payload, headers=authorize_headers
            )
            auth_data = authorize_response.json()
            self.access_token = auth_data.get("access_token")
            return self.access_token
        return None

    def consulta(self):
        if not self.access_token:
            print("No se ha autorizado correctamente.")
            return

        consulta_headers = self.headers.copy()
        consulta_headers.update(
            {
                "Authorization": f"Bearer {self.access_token}",
                "Referer": "https://www.partslink24.com/p5/latest/p5.html",
            }
        )

        params = {
            "lang": "es",
            "serviceName": self.serviceNames,
            "vin": self.vin,
            "q": self.query,
        }

        consulta_response = self.login_session.get(
            self.consulta_url, headers=consulta_headers, params=params
        )

        if consulta_response.status_code == 200:
            return consulta_response.json()
        else:
            requests.exceptions.BaseHTTPError()

            print(f"Error en la consulta: {consulta_response.status_code}")
            return None

    def procesar_resultados(self, response_data):
        """Método general para procesar resultados de la consulta."""
        records = response_data.get("data", {}).get("records", [])
        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            if partno and name:
                print(f"Partno: {partno}, Name: {name}")

    def normalizar_partno(self, partno):
        return re.sub(r"^[a-zA-Z]\s*", "", partno.strip())


class PartsLink24API_2:
    def __init__(
        self,
        account,
        user,
        password,
        vin,
        marca,
        query,
        serviceNames,
        consulta_url,
        producto_url,
    ):
        self.logout_session = requests.Session()  # Sesión para logout
        self.login_session = requests.Session()  # Sesión para login

        self.login_url = (
            "https://www.partslink24.com/partslink24/login-ajax!login.action"
        )
        self.logout_url = "https://www.partslink24.com/partslink24/user/logout.do"
        self.authorize_url = "https://www.partslink24.com/auth/ext/api/1.1/authorize"

        self.login_data = {
            "loginBean.accountLogin": account,
            "loginBean.userLogin": user,
            "loginBean.sessionSqueezeOut": "true",
            "loginBean.password": password,
            "loginBean.userOffsetSec": "3600",
            "loginBean.code2f": "",
        }

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.partslink24.com",
            "Referer": "https://www.partslink24.com/partslink24/user/login.do",
            "X-Requested-With": "XMLHttpRequest",
        }

        self.vin = vin
        self.marca = marca
        self.query = query
        self.serviceNames = serviceNames

        self.consulta_url = consulta_url
        self.producto_url = producto_url

        self.token = None
        self.access_token = None

    def login(self):
        # Iniciar sesión
        if self.logout():
            response = self.login_session.post(
                self.login_url, data=self.login_data, headers=self.headers
            )
            if response.status_code == 200:
                cookies = self.login_session.cookies.get_dict()
                self.token = cookies.get("PL24TOKEN")
                return True
            return False

    def logout(self):
        # Cerrar sesión
        logout_response = self.logout_session.get(
            self.logout_url, headers=self.headers, allow_redirects=False
        )
        if logout_response.status_code == 302:
            return True
        return False

    def authorize(self):
        if self.token:
            authorize_payload = {
                "serviceNames": [f"{self.serviceNames}"],
                "serviceCategoryNames": [],
                "withLogin": True,
            }
            authorize_headers = {
                "Content-Type": "application/json",
                "Cookie": "; ".join(
                    [
                        f"{key}={value}"
                        for key, value in self.login_session.cookies.get_dict().items()
                    ]
                ),
            }
            authorize_response = self.login_session.post(
                self.authorize_url, json=authorize_payload, headers=authorize_headers
            )
            auth_data = authorize_response.json()
            self.access_token = auth_data.get("access_token")
            return self.access_token
        return None

    def consulta(self):
        if not self.access_token:
            print("No se ha autorizado correctamente.")
            return

        consulta_headers = self.headers.copy()
        consulta_headers.update(
            {
                "Authorization": f"Bearer {self.access_token}",
                "Referer": "https://www.partslink24.com/p5/latest/p5.html",
            }
        )

        params = {
            "cat": "60R",  # Smart 60J 60R para MercedesV, Mercedes Furgoneta 63J Mercedes
            "lang": "es",
            # "productClassId":"F",
            "serviceName": self.serviceNames,
            "vin": self.vin,
            "q": self.query,
        }
        if "smart_parts" in self.serviceNames:
            params["cat"] = "60J"
        elif "mercedesvans_parts" in self.serviceNames:
            params["cat"] = "60R"
        elif "mercedes_parts" in self.serviceNames:
            params["cat"] = "63J"
        else:
            params["cat"] = ""

        consulta_response = self.login_session.get(
            self.consulta_url, headers=consulta_headers, params=params
        )

        if consulta_response.status_code == 200:
            return consulta_response.json()
        else:
            print(f"Error en la consulta: {consulta_response.status_code}")
            return None

    def procesar_resultados(self, response_data):
        """Método general para procesar resultados de la consulta."""
        records = response_data.get("data", {}).get("records", [])
        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            if partno and name:
                print(f"Partno: {partno}, Name: {name}")

    def normalizar_partno(self, partno):
        return re.sub(r"^[a-zA-Z]\s*", "", partno.strip())


# Clases individuales por MARCA
class BMW(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "BMW",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            bt_page = record.get("recordContext", {}).get("bidata_bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get(
                "bidata_group_hierarchy", []
            )
            group_id = group_hierarchy[0].get("id") if group_hierarchy else None

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and group_id:
                params_producto = {
                    "btnr": bt_page,
                    "hg": group_id,
                    "lang": "es",
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if producto_partno == partno and not unavailable:
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        ref_normalizado = self.quitar_espacios_partno(valid_partno)
                        # elimina saltos y espacios alrededor
                        name = re.sub(r"\s*\n\s*", " ", name).strip()
                        # normaliza múltiples espacios
                        name = re.sub(r"\s+", " ", name)
                        print(
                            f"REF: {ref_normalizado}, NOMBRE: {name}, GRUPO: {name_bt_page}"
                        )


class VW(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "VW",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"

    def limpiar_partno_base(self, partno):
        """
        Devuelve el partno normalizado, truncado a los primeros 4 bloques
        (por si contiene sufijos como colores u opciones).
        """
        bloques = partno.strip().split()
        bloques_base = bloques[:4]  # Máximo 4 bloques
        return self.normalizar_partno(" ".join(bloques_base))

    def quitar_espacios_partno(self, partno: str) -> str:
        """
        Normaliza el número de parte eliminando todos los espacios y convirtiendo a mayúsculas.
        """
        return partno.replace(" ", "").upper()

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            bt_page = record.get("recordContext", {}).get("bidata_bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get(
                "bidata_group_hierarchy", []
            )
            # group_id = group_hierarchy[0].get('id') if group_hierarchy else None
            maingroup = next(
                (g["id"] for g in group_hierarchy if g["type"] == "maingroup"), None
            )

            p5goto = record.get("p5goto", {})
            ws = p5goto.get("ws", [])

            # Buscar illustrationId en el path
            illustration_id = None
            for w in ws:
                path = w.get("path", "")
                match = re.search(r"illustrationId=(\d+)", path)
                if match:
                    illustration_id = match.group(1)
                    break  # Salimos en cuanto encontramos el primero

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and maingroup and illustration_id:
                params_producto = {
                    "illustrationId": illustration_id,
                    "lang": "es",
                    "maingroup": maingroup,
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        # if self.normalizar_partno(producto_partno) == self.normalizar_partno(partno) and not unavailable:
                        if (
                            self.limpiar_partno_base(producto_partno)
                            == self.limpiar_partno_base(partno)
                            and not unavailable
                        ):
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        ref_normalizado = self.quitar_espacios_partno(valid_partno)
                        # elimina saltos y espacios alrededor
                        name = re.sub(r"\s*\n\s*", " ", name).strip()
                        # normaliza múltiples espacios
                        name = re.sub(r"\s+", " ", name)
                        print(
                            f"REF: {ref_normalizado}, NOMBRE: {name}, GRUPO: {name_bt_page}"
                        )


class TOYOTA(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5toyota/extern/search/vin"
        producto_url = (
            "https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails"
        )
        super().__init__(
            account,
            user,
            password,
            vin,
            "TOYOTA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"

    """https://www.partslink24.com/p5toyota/extern/search/vin?lang=es&serviceName=toyota_parts&upds=2025-02-13--12-38&vin=JTEBZ29J100180316&q=balona%20suspension&_=1740073972466"""
    """
https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails?illustNum=481551P&lang=es&mainGroup=4&serviceName=toyota_parts&subGroup=4803&upds=2025-02-13--12-38&vin=JTEBZ29J100180316&_=174007894568"""

    def procesar_resultados(self, response_data):

        records = response_data.get("data", {}).get("records", [])

        for record in records:
            # Extraer información relevante del record
            part_number = record["values"]["partnumber"]
            position = record["values"]["pos"]
            subgroup_desc = record["values"]["subgroupDescription"]
            part_desc = record["values"]["partDescription"]
            illustration = record["recordContext"]["illustration"]
            bt_page = record["recordContext"]["bt_page"]

            # Imprimir la información
            print("=" * 50)  # Separador visual
            print(f"Part Number: {part_number}")
            print(f"Position: {position}")
            print(f"Subgroup Description: {subgroup_desc}")
            print(f"Part Description: {part_desc}")
            print(f"Illustration: {illustration}")
            print(f"BT Page: {bt_page}")
            print("=" * 50)  # Separador visual
            print()  # Espacio en blanco entre registros


class SMART(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5daimler/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5daimler/extern/bom/vin/detail"

        "https://www.partslink24.com/p5daimler/extern/search/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "SMART",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"

    def procesar_resultados(self, response_data):

        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("pos")
            name = record.get("values", {}).get("partDescription")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            # group_id = group_hierarchy[0].get('id') if group_hierarchy else None
            maingroup = next(
                (g["id"] for g in group_hierarchy if g["type"] == "maingroup"), None
            )
            subgroup = next(
                (g["id"] for g in group_hierarchy if g["type"] == "subgroup"), None
            )

            p5goto = record.get("p5goto", {})
            ws = p5goto.get("ws", [])
            values = record["values"]
            print(f"Grupo Principal: {values['mg']}")
            print(f"Subgrupo: {values['sg']}")
            print(f"Descripción: {values['description']}")
            print(f"Posición: {values['position']}")

            # Buscar illustrationId en el path
            illustration_id = None
            for w in ws:
                path = w.get("path", "")
                match = re.search(r"illustNum=(\d+)", path)
                if match:
                    illustration_id = bt_page
                    # match.group(1)
                    break  # Salimos en cuanto encontramos el primero

            # Si hay información suficiente, hacemos la segunda consulta
            if (
                partno
                and name
                and bt_page
                and (maingroup or subgroup)
                and illustration_id
            ):
                params_producto = {
                    "illustNum": illustration_id,
                    "lang": "es",
                    "maingroup": maingroup,
                    "subGroup": subgroup,
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        if producto["id"] != "_null":
                            producto_partno = producto["partno"]
                            unavailable = producto.get("unavailable", False)

                        if (
                            self.normalizar_partno(producto_partno)
                            == self.normalizar_partno(partno)
                            and not unavailable
                        ):
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class SKODA(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "SKODA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            # group_id = group_hierarchy[0].get('id') if group_hierarchy else None
            maingroup = next(
                (g["id"] for g in group_hierarchy if g["type"] == "maingroup"), None
            )

            p5goto = record.get("p5goto", {})
            ws = p5goto.get("ws", [])

            # Buscar illustrationId en el path
            illustration_id = None
            for w in ws:
                path = w.get("path", "")
                match = re.search(r"illustrationId=(\d+)", path)
                if match:
                    illustration_id = match.group(1)
                    break  # Salimos en cuanto encontramos el primero

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and maingroup and illustration_id:
                params_producto = {
                    "illustrationId": illustration_id,
                    "lang": "es",
                    "maingroup": maingroup,
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if (
                            self.normalizar_partno(producto_partno)
                            == self.normalizar_partno(partno)
                            and not unavailable
                        ):
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class SEAT(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "SEAT",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5vwag/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5vwag/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            # group_id = group_hierarchy[0].get('id') if group_hierarchy else None
            maingroup = next(
                (g["id"] for g in group_hierarchy if g["type"] == "maingroup"), None
            )

            p5goto = record.get("p5goto", {})
            ws = p5goto.get("ws", [])

            # Buscar illustrationId en el path
            illustration_id = None
            for w in ws:
                path = w.get("path", "")
                match = re.search(r"illustrationId=(\d+)", path)
                if match:
                    illustration_id = match.group(1)
                    break  # Salimos en cuanto encontramos el primero

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and maingroup and illustration_id:
                params_producto = {
                    "illustrationId": illustration_id,
                    "lang": "es",
                    "maingroup": maingroup,
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if (
                            self.normalizar_partno(producto_partno)
                            == self.normalizar_partno(partno)
                            and not unavailable
                        ):
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class MITSUBISHI(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5mitsubishi/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5mitsubishi/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "MITSUBISHI",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            # Extraer información relevante
            description = record.get("description", "N/A")  # 'N/A' si no existe
            part_number = record["values"]["partNumber"]
            part_description = record["values"]["partDescription"]

            # Limpiar posibles códigos HTML o caracteres especiales (opcional)
            description = description.replace("<b>", "").replace("</b>", "")
            part_description = part_description.replace("<b>", "").replace("</b>", "")

            # Imprimir la información
            print("=" * 50)  # Separador visual
            print(f"Descripción: {description}")
            print(f"Part Number: {part_number}")
            print(f"Part Description: {part_description}")
            print("=" * 50)  # Separador visual
            print()  # Espacio en blanco entre registros


class LANDROVER(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5jlr/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails"
        super().__init__(
            account,
            user,
            password,
            vin,
            "DACIA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para LANDROVER con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partnumber")
            name = record.get("values", {}).get("bomPath")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            group_id = group_hierarchy[0].get("id") if group_hierarchy else None

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and group_id:
                params_producto = {
                    "btnr": bt_page,
                    "hg": group_id,
                    "lang": "es",
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if producto_partno == partno and not unavailable:
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class DACIA(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5renault/extern/search/vin_mdl"
        producto_url = "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails"
        super().__init__(
            account,
            user,
            password,
            vin,
            "LANDROVER",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5renault/extern/search/vin_mdl"
        # self.producto_url = "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details"

    def procesar_resultados(self, response_data):
        """Método específico para DACIA con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partnumber")
            name = record.get("values", {}).get("bomPath")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            group_id = group_hierarchy[0].get("id") if group_hierarchy else None

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and group_id:
                params_producto = {
                    "btnr": bt_page,
                    "hg": group_id,
                    "lang": "es",
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if producto_partno == partno and not unavailable:
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class AUDI(PartsLink24API):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"
        super().__init__(
            account,
            user,
            password,
            vin,
            "AUDI",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/p5bmw/extern/search/vin"
        # self.producto_url = "https://www.partslink24.com/p5bmw/extern/bom/vin"

    def procesar_resultados(self, response_data):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])

        for record in records:
            partno = record.get("values", {}).get("partno")
            name = record.get("values", {}).get("name")
            bt_page = record.get("recordContext", {}).get("bt_page")

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get("group_hierarchy", [])
            group_id = group_hierarchy[0].get("id") if group_hierarchy else None

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and group_id:
                params_producto = {
                    "btnr": bt_page,
                    "hg": group_id,
                    "lang": "es",
                    "serviceName": self.serviceNames,
                    "vin": self.vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.login_session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()

                    # Buscar el nombre del bt_page en los 'crumbs'
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = None
                    for crumb in crumbs:
                        crumb_name = crumb.get("name", "")
                        if crumb_name.startswith(bt_page):
                            name_bt_page = crumb_name
                            break  # Encontramos el nombre y salimos

                    # Verificar si el partno es válido en la respuesta de productos
                    valid_partno = None
                    productos = response_data_product.get("data", {}).get("records", [])
                    for producto in productos:
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        unavailable = producto.get("unavailable", False)

                        if producto_partno == partno and not unavailable:
                            valid_partno = producto_partno
                            break  # Encontramos un partno válido

                    if valid_partno:
                        print(
                            f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}"
                        )


class VOLVO(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action?"
        )
        super().__init__(
            account,
            user,
            password,
            vin,
            "VOLVO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action?service=volvo_parts&vin=YV1BZ714691047931"
        # self.producto_url = "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action?"

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Group1: {item['group1']}")
                print(f"Group2: {item['group2']}")
                print(f"Illustration: {item['illu']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"Score: {item['score']}")
                print(f"Section Code: {item['sectionCode']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class PEUGEOT(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/psa/peugeot_parts/json-vin-search.action"
        )
        super().__init__(
            account,
            user,
            password,
            vin,
            "VOLVO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/psa/peugeot_parts/json-vin-search.action"
        # self.producto_url = "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action?"

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Illustration: {item['illustration']}")
                print(f"Illustration Formatted: {item['illustrationFormatted']}")
                print(f"Illustration Path: {item['illustrationPath']}")
                print(f"Main Group Path: {item['mainGroupPath']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"Scope Path: {item['scopePath']}")
                print(f"Score: {item['score']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class OPEL(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/opel/opel_parts/json-vin-search.action"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "OPEL",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )
        # self.consulta_url = "https://www.partslink24.com/opel/opel_parts/json-vin-search.action"
        # self.producto_url = "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action?"

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"GM Part Number: {item['gmPartNo']}")
                print(f"GM Opel Part Number: {item['gmOpelPartNo']}")
                print(f"Illustration: {item['illustration']}")
                print(f"Illustration Short Name: {item['illustrationShortName']}")
                print(f"Main Group ID: {item['mainGroupId']}")
                print(f"Sub Group ID: {item['subGroupId']}")
                print(f"Score: {item['score']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class NISSAN(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/nissan/nissan_parts/json-vin-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "OPEL",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Drawing Number: {item['drawingNo']}")
                print(f"Drawing Variant: {item['drawingVar']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Main Group Caption: {item['mainGroupCaption']}")
                print(f"Model: {item['model']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"PNC: {item['pnc']}")
                print(f"PNC HTML: {item['pncHtml']}")
                print(f"Score: {item['score']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"Sub Group Caption: {item['subGroupCaption']}")
                print(f"URL: {item['url']}")
                print(f"Usage: {item['usage']}")
                print("-" * 40)  # Separador entre items


class LANCIA(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/fiatspa/lancia_parts/json-vin-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "LANCIA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['caption'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"BOM Code: {item['bomCode']}")
                print(f"BOM Revision: {item['bomRevision']}")
                print(f"BOM Variant: {item['bomVariant']}")
                print(f"Country Code: {item['countrycode']}")
                print(f"Illustration Description: {item['illustrationDescription']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number Highlighted: {item['partnoHighlighted']}")
                print(f"Score: {item['score']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class KIA(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/json-vin-search.action?"
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "KIA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Illustration: {item['illustration']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"PNC: {item['pnc']}")
                print(f"PNC HTML: {item['pncHtml']}")
                print(f"Score: {item['score']}")
                print(f"Spread Part Number: {item['spreadPartno']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class JEEP(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/fiatspa/jeep_parts/json-search.action"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "KIA",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['caption'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"BOM Code: {item['bomCode']}")
                print(f"BOM Revision: {item['bomRevision']}")
                print(f"BOM Variant: {item['bomVariant']}")
                print(f"Country Code: {item['countrycode']}")
                print(f"Illustration Description: {item['illustrationDescription']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number Highlighted: {item['partnoHighlighted']}")
                print(f"Score: {item['score']}")
                print(f"Service Kit Drawing ID: {item['servicekitDrawingId']}")
                print(f"Service Kit ID: {item['servicekitId']}")
                print(f"Service Kit Position Number: {item['servicekitPosno']}")
                print(
                    f"Service Kit Position Number Sequence: {item['servicekitPosno_seq']}"
                )
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class IVECO(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/iveco/iveco_parts/json-vin-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "IVECO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(f"Group: {item['grHtml']}")
                print(f"Illustration Number: {item['illuno']}")
                print(f"Main Group: {item['mgHtml']}")
                print(
                    f"Part Name: {item['partnameHtml'].replace('<b>', '').replace('</b>', '')}"
                )
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"Score: {item['score']}")
                print(f"Selected: {item['selected']}")
                print(f"Sub Group: {item['sgHtml']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class HYUNDAI(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/json-vin-search.action"
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "IVECO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Illustration: {item['illustration']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"PNC: {item['pnc']}")
                print(f"PNC HTML: {item['pncHtml']}")
                print(f"Score: {item['score']}")
                print(f"Spread Part Number: {item['spreadPartno']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class FORD(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/ford/fordp_parts/json-vin-search.action"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "IVECO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(f"BOM ID: {item['bomId']}")
                print(f"Engineering Part HTML: {item['engineeringPartHTML']}")
                print(f"Engineering Part Number: {item['engineeringPartNo']}")
                print(f"Imageboard HTML: {item['imageboardHTML']}")
                print(f"Main Group ID: {item['mainGroupId']}")
                print(f"PNC: {item['pnc']}")
                print(
                    f"PNC Description HTML: {item['pncDescriptionHTML'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"PNC HTML: {item['pncHTML']}")
                print(f"Scope Description HTML: {item['scopeDescriptionHTML']}")
                print(f"Score: {item['score']}")
                print(f"Selected: {item['selected']}")
                print(
                    f"Service Part Description HTML: {item['servicePartDescriptionHTML'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Service Part HTML: {item['servicePartHTML']}")
                print(f"Service Part Number: {item['servicePartNo']}")
                print(f"Shared Catalog Code: {item['sharedCatCode']}")
                print(f"Sub Group ID: {item['subGroupId']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class FIAT(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/fiatspa/fiatp_parts/json-vin-search.action"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "IVECO",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['caption'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"BOM Code: {item['bomCode']}")
                print(f"BOM Revision: {item['bomRevision']}")
                print(f"BOM Variant: {item['bomVariant']}")
                print(f"Country Code: {item['countrycode']}")
                print(f"Illustration Description: {item['illustrationDescription']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number Highlighted: {item['partnoHighlighted']}")
                print(f"Score: {item['score']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class FIATPro(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/fiatspa/fiatt_parts/json-vin-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "FiatPro",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['caption'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"BOM Code: {item['bomCode']}")
                print(f"BOM Revision: {item['bomRevision']}")
                print(f"BOM Variant: {item['bomVariant']}")
                print(f"Country Code: {item['countrycode']}")
                print(f"Illustration Description: {item['illustrationDescription']}")
                print(f"Main Group: {item['mainGroup']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number Highlighted: {item['partnoHighlighted']}")
                print(f"Score: {item['score']}")
                print(f"Sub Group: {item['subGroup']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


class CITROEN(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/psa/citroen_parts/json-vin-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "Citroen",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Illustration: {item['illustration']}")
                print(f"Illustration Formatted: {item['illustrationFormatted']}")
                print(f"Illustration Path: {item['illustrationPath']}")
                print(f"Main Group Path: {item['mainGroupPath']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"Scope Path: {item['scopePath']}")
                print(f"Score: {item['score']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class CITROENDS(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/psa/citroenDs_parts/json-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "Citroen",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Illustration: {item['illustration']}")
                print(f"Illustration Formatted: {item['illustrationFormatted']}")
                print(f"Illustration Path: {item['illustrationPath']}")
                print(f"Main Group Path: {item['mainGroupPath']}")
                print(f"Part Number: {item['partno']}")
                print(f"Part Number HTML: {item['partnoHtml']}")
                print(f"Scope Path: {item['scopePath']}")
                print(f"Score: {item['score']}")
                print(f"URL: {item['url']}")
                print("-" * 40)  # Separador entre items


class VAUXHALL(PartsLink24API_2):
    def __init__(self, vin, query, serviceNames):
        consulta_url = "https://www.partslink24.com/volvo/pl24-entry.action"
        producto_url = (
            "https://www.partslink24.com/opel/vauxhall_parts/json-search.action?"
        )
        value = super().__init__(
            account,
            user,
            password,
            vin,
            "Vauxhall",
            query,
            serviceNames,
            consulta_url,
            producto_url,
        )

    def procesar_resultados(self, response_data):
        # Verificar si hay items
        if not response_data.get("items"):
            print("No se encontraron objetos con el término de búsqueda.")
        else:
            # Imprimir los items de manera organizada
            print("Items encontrados:")
            for item in response_data["items"]:
                print(f"BOM Detail ID: {item['bomDetailId']}")
                print(f"BOM ID: {item['bomId']}")
                print(
                    f"Caption: {item['captionHtml'].replace('<u>', '').replace('</u>', '')}"
                )
                print(f"Category ID: {item['catId']}")
                print(f"GM Opel Part Number: {item['gmOpelPartNo']}")
                print(f"GM Opel Part Number HTML: {item['gmOpelPartNoHtml']}")
                print(f"GM Part Number: {item['gmPartNo']}")
                print(f"GM Part Number HTML: {item['gmPartNoHtml']}")
                print(f"Illustration: {item['illustration']}")
                print(f"Illustration Short Name: {item['illustrationShortName']}")
                print(f"Main Group ID: {item['mainGroupId']}")
                print(f"Score: {item['score']}")
                print(f"Sub Group ID: {item['subGroupId']}")
                print(f"URL: {item['url']}")
                print(f"Valid: {item['valid']}")
                print("-" * 40)  # Separador entre items


# vin = "WVGZZZ1TZDW067437"
# query = "cerradura de capo"
# marca = "VW"


# vin = "WBAUD91000PZ04802"
# query = "Alzacristales electr"
# marca = "BMW"

# vin = "WVWZZZ1JZYB025644"
# query = "Cerradura de la puerta"
# marca = "VW"

# vin = "JTEBZ29J100180316"
# query = "suspension neumatica"
# marca = "TOYOTA"


# Validador
def run_api(bastidor, q, make):

    vin = bastidor
    query = q
    marca = make

    if marca == "BMW":
        serviceNames = os.getenv("serviceNamesBMW")
        api = BMW(vin, query, serviceNames)
    elif marca.upper() == "VW":
        serviceNames = os.getenv("serviceNamesVW")
        api = VW(vin, query, serviceNames)
    elif marca == "TOYOTA":
        serviceNames = os.getenv("serviceNamesTOYOTA")
        api = TOYOTA(vin, query, serviceNames)
    elif marca == "SMART":
        serviceNames = os.getenv("serviceNamesSMART")
        api = SMART(vin, query, serviceNames)
    elif marca == "SKODA":
        serviceNames = os.getenv("serviceNamesSKODA")
        api = SKODA(vin, query, serviceNames)
    elif marca == "SEAT":
        serviceNames = os.getenv("serviceNamesSEAT")
        api = VW(vin, query, serviceNames)
    elif marca == "PORSCHE":
        serviceNames = os.getenv("serviceNamesPORSCHE")
        api = VW(vin, query, serviceNames)
    elif marca == "MITSUBISHI":
        serviceNames = os.getenv("serviceNamesMITSUBISHI")
        api = MITSUBISHI(vin, query, serviceNames)
    elif marca == "MINI":
        serviceNames = os.getenv("serviceNamesMINI")
        api = BMW(vin, query, serviceNames)
    elif marca == "MERCEDESV":
        serviceNames = os.getenv("serviceNamesMERCEDESV")
        api = SMART(vin, query, serviceNames)
    elif marca == "MERCEDES":
        serviceNames = os.getenv("serviceNamesMERCEDES")
        api = SMART(vin, query, serviceNames)
    elif marca == "LANDROVER":
        serviceNames = os.getenv("serviceNamesLANDROVER")
        api = LANDROVER(vin, query, serviceNames)
    elif marca == "DACIA":
        serviceNames = os.getenv("serviceNamesDACIA")
        api = DACIA(vin, query, serviceNames)
    elif marca == "VOLVO":
        serviceNames = os.getenv("serviceNamesVOLVO")
        api = VOLVO(vin, query, serviceNames)
    elif marca == "PEUGEOT":
        serviceNames = os.getenv("serviceNamesPEUGEOT")
        api = PEUGEOT(vin, query, serviceNames)
    elif marca == "OPEL":
        serviceNames = os.getenv("serviceNamesOPEL")
        api = OPEL(vin, query, serviceNames)
    elif marca == "NISSAN":
        serviceNames = os.getenv("serviceNamesNISSAN")
        api = NISSAN(vin, query, serviceNames)
    elif marca == "LANCIA":
        serviceNames = os.getenv("serviceNamesLANCIA")
        api = LANCIA(vin, query, serviceNames)
    elif marca == "KIA":
        serviceNames = os.getenv("serviceNamesKIA")
        api = KIA(vin, query, serviceNames)
    elif marca == "JEEP":
        serviceNames = os.getenv("serviceNamesJEEP")
        api = JEEP(vin, query, serviceNames)
    elif marca == "IVECO":
        serviceNames = os.getenv("serviceNamesIVECO")
        api = IVECO(vin, query, serviceNames)
    elif marca == "HYUNDAI":
        serviceNames = os.getenv("serviceNamesHYUNDAI")
        api = HYUNDAI(vin, query, serviceNames)
    elif marca == "FORD":
        serviceNames = os.getenv("serviceNamesFORD")
        api = FORD(vin, query, serviceNames)
    elif marca == "FIAT":
        serviceNames = os.getenv("serviceNamesFIAT")
        api = FIAT(vin, query, serviceNames)
    elif marca == "FIATPro":
        serviceNames = os.getenv("serviceNamesFIATPro")
        api = FIATPro(vin, query, serviceNames)
    elif marca == "CITROEN":
        serviceNames = os.getenv("serviceNamesCITROEN")
        api = CITROEN(vin, query, serviceNames)
    elif marca == "CITROENDS":
        serviceNames = os.getenv("serviceNamesCITROENDs")
        api = CITROENDS(vin, query, serviceNames)
    elif marca == "VAUXHALL":
        serviceNames = os.getenv("serviceNamesVAUXHALL")
        api = VAUXHALL(vin, query, serviceNames)
    else:
        api = False
    try:
        if api.login():
            if api.authorize():
                response_data = api.consulta()
                if response_data:
                    api.procesar_resultados(response_data)
    except:
        print("No se logro crear el objeto API")
