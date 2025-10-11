import time
import requests
import os
import re
import json
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs

# import re

load_dotenv()
ACCOUNT = os.getenv("Account")
USER = os.getenv("User")
PASSWORD = os.getenv("Password")

BRAND_DATA = {
    "ABARTH": {
        "service_name": "abarth_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/abarth_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/abarth_parts/json-bom.action",
    },
    "ALFA": {
        "service_name": "alfa_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/alfa_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/alfa_parts/json-bom.action",
    },
    "ALPINE": {
        "service_name": "alpine_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin_mdl",
        "producto_url": "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details",
    },
    "AUDI": {
        "service_name": "audi_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es",
    },
    "BENTLEY": {
        "service_name": "bentley_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "BMW": {
        "service_name": "bmw_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess?lang=es",
    },
    "BMWCLASSIC": {
        "service_name": "bmwclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
    },
    "BMWMOTORRAD": {
        "service_name": "bmwmotorrad_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
    },
    "BMWMOTORRADCLASSIC": {
        "service_name": "bmwmotorradclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
    },
    "CITROEN": {
        "service_name": "citroen_parts",
        "consulta_url": "https://www.partslink24.com/psa/citroen_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/psa/citroen_parts/scope.action",
    },
    "CITROENDS": {
        "service_name": "citroenDs_parts",
        "consulta_url": "https://www.partslink24.com/psa/citroenDs_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/psa/citroenDs_parts/scope.action",
    },
    "CUPRA": {
        "service_name": "cupra_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "DACIA": {
        "service_name": "dacia_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin_mdl",
        "producto_url": "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details",
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess?lang=es",
    },
    "FIAT": {
        "service_name": "fiatp_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/fiatp_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/fiatp_parts/json-bom.action",
    },
    "FIATPRO": {
        "service_name": "fiatt_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/fiatt_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/fiatt_parts/json-bom.action",
    },
    "FORD": {
        "service_name": "fordp_parts",
        "consulta_url": "https://www.partslink24.com/ford/fordp_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/ford/fordp_parts/bom.action",
    },
    "FORDCOM": {
        "service_name": "fordt_parts",
        "consulta_url": "https://www.partslink24.com/ford/fordt_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/ford/fordt_parts/bom.action",
    },
    "HYUNDAI": {
        "service_name": "hyundai_parts",
        "consulta_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/main-group.action",
    },
    "INFINITY": {
        "service_name": "infinity_parts",
        "consulta_url": "https://www.partslink24.com/nissan/infinity_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/nissan/infinity_parts/main-group.action",
    },
    "IVECO": {
        "service_name": "iveco_parts",
        "consulta_url": "https://www.partslink24.com/iveco/iveco_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/iveco/iveco_parts/drawing.action",
    },
    "JAGUAR": {
        "service_name": "jaguar_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess?lang=es",
    },
    "JEEP": {
        "service_name": "jeep_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/jeep_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/jeep_parts/json-bom.action",
    },
    "KIA": {
        "service_name": "kia_parts",
        "consulta_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/main-group.action",
    },
    "LANCIA": {
        "service_name": "lancia_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-bom.action",
    },
    "LANDROVER": {
        "service_name": "landrover_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess?lang=es",
    },
    "LEXUS": {
        "service_name": "lexus_parts",
        "consulta_url": "https://www.partslink24.com/p5toyota/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails",
    },
    "MAN": {
        "service_name": "man_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "MERCEDES": {
        "service_name": "mercedes_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es",
    },
    "MERCEDEST": {
        "service_name": "mercedestrucks_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
    },
    "MERCEDESU": {
        "service_name": "mercedesunimog_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
    },
    "MERCEDESV": {
        "service_name": "mercedesvans_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es",
    },
    "MINI": {
        "service_name": "mini_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess?lang=es",
    },
    "MINICLASSIC": {
        "service_name": "miniclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
    },
    "MITSUBISHI": {
        "service_name": "mmc_parts",
        "consulta_url": "https://www.partslink24.com/p5mitsubishi/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5mitsubishi/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5mitsubishi/extern/directAccess?lang=es",
    },
    "NISSAN": {
        "service_name": "nissan_parts",
        "consulta_url": "https://www.partslink24.com/nissan/nissan_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/nissan/nissan_parts/main-group.action",
    },
    "OPEL": {
        "service_name": "opel_parts",
        "consulta_url": "https://www.partslink24.com/opel/opel_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/opel/opel_parts/illustration.action",
    },
    "PEUGEOT": {
        "service_name": "peugeot_parts",
        "consulta_url": "https://www.partslink24.com/psa/peugeot_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/psa/peugeot_parts/scope.action",
    },
    "POLESTAR": {
        "service_name": "polestar_parts",
        "consulta_url": "https://www.partslink24.com/volvo/polestar_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/volvo/polestar_parts/illustration.action",
    },
    "PORSCHE": {
        "service_name": "porsche_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es",
    },
    "PORSCHEC": {
        "service_name": "porscheclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "RENAULT": {
        "service_name": "renault_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin_mdl",
        "producto_url": "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details",
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess?lang=es",
    },
    "SEAT": {
        "service_name": "seat_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es",
    },
    "SKODA": {
        "service_name": "skoda_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es",
    },
    "SMART": {
        "service_name": "smart_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es",
    },
    "SUZUKI": {
        "service_name": "suzuki_parts",
        "consulta_url": "https://www.partslink24.com/p5suzuki/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5suzuki/extern/details/vin/bomdetails",
        "datos_url": "https://www.partslink24.com/p5suzuki/extern/directAccess?lang=es",
    },
    "TOYOTA": {
        "service_name": "toyota_parts",
        "consulta_url": "https://www.partslink24.com/p5toyota/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails",
        "datos_url": "https://www.partslink24.com/p5toyota/extern/directAccess?lang=es",
    },
    "VAUXHALL": {
        "service_name": "vauxhall_parts",
        "consulta_url": "https://www.partslink24.com/opel/vauxhall_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/opel/vauxhall_parts/illustration.action",
    },
    "VW": {
        "service_name": "vw_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es",
    },
    "VMCLASSIC": {
        "service_name": "vmclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "VMCOM": {
        "service_name": "vn_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
    },
    "VOLVO": {
        "service_name": "volvo_parts",
        "consulta_url": "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/volvo/volvo_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/volvo/volvo_parts/vin-group.action?hintstoken=154ed8fd-95b0-41ab-ae75-b82397c5d1ba&mode=A0LW0ESES&partnerGroup=46&vin=YV1MW774972274109&lang=es&upds=2025.09.16+13%3A54%3A35&openVinDialog=true",
    },
}

