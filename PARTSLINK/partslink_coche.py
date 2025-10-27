import time
import requests
import os
import re
import json
import sys
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
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
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess?lang=es"
        
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
        "datos_url": "https://www.partslink24.com/iveco/iveco_parts/vin-group.action?hintstoken=397fcf73-35a0-4bbe-8e80-7ade3a0539e2&mode=A0LW0ESES&vin=ZCFC3070105209146&lang=es&upds=2025.09.26+18%3A46%3A59+CEST&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/iveco/iveco_parts/vin-group.action"
    },
    "JAGUAR": {
        "service_name": "jaguar_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/vin-group.action?hintstoken=71debd71-4de1-46b8-a43a-8f052f34a1b7&mode=A0LW0ESES&vin=KNEUP751256716941&lang=es&upds=2025.09.30+06%3A41%3A41+UTC&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/vin-group.action"
    },
    "LANCIA": {
        "service_name": "lancia_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/lancia_parts/vin-group.action?hintstoken=854daa53-1f8e-42be-947a-e44a7aaa6a7f&mode=A0LW0ESES&sincom=&vin=ZLA17900013377390&lang=es&upds=2025.09.17+10%3A40%3A29+CEST&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/fiatspa/lancia_parts/vin-group.action"
    },
    "LANDROVER": {
        "service_name": "landrover_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es"
    },
    "MINI": {
        "service_name": "mini_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5mitsubishi/extern/directAccess?lang=es"
    },
    "NISSAN": {
        "service_name": "nissan_parts",
        "consulta_url": "https://www.partslink24.com/nissan/nissan_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/nissan/nissan_parts/main-group.action",
        "datos_url": "https://www.partslink24.com/nissan/nissan_parts/vin-group.action?hintstoken=7ab74440-33c4-49b8-b2f6-58ff3ac9438a&mode=A0LW0ESES&testmode=&vin=SJNFDAE11U1245311&lang=es&upds=2025.09.03+14%3A13%3A16+UTC&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/nissan/nissan_parts/vin-group.action"
    },
    "OPEL": {
        "service_name": "opel_parts",
        "consulta_url": "https://www.partslink24.com/opel/opel_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/opel/opel_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/opel/opel_parts/vin-group.action?hintstoken=example&mode=A0LW0ESES&vin=EXAMPLE&lang=es&upds=2025.09.16+13%3A54%3A35&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/opel/opel_parts/vin-group.action"
    },
    "PEUGEOT": {
        "service_name": "peugeot_parts",
        "consulta_url": "https://www.partslink24.com/psa/peugeot_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/psa/peugeot_parts/scope.action",
        "datos_url": "https://www.partslink24.com/psa/peugeot_parts/vin-group.action?hintstoken=90f186ec-9b48-4d2f-a830-4f61c067b129&mode=A0LW0ESES&lang=es&upds=2024.02.13+09%3A27%3A21+CET&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/psa/peugeot_parts/vin-group.action"
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
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess?lang=es"
    },
    "SEAT": {
        "service_name": "seat_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es"
    },
    "SKODA": {
        "service_name": "skoda_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess?lang=es"
    },
    "SMART": {
        "service_name": "smart_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess?lang=es"
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
        "datos_url": "https://www.partslink24.com/p5toyota/extern/directAccess?lang=es"
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
        "datos_url":"https://www.partslink24.com/volvo/volvo_parts/vin-group.action?hintstoken=154ed8fd-95b0-41ab-ae75-b82397c5d1ba&mode=A0LW0ESES&partnerGroup=46&vin=YV1MW774972274109&lang=es&upds=2025.09.16+13%3A54%3A35&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/volvo/volvo_parts/vin-group.action"
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
            response_auth = self.session.post(
                self.authorize_url, json=auth_payload)
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
        response = self._realizar_consulta(
            vin, query, service_name, search_url)
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
            refrescar_token = self.refresh_access_token(
                ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                response = self._realizar_consulta(
                    vin, query, service_name, search_url)
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

                response = self._realizar_consulta(
                    vin, query, service_name, search_url)
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
            # Check if response is JSON or HTML
            content_type = response.headers.get('content-type', '').lower()
            
            if 'application/json' in content_type:
                try:
                    return response.json()  # Devuelve todos los datos del coche
                except ValueError as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Response content: {response.text[:500]}...")
                    return None
            else:
                # Handle HTML response (like Peugeot)
                print(f"Received HTML response instead of JSON")
                print(f"Response content: {response.text[:500]}...")
                print(f"Status code: {response.status_code}")
                print(f"Content-Type: {content_type}")
                print("Test")
                # For debugging, let's return the raw text for now
                return {
                    "raw_html": response.text,
                    "status_code": response.status_code,
                    "content_type": content_type,
                    "url": response.url
                }

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
        print("Error crítico: La consulta falló después de todos los intentos de recuperación.")
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
                "_": str(int(time.time() * 1000))  # timestamp dinámico
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

            params = {"lang": "es", "serviceName": service_name,
                      "vin": vin, "q": query}

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

            response = self.session.get(
                search_url, headers=headers, params=params)

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

class ToyotaAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("TOYOTA", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.datos_url = brand_info.get("datos_url")

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

class KiaAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        self.datos_url_base = BRAND_DATA["KIA"]["datos_url_base"]

    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        print(f"[KIA DEBUG] Iniciando obtener_datos_coche para VIN: {vin}")
        
        # Verificar access_token
        access_token = self.session.cookies.get('access_token')
        print(f"[KIA DEBUG] Access token presente: {access_token is not None}")
        if access_token:
            print(f"[KIA DEBUG] Access token valor: {access_token[:50]}...")
        
        # Verificar cookies de sesión
        print(f"[KIA DEBUG] Cookies de sesión: {dict(self.session.cookies)}")
        
        payload = {
            "vin": vin,
            "mode": "A0LW0ESES",
            "lang": "es",
            "openVinDialog": "true"
        }
        
        print(f"[KIA DEBUG] Payload completo: {payload}")
        print(f"[KIA DEBUG] URL objetivo: {self.datos_url_base}")
        
        self.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        print(f"[KIA DEBUG] Headers: {self.headers}")
        
        response = self.session.post(self.datos_url_base, data=payload, headers=self.headers)
        
        print(f"[KIA DEBUG] Status de respuesta: {response.status_code}")
        print(f"[KIA DEBUG] Primeros 500 caracteres de respuesta: {response.text[:500]}")
        
        # Detectar modo demo
        if "demo" in response.text.lower() or "login" in response.text.lower():
            print("[KIA DEBUG] ⚠️ DETECTADO MODO DEMO O LOGIN - Posible problema de autenticación")
        
        return response
        
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


class PeugeotAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["PEUGEOT"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
    
    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        """
        Método personalizado para Peugeot que envía el VIN en el payload POST
        """
        if service_name is None:
            service_name = self.service_name
        
        print(f"🔍 PEUGEOT - Enviando consulta para VIN: {vin}")
        
        # Preparar datos para enviar en el POST
        payload = {
            'vin': vin,
            'lang': 'es',
            'mode': 'A0LW0ESES',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición
        headers = self.headers.copy()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        print(f"📤 PEUGEOT - Payload enviado: {payload}")
        print(f"🌐 PEUGEOT - URL destino: {self.datos_url_base}")
        
        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 PEUGEOT - Respuesta recibida - Status: {response.status_code}")
        
        return response

class NissanAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["NISSAN"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
    
    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        """
        Método personalizado para Peugeot que envía el VIN en el payload POST
        """
        if service_name is None:
            service_name = self.service_name
        
        print(f"🔍 NISSAN - Enviando consulta para VIN: {vin}")
        
        # Preparar datos para enviar en el POST
        payload = {
            'vin': vin,
            'lang': 'es',
            'mode': 'A0LW0ESES',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición
        headers = self.headers.copy()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        print(f"📤 NISSAN - Payload enviado: {payload}")
        print(f"🌐 NISSAN - URL destino: {self.datos_url_base}")
        
        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 PEUGEOT - Respuesta recibida - Status: {response.status_code}")
        
        return response

class VolvoAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["VOLVO"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
    
    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        """
        Método personalizado para Volvo que envía el VIN en el payload POST
        """
        if service_name is None:
            service_name = self.service_name
        
        print(f"🔍 VOLVO - Enviando consulta para VIN: {vin}")
        
        # Preparar datos para enviar en el POST
        payload = {
            'vin': vin,
            'lang': 'es',
            'mode': 'A0LW0ESES',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición
        headers = self.headers.copy()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        print(f"📤 VOLVO - Payload enviado: {payload}")
        print(f"🌐 VOLVO - URL destino: {self.datos_url_base}")
        
        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 VOLVO - Respuesta recibida - Status: {response.status_code}")
        
        return response

class OpelAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["OPEL"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        """Obtener datos del coche para OPEL usando POST con VIN en el payload"""
        
        # Payload para la petición POST
        payload = {
            'vin': vin,
            'mode': 'A0LW0ESES',
            'lang': 'es',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición
        headers = self.headers.copy()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        print(f"📤 OPEL - Payload enviado: {payload}")
        print(f"🌐 OPEL - URL destino: {self.datos_url_base}")
        
        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 OPEL - Respuesta recibida - Status: {response.status_code}")
        
        return response

class LanciaAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["LANCIA"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
        
    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        """Obtener datos del coche para LANCIA usando POST con VIN en el payload"""
        
        # Payload para la petición POST
        payload = {
            'vin': vin,
            'mode': 'A0LW0ESES',
            'lang': 'es',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición
        headers = self.headers.copy()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        print(f"📤 LANCIA - Payload enviado: {payload}")
        print(f"🌐 LANCIA - URL destino: {self.datos_url_base}")
        
        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 LANCIA - Respuesta recibida - Status: {response.status_code}")
        
        return response

class IvecoAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["IVECO"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

    def obtener_datos_coche(self, vin, service_name=None, datos_url_base=None):
        print(f"[IVECO DEBUG] Iniciando obtener_datos_coche para VIN: {vin}")
        print(f"[IVECO DEBUG] Access token presente: {bool(self.access_token)}")
        print(f"[IVECO DEBUG] Access token valor: {self.access_token}")
        print(f"[IVECO DEBUG] Session cookies: {dict(self.session.cookies)}")
        
        payload = {
            "vin": vin,
            "mode": "A0LW0ESES",
            "lang": "es",
            "openVinDialog": "true"
        }
        
        print(f"[IVECO DEBUG] Payload completo: {payload}")
        print(f"[IVECO DEBUG] URL objetivo: {datos_url_base}")
        
        self.headers.update({
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        })
        
        print(f"[IVECO DEBUG] Headers: {self.headers}")
        
        response = self.session.post(datos_url_base, data=payload, headers=self.headers)
        
        print(f"[IVECO DEBUG] Status code: {response.status_code}")
        print(f"[IVECO DEBUG] Response content (primeros 500 chars): {response.text[:500]}")
        
        # Detectar modo demo
        if "demo" in response.text.lower() or "demonstration" in response.text.lower():
            print("[IVECO DEBUG] ¡DETECTADO MODO DEMO!")
        
        return response

def procesar_respuesta_html(response, vin, marca, datos_url):
    """
    Función para procesar respuestas HTML de marcas como Peugeot, Nissan y Volvo
    """
    try:
        # Guardar el HTML para depuración
        html_filename = f"debug_html_{marca}_{vin}_{int(time.time())}.html"
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"📄 HTML guardado en: {html_filename}")
        
        # Parsear el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar la tabla con información del vehículo
        tabla_info = soup.find('table', class_='vinInfoTable')
        
        datos_coche = {
            "vin": vin,
            "marca": marca.upper(),
            "datos_url": datos_url,
            "html_file": html_filename
        }
        
        if tabla_info:
            print(f"✅ Tabla vinInfoTable encontrada para {marca}")
            
            # Extraer todas las filas de la tabla
            filas = tabla_info.find_all('tr')
            
            for fila in filas:
                celdas = fila.find_all('td')
                
                # Procesar filas con 2 o 4 celdas (campo-valor o campo-valor-campo-valor)
                if len(celdas) == 2:
                    campo = celdas[0].get_text(strip=True).upper()
                    valor = celdas[1].get_text(strip=True)
                    
                    # Mapear campos comunes
                    if "NÚMERO DE CHASIS" in campo or "VIN" in campo:
                        datos_coche["numero_chasis"] = valor
                    elif "MODELO" in campo:
                        datos_coche["modelo"] = valor
                    elif "DAM" in campo:
                        datos_coche["dam"] = valor
                    elif "CÓDIGO DE FÁBRICA" in campo:
                        datos_coche["codigo_fabrica"] = valor
                    elif "TIPO DE PRODUCTO" in campo:
                        datos_coche["tipo_producto"] = valor
                    elif "MARCA COMERCIAL" in campo or "TIPO DE ÓRGANO" in campo:
                        datos_coche["marca_comercial"] = valor
                    elif "SILUETA" in campo:
                        datos_coche["silueta"] = valor
                    elif "ACABADO" in campo:
                        datos_coche["acabado"] = valor
                    elif "MOTOR" in campo or "Motor" in campo:
                        datos_coche["motor"] = valor
                    elif "TRANSMISIÓN" in campo or "Caja de cambios" in campo:
                        datos_coche["transmision"] = valor
                    elif "BASE DE CONCEPCIÓN" in campo:
                        datos_coche["base_concepcion"] = valor
                    elif "CRITERIO DE VARIANTE" in campo or "CLIENTELA CONCEPCIÓN" in campo:
                        datos_coche["criterio_variante"] = valor
                    elif "AÑO MODELO" in campo:
                        datos_coche["año_modelo"] = valor
                    elif "TIPO DE PINTURA" in campo:
                        datos_coche["tipo_pintura"] = valor
                    elif "COLOR DE CARROCERÍA" in campo:
                        datos_coche["color_carroceria"] = valor
                    elif "TIPO DE REVESTIMIENTO INTERIOR" in campo:
                        datos_coche["revestimiento_interior"] = valor
                    elif "COLOR DE GUARNECIDO" in campo:
                        datos_coche["color_guarnecido"] = valor
                    
                    # Campos específicos de Nissan
                    elif "Desde" in campo:
                        datos_coche["fecha_desde"] = valor
                    elif "Chasis" in campo:
                        datos_coche["tipo_chasis"] = valor
                    elif "Clasificación" in campo:
                        datos_coche["clasificacion"] = valor
                    elif "Área de distribución" in campo:
                        datos_coche["area_distribucion"] = valor
                    elif "Tipo" in campo:
                        datos_coche["tipo"] = valor
                    elif "Color exterior" in campo:
                        datos_coche["color_exterior"] = valor
                    elif "Color interior" in campo:
                        datos_coche["color_interior"] = valor
                    
                    # Campos específicos de Volvo
                    elif "AÑO DE FABRICACIÓN" in campo:
                        datos_coche["año_fabricacion"] = valor
                    elif "UNIDAD DE VELOCIDAD" in campo:
                        datos_coche["unidad_velocidad"] = valor
                    elif "Nº PROD. MECANISMO DE DIRECCIÓN" in campo:
                        datos_coche["numero_mecanismo_direccion"] = valor
                    elif "SEMANA DE ESTRUCTURACIÓN" in campo:
                        datos_coche["semana_estructuracion"] = valor
                    elif "GRUPO DE SOCIO" in campo:
                        datos_coche["grupo_socio"] = valor
                    elif "CÓDIGO DE TAPIZADO/INTERIOR" in campo:
                        datos_coche["codigo_tapizado"] = valor
                    elif "TAPIZADO/EQUIPAMIENTO INTERIOR" in campo:
                        datos_coche["tapizado_interior"] = valor
                    elif "CÓDIGO DE ESTILO DE CARROCERÍA" in campo:
                        datos_coche["codigo_estilo_carroceria"] = valor
                    elif "TIPO DE CARROCERÍA" in campo:
                        datos_coche["tipo_carroceria"] = valor
                    elif "CÓDIGO DE VEHÍCULO ESPECIAL" in campo:
                        datos_coche["codigo_vehiculo_especial"] = valor
                    elif "VEHÍCULOS ESPECIALES" in campo:
                        datos_coche["vehiculos_especiales"] = valor
                    elif "TIPO DE VENTA" in campo:
                        datos_coche["tipo_venta"] = valor
                    elif "CÓDIGO DE MERCADO" in campo:
                        datos_coche["codigo_mercado"] = valor
                    elif "MARCA" in campo and len(valor) <= 5:  # Para distinguir de "marca comercial"
                        datos_coche["marca_mercado"] = valor
                    elif "CÓDIGO DEL MOTOR" in campo:
                        datos_coche["codigo_motor"] = valor
                    elif "Nº PIEZA DE MOTOR" in campo:
                        datos_coche["numero_pieza_motor"] = valor
                    elif "NÚMERO DE SERIE DEL MOTOR" in campo:
                        datos_coche["numero_serie_motor"] = valor
                    elif "CÓDIGO DE LA TRANSMISIÓN" in campo:
                        datos_coche["codigo_transmision"] = valor
                
                elif len(celdas) == 4:
                    # Procesar dos pares campo-valor en la misma fila
                    campo1 = celdas[0].get_text(strip=True).upper()
                    valor1 = celdas[1].get_text(strip=True)
                    campo2 = celdas[2].get_text(strip=True).upper()
                    valor2 = celdas[3].get_text(strip=True)
                    
                    # Procesar primer par
                    if "NÚMERO DE CHASIS" in campo1 or "VIN" in campo1:
                        datos_coche["numero_chasis"] = valor1
                    elif "MODELO" in campo1:
                        datos_coche["modelo"] = valor1
                    elif "DAM" in campo1:
                        datos_coche["dam"] = valor1
                    elif "CÓDIGO DE FÁBRICA" in campo1:
                        datos_coche["codigo_fabrica"] = valor1
                    elif "TIPO DE PRODUCTO" in campo1:
                        datos_coche["tipo_producto"] = valor1
                    elif "MARCA COMERCIAL" in campo1 or "TIPO DE ÓRGANO" in campo1:
                        datos_coche["marca_comercial"] = valor1
                    elif "SILUETA" in campo1:
                        datos_coche["silueta"] = valor1
                    elif "ACABADO" in campo1:
                        datos_coche["acabado"] = valor1
                    elif "MOTOR" in campo1 or "Motor" in campo1:
                        datos_coche["motor"] = valor1
                    elif "TRANSMISIÓN" in campo1 or "Caja de cambios" in campo1:
                        datos_coche["transmision"] = valor1
                    elif "BASE DE CONCEPCIÓN" in campo1:
                        datos_coche["base_concepcion"] = valor1
                    elif "CRITERIO DE VARIANTE" in campo1 or "CLIENTELA CONCEPCIÓN" in campo1:
                        datos_coche["criterio_variante"] = valor1
                    elif "AÑO MODELO" in campo1:
                        datos_coche["año_modelo"] = valor1
                    elif "TIPO DE PINTURA" in campo1:
                        datos_coche["tipo_pintura"] = valor1
                    elif "COLOR DE CARROCERÍA" in campo1:
                        datos_coche["color_carroceria"] = valor1
                    elif "TIPO DE REVESTIMIENTO INTERIOR" in campo1:
                        datos_coche["revestimiento_interior"] = valor1
                    elif "COLOR DE GUARNECIDO" in campo1:
                        datos_coche["color_guarnecido"] = valor1
                    
                    # Campos específicos de Nissan (primer par)
                    elif "Desde" in campo1:
                        datos_coche["fecha_desde"] = valor1
                    elif "Chasis" in campo1:
                        datos_coche["tipo_chasis"] = valor1
                    elif "Clasificación" in campo1:
                        datos_coche["clasificacion"] = valor1
                    elif "Área de distribución" in campo1:
                        datos_coche["area_distribucion"] = valor1
                    elif "Tipo" in campo1:
                        datos_coche["tipo"] = valor1
                    elif "Color exterior" in campo1:
                        datos_coche["color_exterior"] = valor1
                    elif "Color interior" in campo1:
                        datos_coche["color_interior"] = valor1
                    
                    # Campos específicos de Volvo (primer par)
                    elif "AÑO DE FABRICACIÓN" in campo1:
                        datos_coche["año_fabricacion"] = valor1
                    elif "UNIDAD DE VELOCIDAD" in campo1:
                        datos_coche["unidad_velocidad"] = valor1
                    elif "Nº PROD. MECANISMO DE DIRECCIÓN" in campo1:
                        datos_coche["numero_mecanismo_direccion"] = valor1
                    elif "SEMANA DE ESTRUCTURACIÓN" in campo1:
                        datos_coche["semana_estructuracion"] = valor1
                    elif "GRUPO DE SOCIO" in campo1:
                        datos_coche["grupo_socio"] = valor1
                    elif "CÓDIGO DE TAPIZADO/INTERIOR" in campo1:
                        datos_coche["codigo_tapizado"] = valor1
                    elif "TAPIZADO/EQUIPAMIENTO INTERIOR" in campo1:
                        datos_coche["tapizado_interior"] = valor1
                    elif "CÓDIGO DE ESTILO DE CARROCERÍA" in campo1:
                        datos_coche["codigo_estilo_carroceria"] = valor1
                    elif "TIPO DE CARROCERÍA" in campo1:
                        datos_coche["tipo_carroceria"] = valor1
                    elif "CÓDIGO DE VEHÍCULO ESPECIAL" in campo1:
                        datos_coche["codigo_vehiculo_especial"] = valor1
                    elif "VEHÍCULOS ESPECIALES" in campo1:
                        datos_coche["vehiculos_especiales"] = valor1
                    elif "TIPO DE VENTA" in campo1:
                        datos_coche["tipo_venta"] = valor1
                    elif "CÓDIGO DE MERCADO" in campo1:
                        datos_coche["codigo_mercado"] = valor1
                    elif "MARCA" in campo1 and len(valor1) <= 5:
                        datos_coche["marca_mercado"] = valor1
                    elif "CÓDIGO DEL MOTOR" in campo1:
                        datos_coche["codigo_motor"] = valor1
                    elif "Nº PIEZA DE MOTOR" in campo1:
                        datos_coche["numero_pieza_motor"] = valor1
                    elif "NÚMERO DE SERIE DEL MOTOR" in campo1:
                        datos_coche["numero_serie_motor"] = valor1
                    elif "CÓDIGO DE LA TRANSMISIÓN" in campo1:
                        datos_coche["codigo_transmision"] = valor1
                    
                    # Procesar segundo par (repetir la misma lógica para campo2/valor2)
                    if "NÚMERO DE CHASIS" in campo2 or "VIN" in campo2:
                        datos_coche["numero_chasis"] = valor2
                    elif "MODELO" in campo2:
                        datos_coche["modelo"] = valor2
                    elif "DAM" in campo2:
                        datos_coche["dam"] = valor2
                    elif "CÓDIGO DE FÁBRICA" in campo2:
                        datos_coche["codigo_fabrica"] = valor2
                    elif "TIPO DE PRODUCTO" in campo2:
                        datos_coche["tipo_producto"] = valor2
                    elif "MARCA COMERCIAL" in campo2 or "TIPO DE ÓRGANO" in campo2:
                        datos_coche["marca_comercial"] = valor2
                    elif "SILUETA" in campo2:
                        datos_coche["silueta"] = valor2
                    elif "ACABADO" in campo2:
                        datos_coche["acabado"] = valor2
                    elif "MOTOR" in campo2 or "Motor" in campo2:
                        datos_coche["motor"] = valor2
                    elif "TRANSMISIÓN" in campo2 or "Caja de cambios" in campo2:
                        datos_coche["transmision"] = valor2
                    elif "BASE DE CONCEPCIÓN" in campo2:
                        datos_coche["base_concepcion"] = valor2
                    elif "CRITERIO DE VARIANTE" in campo2 or "CLIENTELA CONCEPCIÓN" in campo2:
                        datos_coche["criterio_variante"] = valor2
                    elif "AÑO MODELO" in campo2:
                        datos_coche["año_modelo"] = valor2
                    elif "TIPO DE PINTURA" in campo2:
                        datos_coche["tipo_pintura"] = valor2
                    elif "COLOR DE CARROCERÍA" in campo2:
                        datos_coche["color_carroceria"] = valor2
                    elif "TIPO DE REVESTIMIENTO INTERIOR" in campo2:
                        datos_coche["revestimiento_interior"] = valor2
                    elif "COLOR DE GUARNECIDO" in campo2:
                        datos_coche["color_guarnecido"] = valor2
                    
                    # Campos específicos de Nissan (segundo par)
                    elif "Desde" in campo2:
                        datos_coche["fecha_desde"] = valor2
                    elif "Chasis" in campo2:
                        datos_coche["tipo_chasis"] = valor2
                    elif "Clasificación" in campo2:
                        datos_coche["clasificacion"] = valor2
                    elif "Área de distribución" in campo2:
                        datos_coche["area_distribucion"] = valor2
                    elif "Tipo" in campo2:
                        datos_coche["tipo"] = valor2
                    elif "Color exterior" in campo2:
                        datos_coche["color_exterior"] = valor2
                    elif "Color interior" in campo2:
                        datos_coche["color_interior"] = valor2
                    
                    # Campos específicos de Volvo (segundo par)
                    elif "AÑO DE FABRICACIÓN" in campo2:
                        datos_coche["año_fabricacion"] = valor2
                    elif "UNIDAD DE VELOCIDAD" in campo2:
                        datos_coche["unidad_velocidad"] = valor2
                    elif "Nº PROD. MECANISMO DE DIRECCIÓN" in campo2:
                        datos_coche["numero_mecanismo_direccion"] = valor2
                    elif "SEMANA DE ESTRUCTURACIÓN" in campo2:
                        datos_coche["semana_estructuracion"] = valor2
                    elif "GRUPO DE SOCIO" in campo2:
                        datos_coche["grupo_socio"] = valor2
                    elif "CÓDIGO DE TAPIZADO/INTERIOR" in campo2:
                        datos_coche["codigo_tapizado"] = valor2
                    elif "TAPIZADO/EQUIPAMIENTO INTERIOR" in campo2:
                        datos_coche["tapizado_interior"] = valor2
                    elif "CÓDIGO DE ESTILO DE CARROCERÍA" in campo2:
                        datos_coche["codigo_estilo_carroceria"] = valor2
                    elif "TIPO DE CARROCERÍA" in campo2:
                        datos_coche["tipo_carroceria"] = valor2
                    elif "CÓDIGO DE VEHÍCULO ESPECIAL" in campo2:
                        datos_coche["codigo_vehiculo_especial"] = valor2
                    elif "VEHÍCULOS ESPECIALES" in campo2:
                        datos_coche["vehiculos_especiales"] = valor2
                    elif "TIPO DE VENTA" in campo2:
                        datos_coche["tipo_venta"] = valor2
                    elif "CÓDIGO DE MERCADO" in campo2:
                        datos_coche["codigo_mercado"] = valor2
                    elif "MARCA" in campo2 and len(valor2) <= 5:
                        datos_coche["marca_mercado"] = valor2
                    elif "CÓDIGO DEL MOTOR" in campo2:
                        datos_coche["codigo_motor"] = valor2
                    elif "Nº PIEZA DE MOTOR" in campo2:
                        datos_coche["numero_pieza_motor"] = valor2
                    elif "NÚMERO DE SERIE DEL MOTOR" in campo2:
                        datos_coche["numero_serie_motor"] = valor2
                    elif "CÓDIGO DE LA TRANSMISIÓN" in campo2:
                        datos_coche["codigo_transmision"] = valor2
            
            print(f"✅ Datos del vehículo {marca} extraídos exitosamente")
            print(f"📋 Campos extraídos: {list(datos_coche.keys())}")
            
            # Actualizar el estado
            datos_coche["estado"] = "Datos extraídos exitosamente de vinInfoTable"
        else:
            print(f"⚠️ No se encontró la tabla vinInfoTable en el HTML")
            print(f"🔍 Buscando otras tablas...")
            todas_tablas = soup.find_all('table')
            print(f"📊 Se encontraron {len(todas_tablas)} tablas en total")
            for i, tabla in enumerate(todas_tablas):
                print(f"  Tabla {i+1}: class='{tabla.get('class')}', id='{tabla.get('id')}'")
                if i < 3:  # Mostrar contenido de las primeras 3 tablas
                    print(f"    Contenido: {tabla.get_text()[:100]}...")
            
            datos_coche["estado"] = "No se encontró vinInfoTable - requiere análisis manual"
        
        return datos_coche
        
    except Exception as e:
        print(f"Error al procesar respuesta HTML: {e}")
        return {
            "vin": vin,
            "marca": marca.upper(),
            "error": str(e),
            "estado": "Error al procesar HTML"
        }


def mostrar_datos_vehiculo_html_formateados(datos_coche):
    """
    Función para mostrar los datos del vehículo extraídos de HTML de forma legible
    """
    try:
        print("\n" + "="*50)
        print("         INFORMACIÓN DEL VEHÍCULO (HTML)")
        print("="*50)
        
        # Mostrar información básica
        print(f"VIN: {datos_coche.get('vin', 'No disponible')}")
        print(f"Marca: {datos_coche.get('marca', 'No disponible')}")
        print(f"Estado: {datos_coche.get('estado', 'No disponible')}")
        print("-" * 50)
        
        # Mostrar datos específicos del vehículo
        campos_vehiculo = [
            # Campos comunes (Peugeot/Nissan/Volvo)
            ("Número de chasis", "numero_chasis"),
            ("Modelo", "modelo"),
            ("DAM", "dam"),
            ("Código de fábrica", "codigo_fabrica"),
            ("Tipo de producto", "tipo_producto"),
            ("Marca comercial", "marca_comercial"),
            ("Silueta", "silueta"),
            ("Acabado", "acabado"),
            ("Motor", "motor"),
            ("Transmisión", "transmision"),
            ("Base de concepción", "base_concepcion"),
            ("Criterio de variante", "criterio_variante"),
            ("Año modelo", "año_modelo"),
            ("Tipo de pintura", "tipo_pintura"),
            ("Color de carrocería", "color_carroceria"),
            ("Revestimiento interior", "revestimiento_interior"),
            ("Color de guarnecido", "color_guarnecido"),
            
            # Campos específicos de Nissan
            ("Fecha desde", "fecha_desde"),
            ("Tipo de chasis", "tipo_chasis"),
            ("Clasificación", "clasificacion"),
            ("Área de distribución", "area_distribucion"),
            ("Tipo", "tipo"),
            ("Color exterior", "color_exterior"),
            ("Color interior", "color_interior"),
            
            # Campos específicos de Volvo
            ("Año de fabricación", "año_fabricacion"),
            ("Unidad de velocidad", "unidad_velocidad"),
            ("Nº prod. mecanismo de dirección", "numero_mecanismo_direccion"),
            ("Semana de estructuración", "semana_estructuracion"),
            ("Grupo de socio", "grupo_socio"),
            ("Código de tapizado/interior", "codigo_tapizado"),
            ("Tapizado/equipamiento interior", "tapizado_interior"),
            ("Código de estilo de carrocería", "codigo_estilo_carroceria"),
            ("Tipo de carrocería", "tipo_carroceria"),
            ("Código de vehículo especial", "codigo_vehiculo_especial"),
            ("Vehículos especiales", "vehiculos_especiales"),
            ("Tipo de venta", "tipo_venta"),
            ("Código de mercado", "codigo_mercado"),
            ("Marca mercado", "marca_mercado"),
            ("Código del motor", "codigo_motor"),
            ("Nº pieza de motor", "numero_pieza_motor"),
            ("Número de serie del motor", "numero_serie_motor"),
            ("Código de la transmisión", "codigo_transmision")
        ]
        
        for descripcion, clave in campos_vehiculo:
            valor = datos_coche.get(clave, "")
            if valor:
                print(f"{descripcion}: {valor}")
        
        print("="*50)
        
    except Exception as e:
        print(f"Error al formatear los datos HTML: {e}")


def mostrar_datos_vehiculo_formateados(datos_coche):
    """
    Función simple para mostrar los datos del vehículo de forma legible
    """
    try:
        print("\n" + "="*50)
        print("         INFORMACIÓN DEL VEHÍCULO")
        print("="*50)
        
        # Extraer datos básicos
        records = datos_coche.get("data", {}).get("segments", {}).get("vinfoBasic", {}).get("records", [])
        
        for record in records:
            values = record.get("values", {})
            descripcion = values.get("description", "")
            valor = values.get("value", "")
            
            # Limpiar el valor
            if valor:
                valor = valor.strip().replace('\r\n', ' ').replace('\n', ' ')
                valor = ' '.join(valor.split())  # Eliminar espacios múltiples
            
            print(f"{descripcion}: {valor}")
        
        print("="*50)
        
    except Exception as e:
        print(f"Error al formatear los datos: {e}")

def test(vin: str, brand: str):
    # Marcas que devuelven HTML en lugar de JSON
    MARCAS_HTML = ["PEUGEOT", "NISSAN", "VOLVO", "OPEL", "LANCIA", "KIA", "IVECO"]
    
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
    elif brand.upper() == "PEUGEOT":
        session_manager = PeugeotAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "NISSAN":
        session_manager = NissanAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "VOLVO":
        session_manager = VolvoAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "OPEL":
        session_manager = OpelAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "LANCIA":
        session_manager = LanciaAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "KIA":
        session_manager = KiaAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "IVECO":
        session_manager = IvecoAPI(ACCOUNT, USER, PASSWORD)
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
                ALL_SERVICES, is_refresh=False)
            if is_ready:
                session_manager.save_session_state()

    if not is_ready:
        print("Fallo en la autenticación. No se puede continuar.")
        return

    # La clase VwApi ya conoce sus URLs y service_name, no hay que buscarlos.
    resultado = session_manager.obtener_datos_coche(
        vin,
        session_manager.service_name,
        session_manager.datos_url
    )
    # Determinar el tipo de respuesta y procesarla adecuadamente
    if brand.upper() in MARCAS_HTML:
        # Procesar respuesta HTML
        if resultado and hasattr(resultado, 'status_code'):
            datos_coche = procesar_respuesta_html(resultado, vin, brand, session_manager.datos_url)
        else:
            print("No se obtuvo respuesta válida de la marca HTML.")
            return
    else:
        # Para otras marcas, el resultado ya es un diccionario JSON
        datos_coche = resultado

    if datos_coche:
        with open(f"{vin}_datos.json", "w", encoding="utf-8") as f:
            json.dump(datos_coche, f, indent=4, ensure_ascii=False)
        print(f"Datos guardados en {vin}_datos.json")

        # Mostrar datos formateados según el tipo de respuesta
        if brand.upper() in MARCAS_HTML:
            mostrar_datos_vehiculo_html_formateados(datos_coche)
        else:
            mostrar_datos_vehiculo_formateados(datos_coche)
        
        #Opcional, se imprime el json completo. 
        #print(json.dumps(datos_coche, indent=4, ensure_ascii=False))
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

    if len(sys.argv) != 3:
        print(
            "Error: Se requieren 2 argumentos: VIN, Marca. Ejemplo: python partslink.py WVWZZZ1KZ4B024648 'vw' "
        )
        sys.exit(1)
    vin = sys.argv[1]
    marca = sys.argv[2]


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

    #marca = "porsche"
    #pieza = "Cerradura de la puerta"
    #vin = "WP1ZZZ92ZFLA35688"

    if not all([ACCOUNT, USER, PASSWORD, ALL_SERVICES]):
        print(
            "Error: Asegúrate de que 'Account', 'User', 'Password' y 'serviceNamesBMW' están en tu .env"
        )
    else:

        test(vin, marca)