ALL_SERVICES = [datos["service_name"] for datos in BRAND_DATA.values()]


class PartsLink24API:
    def __init__(self, account, user, password):
        self.session = requests.Session()
        self.logout_session = requests.Session()

        self.login_url = (
            "https://www.partslink24.com/partslink24/login-ajax!login.action"
        )
        self.authorize_url = "https://www.partslink24.com/auth/ext/api/1.1/authorize"
        self.logout_url = "https://www.partslink24.com/partslink24/user/logout.do"
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
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.partslink24.com",
            "Referer": "https://www.partslink24.com/partslink24/user/login.do",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.access_token = None
        self.vin = None
        self.session_file = "session_state.json"

    def logout(self):
        # print("Intentando cerrar cualquier sesión previa...")
        try:
            response = self.logout_session.get(
                self.logout_url, headers=self.headers, allow_redirects=False
            )
            # print(f"Petición de logout enviada. {response.content}")
        except requests.RequestException as e:
            print(f"Error durante el logout (se ignorará): {e}")
            return

    def save_session_state(self):
        if not self.access_token:
            return

        session_state = {
            "cookies": self.session.cookies.get_dict(),
            "access_token": self.access_token,
        }
        with open(self.session_file, "w") as f:
            json.dump(session_state, f, indent=4)
        # print(
        #    f"-> Sesión activa guardada correctamente en '{self.session_file}'")

    def load_session_state(self):
        if not os.path.exists(self.session_file):
            return False
        try:
            with open(self.session_file, "r") as f:
                session_state = json.load(f)
            self.session.cookies.update(session_state["cookies"])
            self.access_token = session_state["access_token"]

            return True
        except (json.JSONDecodeError, KeyError):
            return False

    def login(self, service_name):
        self.logout()
        # print("Iniciando proceso de autenticación completo...")
        try:
            response_login = self.session.post(
                self.login_url, data=self.login_data, headers=self.headers
            )
            response_login.raise_for_status()

            login_response_data = response_login.json()
            if not (
                login_response_data.get("status") == "OK"
                and not login_response_data.get("errors")
            ):
                return False
            # print("Login con credenciales exitoso.")
        except requests.RequestException:
            return False

        return True

    def refresh_access_token(self, service_name, is_refresh=True):
        action = "Refrescando" if is_refresh else "Solicitando"
        # print(f"{action} token de acceso...")
        try:
            auth_payload = {"serviceNames": service_name, "withLogin": True}
            response_auth = self.session.post(self.authorize_url, json=auth_payload)
            response_auth.raise_for_status()
            auth_data = response_auth.json()
            self.access_token = auth_data.get("access_token")
            if not self.access_token:
                return False
            #  print("Autorización exitosa. Token recibido/refrescado.")
            return True
        except requests.RequestException:
            return False

    def buscar_pieza(self, vin, query, service_name, search_url, product_url):
        # print(
        #     f"\n--- Iniciando consulta para VIN: {vin}, Pieza: '{query}' ---")
        if not self.access_token:

            return None

        # --- Intento 1: Usar la sesión actual ---
        palabra_clave = query.lower().strip()
        response = self._realizar_consulta(vin, query, service_name, search_url)
        if response and response.status_code == 200:

            parsed_response = self.procesar_resultados(
                response.json(), service_name, vin, product_url, palabra_clave
            )
            # print(parsed_response)
            return parsed_response

        # --- Plan B: Si falla con 401, refrescar token y reintentar ---
        if response is not None and response.status_code == 401:
            # print("Intento 1 fallido (401). Refrescando token (Plan B)...")
            # Usamos la lista completa para refrescar
            refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                response = self._realizar_consulta(vin, query, service_name, search_url)
                if response and response.status_code == 200:
                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, palabra_clave
                    )
                    print(parsed_response)
                    return parsed_response

        # --- Plan C: Si vuelve a fallar, hacer re-login completo y reintentar ---
        if response is not None and response.status_code == 401:
            # print("Intento 2 fallido (401). Realizando re-login completo (Plan C)...")
            # Usamos la lista completa para el nuevo login
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                # print("Archivo de sesión anterior eliminado para un nuevo login.")

            logged = self.login(ALL_SERVICES)
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)

                response = self._realizar_consulta(vin, query, service_name, search_url)
                if response and response.status_code == 200:
                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, palabra_clave
                    )
                    print(parsed_response)
                    return parsed_response
        elif response.status_code == 500:
            return {"error": "Error interno del servidor (500)."}
        # Si llegamos aquí, todos los intentos fallaron.
        print(
            "Error crítico: La consulta falló después de todos los intentos de recuperación."
        )
        return None

    def obtener_datos_coche(self, vin, service_name, search_url):
        """
        Obtiene todos los datos del coche desde PartsLink24 usando el VIN.
        """
        if not self.access_token:
            return None

        # --- Intento 1: Usar la sesión actual ---
        # payload = {
        #     "lang": "es",
        #     "serviceName": service_name,
        #     "q": vin,
        #     "p5v": "1.22.2",
        #     "_": str(int(time.time() * 1000))  # Timestamp dinámico
        # }

        response = self._realizar_consulta_custom(search_url, vin, service_name)

        if response and response.status_code == 200:
            return response.json()  # Devuelve todos los datos del coche

        # --- Plan B: Si falla con 401, refrescar token y reintentar ---
        if response is not None and response.status_code == 401:
            refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                response = self._realizar_consulta_custom(search_url, vin, service_name)
                if response and response.status_code == 200:
                    return response.json()

        # --- Plan C: Si vuelve a fallar, hacer re-login completo y reintentar ---
        if response is not None and response.status_code == 401:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login(ALL_SERVICES)
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                response = self._realizar_consulta_custom(search_url, vin, service_name)
                if response and response.status_code == 200:
                    return response.json()
        elif response is not None and response.status_code == 500:
            return {"error": "Error interno del servidor (500)."}

        # Si llegamos aquí, todos los intentos fallaron.
        print(
            "Error crítico: La consulta falló después de todos los intentos de recuperación."
        )
        return None

    def _realizar_consulta_custom(self, search_url, vin, service_name):
        try:
            headers = self.headers.copy()
            headers["Authorization"] = f"Bearer {self.access_token}"

            # Payload específico para la consulta de datos del coche
            params = {
                "lang": "es",
                "serviceName": service_name,
                "q": vin,
                "p5v": "1.22.2",
                "_": str(int(time.time() * 1000)),  # timestamp dinámico
            }

            response = self.session.get(search_url, headers=headers, params=params)
            return response

        except requests.RequestException as e:
            print(f"Error de red durante la consulta: {e}")
            return None

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        return response_data

    def _realizar_consulta(self, vin, query, service_name, search_url):
        self.vin = vin
        try:
            # self.refresh_access_token(service_name, is_refresh=True)

            headers = self.headers.copy()

            headers["Authorization"] = f"Bearer {self.access_token}"

            params = {"lang": "es", "serviceName": service_name, "vin": vin, "q": query}

            if service_name == "smart_parts":
                params["cat"] = "60J"
                params["productClassId"] = "F"
                params["scope"] = "F"
                params["subAggregate"] = "n-r"
                params["upds"] = "ND"
            elif service_name == "mercedesvans_parts":
                params["cat"] = "60R"
            elif service_name == "mercedes_parts":
                params["cat"] = "63J"

            response = self.session.get(search_url, headers=headers, params=params)

            # print(response.url)

            return response
        except requests.RequestException as e:
            print(f"Error de red durante la consulta: {e}")
            return None


class BmwAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        # Cargamos los datos específicos de BMW
        brand_data = BRAND_DATA.get("BMW", {})
        self.service_name = brand_data.get("service_name")
        self.datos_url = brand_data["datos_url"]


class FordAPI(PartsLink24API):
    pass


class VwAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("VW", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.datos_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        """
        Procesa los resultados, valida piezas en sub-consultas y acumula
        todos los resultados válidos en un único diccionario, evitando duplicados.
        """
        productos_data = {}
        registros_vistos = set()

        records = response_data.get("data", {}).get("records", [])

        for indice, record in enumerate(records):
            if indice >= 3:
                break
            try:
                bt_page = record.get("recordContext", {}).get("bidata_bt_page")
                path_info = record.get("p5goto", {}).get("ws", [{}])[0].get("path", "")

                parsed_url = urlparse(path_info)
                query_params = parse_qs(parsed_url.query)
                illustration_id = query_params.get("illustrationId", [None])[0]
                maingroup = query_params.get("maingroup", [None])[0]

                if not all([bt_page, illustration_id, maingroup]):
                    continue

                params_producto = {
                    "illustrationId": illustration_id,
                    "lang": "es",
                    "maingroup": maingroup,
                    "serviceName": service_name,
                    "vin": vin,
                }
                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.session.get(
                    product_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()
                    crumbs = response_data_product.get("crumbs", [])
                    name_bt_page = next(
                        (
                            c.get("name", "")
                            for c in crumbs
                            if c.get("name", "").startswith(bt_page)
                        ),
                        bt_page,
                    )
                    productos = response_data_product.get("data", {}).get("records", [])

                    for producto in productos:
                        unavailable = producto.get("unavailable", False)
                        values = producto.get("values", {})
                        producto_partno = values.get("partno")
                        nombre_pieza = values.get("description", "N/A").lower().strip()
                        ref_normalizado = None
                        if producto_partno:
                            ref_normalizado = (
                                producto_partno.strip().replace(" ", "").upper()
                            )

                        # Evitar duplicados: clave por ref y grupo
                        clave = (ref_normalizado, name_bt_page)
                        if (
                            unavailable
                            or not ref_normalizado
                            or clave in registros_vistos
                        ):
                            continue
                        registros_vistos.add(clave)

                        datos_pieza = {
                            "name": nombre_pieza,
                            "group": name_bt_page,
                            "unavailable": unavailable,
                        }
                        productos_data[ref_normalizado] = datos_pieza

            except Exception as e:
                print(f"Ocurrió un error procesando un registro de categoría: {e}")
                continue

        print(productos_data)
        return productos_data


class ToyotaAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("TOYOTA", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.datos_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        records = response_data.get("data", {}).get("records", [])
        part_list = []
        counter = 1
        for record in records:
            # Extraer información relevante del record
            part_number = record["values"]["partnumber"]
            position = record["values"]["pos"]
            subgroup_desc = record["values"]["subgroupDescription"]
            part_desc = record["values"]["partDescription"]
            illustration = record["recordContext"]["illustration"]
            bt_page = record["recordContext"]["bt_page"]

            dict_list = {
                "Parte": counter,
                "part_number": part_number,
                "position": position,
                "subgroup_description": subgroup_desc,
                "part_description": part_desc,
                "illustration": illustration,
                "bt_page": bt_page,
            }

            part_list.append(dict_list)

            # Imprimir la información
            # print("=" * 50)  # Separador visual
            # print(f"Parte {counter}")
            # print(f"Part Number: {part_number}")
            # print(f"Position: {position}")
            # print(f"Subgroup Description: {subgroup_desc}")
            # print(f"Part Description: {part_desc}")
            # print(f"Illustration: {illustration}")
            # print(f"BT Page: {bt_page}")
            # print("=" * 50)  # Separador visual
            # print()
            counter += 1
        print(part_list)
        return {"output": part_list}


class SmartAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SMART", {})
        self.service_name = brand_info.get("service_name")
        self.datos_url = brand_info.get("datos_url")


class SuzukiAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SUZUKI", {})
        self.service_name = brand_info.get("service_name")
        self.datos_url = brand_info.get("datos_url")


class SkodaApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SKODA", {})
        self.service_name = brand_info.get("service_name")
        self.datos_url = brand_info.get("datos_url")


class SeatAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SEAT", {})
        self.service_name = brand_info.get("service_name")
        self.datos_url = brand_info.get("datos_url")


class HyundaiApi(PartsLink24API):
    pass


class RenaultAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["RENAULT"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class PorscheAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["PORSCHE"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class JeepApi(PartsLink24API):
    pass


class AudiAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["AUDI"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class MiniAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["MINI"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class MercedesVansAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["MERCEDESV"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class MercedesAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["MERCEDES"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class LandRoverAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["LANDROVER"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class JaguarAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["JAGUAR"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class DaciaAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["DACIA"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


class MitsubishiAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["MITSUBISHI"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]


def mostrar_datos_vehiculo_formateados(datos_coche):
    """
    Función simple para mostrar los datos del vehículo de forma legible
    """
    try:
        print("\n" + "=" * 50)
        print("         INFORMACIÓN DEL VEHÍCULO")
        print("=" * 50)

        # Extraer datos básicos
        records = (
            datos_coche.get("data", {})
            .get("segments", {})
            .get("vinfoBasic", {})
            .get("records", [])
        )

        for record in records:
            values = record.get("values", {})
            descripcion = values.get("description", "")
            valor = values.get("value", "")

            # Limpiar el valor
            if valor:
                valor = valor.strip().replace("\r\n", " ").replace("\n", " ")
                valor = " ".join(valor.split())  # Eliminar espacios múltiples

            print(f"{descripcion}: {valor}")

        print("=" * 50)

    except Exception as e:
        print(f"Error al formatear los datos: {e}")


def test(vin: str, brand: str):
    # Usamos la clase específica de la marca para que sea más limpio
    if brand.upper() == "VW":
        session_manager = VwAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "BMW":
        session_manager = BmwAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "TOYOTA":
        session_manager = ToyotaAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SUZUKI":
        session_manager = SuzukiAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SMART":
        session_manager = SmartAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SKODA":
        session_manager = SkodaApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SEAT":
        session_manager = SeatAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "RENAULT":
        session_manager = RenaultAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "PORSCHE":
        session_manager = PorscheAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MITSUBISHI":
        session_manager = MitsubishiAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MINI":
        session_manager = MiniAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MERCEDESV":
        session_manager = MercedesVansAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MERCEDES":
        session_manager = MercedesAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "LANDROVER":
        session_manager = LandRoverAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "JAGUAR":
        session_manager = JaguarAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "DACIA":
        session_manager = DaciaAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "AUDI":
        session_manager = AudiAPI(ACCOUNT, USER, PASSWORD)
    else:
        # Aquí podrías añadir BmwAPI, etc.
        print(f"Marca {brand} no soportada.")
        return

    is_ready = session_manager.load_session_state()

    if not is_ready:
        # print("No se encontro el archivo de sesion. Realizando login...")
        # La clase VwApi no tiene login, llamamos al de la clase padre
        logged_in = session_manager.login(ALL_SERVICES)
        if logged_in:
            is_ready = session_manager.refresh_access_token(
                ALL_SERVICES, is_refresh=False
            )
            if is_ready:
                session_manager.save_session_state()

    if not is_ready:
        print("Fallo en la autenticación. No se puede continuar.")
        return

    # La clase VwApi ya conoce sus URLs y service_name, no hay que buscarlos.
    datos_coche = session_manager.obtener_datos_coche(
        vin, session_manager.service_name, session_manager.datos_url
    )

    if datos_coche:
        with open(f"{vin}_datos.json", "w", encoding="utf-8") as f:
            json.dump(datos_coche, f, indent=4, ensure_ascii=False)
        print(f"Datos guardados en {vin}_datos.json")

        # Mostrar datos formateados
        mostrar_datos_vehiculo_formateados(datos_coche)
        # Opcional, se imprime el json completo.
        # print(json.dumps(datos_coche, indent=4, ensure_ascii=False))
    else:
        print("No se obtuvieron datos del coche.")

    # session_manager.buscar_pieza(
    #     vin,
    #     query,
    #     session_manager.service_name,
    #     session_manager.consulta_url,
    #     session_manager.producto_url,
    # )


if __name__ == "__main__":

    # if len(sys.argv) != 3:
    #     print(
    #         "Error: Se requieren 2 argumentos: VIN, Marca. Ejemplo: python partslink.py WVWZZZ1KZ4B024648 'vw' "
    #     )
    #     sys.exit(1)
    # vin = sys.argv[1]
    # marca = sys.argv[2]

    # marca = "smart"
    # vin = "WME4513311K043393"
    # pieza = "Espejos retrovisores"

    # # vin = "WBA51CM0108C22188"

    # vin = "JTEBZ29J100180316"
    # marca = "toyota"
    # pieza = "panel de puerta"

    # WVWZZZ1KZ8W204031
    # WVWZZZ9NZ4Y177451
    # WVGZZZ5NZ9W079782

    # marca = "porsche"
    # pieza = "Cerradura de la puerta"
    # vin = "WP1ZZZ92ZFLA35688"

    marca = "mitsubishi"
    vin = "4MBMND32ATE001965"

    if not all([ACCOUNT, USER, PASSWORD, ALL_SERVICES]):
        print(
            "Error: Asegúrate de que 'Account', 'User', 'Password' y 'serviceNamesBMW' están en tu .env"
        )
    else:

        test(vin, marca)
