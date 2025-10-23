import requests
import base64
import time
import os
import re
import json
import sys
from collections import defaultdict
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
from typing import Optional
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
        "datos_url": "https://www.partslink24.com/fiatspa/abarth_parts/directAccess",
    },
    "ALFA": {
        "service_name": "alfa_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/alfa_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/alfa_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/alfa_parts/directAccess",
    },
    "ALPINE": {
        "service_name": "alpine_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin_mdl",
        "producto_url": "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details",
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess",
    },
    "AUDI": {
        "service_name": "audi_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "BENTLEY": {
        "service_name": "bentley_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "BMW": {
        "service_name": "bmw_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "BMWCLASSIC": {
        "service_name": "bmwclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "BMWMOTORRAD": {
        "service_name": "bmwmotorrad_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "BMWMOTORRADCLASSIC": {
        "service_name": "bmwmotorradclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "CITROEN": {
        "service_name": "citroen_parts",
        "consulta_url": "https://www.partslink24.com//psa/citroen_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/psa/citroen_parts/vin-image-board.action",
        "datos_url": "https://www.partslink24.com/psa/citroen_parts/directAccess",
    },
    "CITROENDS": {
        "service_name": "citroenDs_parts",
        "consulta_url": "https://www.partslink24.com/psa/citroenDs_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/psa/citroenDs_parts/scope.action",
        "datos_url": "https://www.partslink24.com/psa/citroenDs_parts/directAccess",
    },
    "CUPRA": {
        "service_name": "cupra_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "DACIA": {
        "service_name": "dacia_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin_mdl",
        "producto_url": "https://www.partslink24.com/p5renault/extern/vehicle/vin_bom_details",
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess",
    },
    "FIAT": {
        "service_name": "fiatp_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/fiatp_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/fiatp_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/fiatp_parts/directAccess",
    },
    "FIATPRO": {
        "service_name": "fiatt_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/fiatt_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/fiatt_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/fiatt_parts/directAccess",
    },
    "FORD": {
        "service_name": "fordp_parts",
        "consulta_url": "https://www.partslink24.com/ford/fordp_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/ford/fordp_parts/json-vin-bom-detail.action?",
        "datos_url": "https://www.partslink24.com/ford/fordp_parts/directAccess",
    },
    "FORDCOM": {
        "service_name": "fordt_parts",
        "consulta_url": "https://www.partslink24.com/ford/fordt_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/ford/fordt_parts/json-vin-bom-detail.action?",
        "datos_url": "https://www.partslink24.com/ford/fordt_parts/directAccess",
    },
    "HYUNDAI": {
        "service_name": "hyundai_parts",
        "consulta_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/main-group.action",
        "datos_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/directAccess",
    },
    "INFINITY": {
        "service_name": "infinity_parts",
        "consulta_url": "https://www.partslink24.com/nissan/infinity_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/nissan/infinity_parts/main-group.action",
        "datos_url": "https://www.partslink24.com/nissan/infinity_parts/directAccess",
    },
    "IVECO": {
        "service_name": "iveco_parts",
        "consulta_url": "https://www.partslink24.com/iveco/iveco_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/iveco/iveco_parts/drawing.action",
        "datos_url": "https://www.partslink24.com/iveco/iveco_parts/directAccess",
    },
    "JAGUAR": {
        "service_name": "jaguar_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess",
    },
    "JEEP": {
        "service_name": "jeep_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/jeep_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/jeep_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/jeep_parts/directAccess",
    },
    "KIA": {
        "service_name": "kia_parts",
        "consulta_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/main-group.action",
        "datos_url": "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/directAccess",
    },
    "LANCIA": {
        "service_name": "lancia_parts",
        "consulta_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/fiatspa/lancia_parts/json-bom.action",
        "datos_url": "https://www.partslink24.com/fiatspa/lancia_parts/directAccess",
    },
    "LANDROVER": {
        "service_name": "landrover_parts",
        "consulta_url": "https://www.partslink24.com/p5jlr/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5jlr/extern/bom/vin_bomdetails",
        "datos_url": "https://www.partslink24.com/p5jlr/extern/directAccess",
    },
    "LEXUS": {
        "service_name": "lexus_parts",
        "consulta_url": "https://www.partslink24.com/p5toyota/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails",
        "datos_url": "https://www.partslink24.com/p5toyota/extern/directAccess",
    },
    "MAN": {
        "service_name": "man_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "MERCEDES": {
        "service_name": "mercedes_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess",
    },
    "MERCEDEST": {
        "service_name": "mercedestrucks_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess",
    },
    "MERCEDESU": {
        "service_name": "mercedesunimog_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess",
    },
    "MERCEDESV": {
        "service_name": "mercedesvans_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess",
    },
    "MINI": {
        "service_name": "mini_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "MINICLASSIC": {
        "service_name": "miniclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5bmw/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5bmw/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5bmw/extern/directAccess",
    },
    "MITSUBISHI": {
        "service_name": "mmc_parts",
        "consulta_url": "https://www.partslink24.com/p5mitsubishi/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5mitsubishi/extern/details/vinDetails",
        "datos_url": "https://www.partslink24.com/p5mitsubishi/extern/directAccess",
    },
    "NISSAN": {
        "service_name": "nissan_parts",
        "consulta_url": "https://www.partslink24.com/nissan/nissan_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/nissan/nissan_parts/main-group.action",
        "datos_url": "https://www.partslink24.com/nissan/nissan_parts/vin-group.action",
    },
    "OPEL": {
        "service_name": "opel_parts",
        "consulta_url": "https://www.partslink24.com/opel/opel_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/opel/opel_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/opel/opel_parts/directAccess",
    },
    "PEUGEOT": {
        "service_name": "peugeot_parts",
        "consulta_url": "https://www.partslink24.com/psa/peugeot_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/psa/peugeot_parts/vin-image-board.action",
        "datos_url": "https://www.partslink24.com/psa/peugeot_parts/directAccess",
    },
    "POLESTAR": {
        "service_name": "polestar_parts",
        "consulta_url": "https://www.partslink24.com/volvo/polestar_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/volvo/polestar_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/volvo/polestar_parts/directAccess",
    },
    "PORSCHE": {
        "service_name": "porsche_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "PORSCHEC": {
        "service_name": "porscheclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "RENAULT": {
        "service_name": "renault_parts",
        "consulta_url": "https://www.partslink24.com/p5renault/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5renault/extern/details/vin/bomDetails",
        "datos_url": "https://www.partslink24.com/p5renault/extern/directAccess",
    },
    "SEAT": {
        "service_name": "seat_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
        "image_url": "https://www.partslink24.com/imageserver/ext/api/images/205837000?",
    },
    "SKODA": {
        "service_name": "skoda_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "SMART": {
        "service_name": "smart_parts",
        "consulta_url": "https://www.partslink24.com/p5daimler/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5daimler/extern/bom/vin/detail",
        "datos_url": "https://www.partslink24.com/p5daimler/extern/directAccess",
    },
    "TOYOTA": {
        "service_name": "toyota_parts",
        "consulta_url": "https://www.partslink24.com/p5toyota/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5toyota/extern/details/vin/bomdetails",
        "datos_url": "https://www.partslink24.com/p5toyota/extern/directAccess",
    },
    "VAUXHALL": {
        "service_name": "vauxhall_parts",
        "consulta_url": "https://www.partslink24.com/opel/vauxhall_parts/json-search.action",
        "producto_url": "https://www.partslink24.com/opel/vauxhall_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/opel/vauxhall_parts/directAccess",
    },
    "VW": {
        "service_name": "vw_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "VMCLASSIC": {
        "service_name": "vmclassic_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "VMCOM": {
        "service_name": "vn_parts",
        "consulta_url": "https://www.partslink24.com/p5vwag/extern/search/vin",
        "producto_url": "https://www.partslink24.com/p5vwag/extern/bom/vin",
        "datos_url": "https://www.partslink24.com/p5vwag/extern/directAccess",
    },
    "VOLVO": {
        "service_name": "volvo_parts",
        "consulta_url": "https://www.partslink24.com/volvo/volvo_parts/json-vin-search.action",
        "producto_url": "https://www.partslink24.com/volvo/volvo_parts/illustration.action",
        "datos_url": "https://www.partslink24.com/volvo/volvo_parts/directAccess",
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
            del self.session.cookies["JSESSIONID"]  # Elimina la cookie específica

            self.access_token = session_state["access_token"]
            print(self.access_token)
            print("")
            print(self.session.cookies.get_dict())

            return True
        except (json.JSONDecodeError, KeyError):
            return False

    def login(self):
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
            print(self.access_token)

            response_auth = self.session.post(
                self.authorize_url,
                json=auth_payload,
            )
            print(response_auth.text)
            response_auth.raise_for_status()
            auth_data = response_auth.json()

            self.access_token = auth_data.get("access_token")
            if not self.access_token:
                return False
            #  print("Autorización exitosa. Token recibido/refrescado.")
            return True
        except requests.RequestException:
            return False

    def buscar_pieza(
        self,
        vin,
        query,
        service_name,
        search_url,
        product_url,
        data_url: Optional[str] = None,
        car: Optional[str] = None,
    ):

        if not self.access_token:
            return None

        # --- Intento 1: Usar la sesión actual ---
        palabra_clave = query.lower().strip()
        response = self._realizar_consulta(vin, query, service_name, search_url)
        print(response.json())
        if response and response.status_code == 200:
            parsed_response = self.procesar_resultados(
                response_data=response.json(),
                service_name=service_name,
                vin=vin,
                product_url=product_url,
                query=palabra_clave,
            )
            # print(parsed_response)
            return parsed_response

        # --- Plan B: Si falla con 401, refrescar token y reintentar ---
        if (
            response is not None
            and response.status_code == 401
            or response.status_code == 402
        ):
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
        if (
            response is not None
            and response.status_code == 401
            or response.status_code == 402
        ):
            # print("Intento 2 fallido (401). Realizando re-login completo (Plan C)...")
            # Usamos la lista completa para el nuevo login
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                # print("Archivo de sesión anterior eliminado para un nuevo login.")

            logged = self.login()
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
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

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        return response_data

    def _realizar_consulta(self, vin, query, service_name, search_url):
        self.vin = vin
        try:
            # self.refresh_access_token(service_name, is_refresh=True)

            headers = self.headers.copy()

            headers["Authorization"] = f"Bearer {self.access_token}"

            params = {
                "lang": "es",
                "serviceName": service_name,
                "vin": vin,
                "q": query,
                # "_": str(int(time.time() * 1000)),
            }
            if service_name == "smart_parts":
                params["cat"] = "60J"
                params["productClassId"] = "F"
                params["scope"] = "F"
                params["subAggregate"] = "n-r"
                params["upds"] = "ND"
            elif service_name == "mercedesvans_parts":
                params["cat"] = "60R"
            elif service_name == "mercedes_parts":
                params["cat"] = "65F"
                params["productClassId"] = "P"
            elif service_name == "nissan_parts":
                # Payload específico para NISSAN hacia json-vin-search.action
                params = {
                    "lang": "es",
                    "upds": "2025.09.03 14:13:16 UTC",
                    "mode": "A0LW0ESES",
                    "page": "0",
                    "textKey": "",
                    "term": query,
                    "vin": vin,
                }

            elif service_name == "citroen_parts":
                # params["mode"] = "A0LW0ESES"
                params["term"] = params.pop("q")
                params["page"] = "0"
            elif service_name == "kia_parts":
                params["term"] = params.pop("q")
            elif service_name == "opel_parts":
                # Configuración específica para OPEL: json-vin-search.action
                params = {
                    "lang": "es",
                    "mode": "A0LW0ESES",
                    "page": "0",
                    "textKey": "",
                    "term": query,
                    "vin": vin,
                }

            response = self.session.get(search_url, headers=headers, params=params)
            print(response.url)
            # print(response.content)

            return response
        except requests.RequestException as e:
            print(f"Error de red durante la consulta: {e}")
            return None

    def get_car_data(self, vin, service_name, search_url):
        header = self.headers.copy()
        header["Authorization"] = f"Bearer {self.access_token}"
        params = {"lang": "es", "q": vin, "serviceName": service_name}

        response = self.session.get(url=search_url, headers=header, params=params)

        return response


class BmwAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("BMW", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        """Método específico para BMW con la consulta adicional a productos."""
        records = response_data.get("data", {}).get("records", [])
        print(records)
        for record in records:
            name = record.get("values", {}).get("name")
            partno = record.get("recordContext", {}).get("bidata_part_no")
            bt_page = record.get("recordContext", {}).get("bidata_bt_page")
            path_info = record.get("p5goto", {}).get("ws", [{}])[0].get("path", "")
            parsed_url = urlparse(path_info)
            query_params = parse_qs(parsed_url.query)
            btnr = query_params.get("btnr", [None])[0]

            # Extraemos el primer id dentro de group_hierarchy (si existe)
            group_hierarchy = record.get("recordContext", {}).get(
                "bidata_group_hierarchy", []
            )
            group_id = group_hierarchy[0].get("id") if group_hierarchy else None

            # Si hay información suficiente, hacemos la segunda consulta
            if partno and name and bt_page and group_id:
                params_producto = {
                    "btnr": btnr,
                    "hg": group_id,
                    "lang": "es",
                    "serviceName": service_name,
                    "vin": vin,
                }

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.session.get(
                    self.producto_url, headers=consulta_headers, params=params_producto
                )

                if consulta_producto.status_code == 200:
                    response_data_product = consulta_producto.json()
                    print(response_data_product)
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
                        # Normalización del nombre usando urllib (como en VW)
                        from urllib.parse import unquote

                        name_normalizado = (
                            unquote(name).replace("\n", " ").replace("\r", " ").strip()
                        )
                        name_normalizado = " ".join(name_normalizado.split())
                        print(
                            f"REF: {ref_normalizado}, NOMBRE: {name_normalizado}, GRUPO: {name_bt_page}"
                        )


# Revisar con mauri
class FordAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info_1 = BRAND_DATA.get("FORD", {})
        self.service_name = brand_info_1.get("service_name")
        self.consulta_url = brand_info_1.get("consulta_url")
        self.producto_url = brand_info_1.get("producto_url")
        self.data_url = brand_info_1.get("datos_url")

        brand_info_2 = BRAND_DATA.get("FORDCOM", {})
        self.service_name_2 = brand_info_2.get("service_name")
        self.consulta_url_2 = brand_info_2.get("consulta_url")
        self.producto_url_2 = brand_info_2.get("producto_url")
        self.data_url_2 = brand_info_2.get("datos_url")

    def buscar_pieza(
        self,
        vin,
        query,
        service_name,
        search_url,
        product_url,
        data_url=None,
        car: Optional[str] = None,
    ):
        response = self._realizar_consulta(
            vin=vin, service_name=service_name, search_url=search_url, query=query
        )

        if response.status_code == 401 or response.status_code == 402:
            self.refresh_access_token(ALL_SERVICES)
            self.save_session_state()

            self.load_session_state()

            response = self._realizar_consulta(
                vin=vin, service_name=service_name, search_url=search_url, query=query
            )

        if response.status_code == 401 or response.status_code == 402:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
                response = self._realizar_consulta(
                    vin=vin,
                    service_name=service_name,
                    search_url=search_url,
                    query=query,
                )
                if response.status_code == 200:

                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, query
                    )
                    return parsed_response
        if response.status_code == 500:
            response = self._realizar_consulta(
                vin=vin,
                query=query,
                service_name=service_name,
                search_url=self.consulta_url_2,
            )
            if response.status_code == 200:
                parsed_response = self.procesar_resultados(
                    response.json(), service_name, vin, product_url, query
                )
                return parsed_response

        parsed_response = parsed_response = self.procesar_resultados(
            response.json(), service_name, vin, product_url, query
        )
        return parsed_response

    def _realizar_consulta(self, vin, query, service_name, search_url):
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"

        payload = {"lang": "es", "page": "0", "term": query, "vin": vin}

        response = self.session.get(url=search_url, headers=headers, params=payload)
        # print(response.json())

        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        items = response_data.get("items", [])
        output = defaultdict(dict)
        for item in items:

            url = item.get("url")

            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            payload = {}

            for p in query_params:
                if p == "upds" or p == "mode":
                    continue
                payload[p] = query_params[p][0]

            response = self.session.get(
                product_url, headers=self.headers, params=payload
            )

            if response.status_code == 500:
                response = self.session.get(
                    self.producto_url_2, headers=self.headers, params=payload
                )
                print(response.url)

            details = response.json().get("details", [])
            for d in details:
                name = d.get("caption", "").lower().strip()
                partno = d.get("partno", "").strip()
                valid = d.get("valid", False)

                output[name][partno] = valid
                print(dict(output))
        return dict(output)


class VwAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("VW", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        """
        Procesa los resultados, valida piezas en sub-consultas y acumula
        todos los resultados válidos en un único diccionario, evitando duplicados.
        """
        productos_data = {}
        registros_vistos = set()

        records = response_data.get("data", {}).get("records", [])

        for indice, record in enumerate(records):
            if indice >= 10:
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
                print(consulta_producto.url)

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
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        demo = response_data.get("demo", False)
        if demo:
            exit

        records = response_data.get("data", {}).get("records", [])
        part_list = []

        for record in records:
            path = record.get("p5goto", {}).get("ws", [])[0].get("path")
            parsed_path = urlparse(path)
            query_params = parse_qs(parsed_path.query)
            payload = {}
            for query in query_params:
                if query == "upds":
                    continue
                payload[query] = query_params[query][0]

            self.headers.update({"Authorization": f"Bearer {self.access_token}"})

            response_parts = self.session.get(
                product_url, headers=self.headers, params=payload
            )

            records_parts = response_parts.json().get("data", {}).get("records", [])

            for part in records_parts:
                values = part.get("values", {})
                partno = values.get("partno")
                name = values.get("description")
                date = values.get("appliFrom")
                note = values.get("appliNote")
                position = values.get("pos")

                part_dict = {
                    "nombre": name,
                    "partno": partno,
                    "fecha": date if date else "N/A",
                    "nota": note if note else "N/A",
                    "posición": position if position else "N/A",
                }

                part_list.append(part_dict)
        print(part_list)
        return {"output": part_list}


# REVISAR CON MAURI
class SmartAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SMART", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        records = response_data.get("data", {}).get("records", [])

        for record in records:

            p5goto = record.get("p5goto", {})
            ws = p5goto.get("ws", [])
            path = ws[0].get("path", "")
            parsed_path = urlparse(path)
            query_params = parse_qs(parsed_path.query)

            bom_id_type = query_params.get("bomIdType")[0]
            main_group = query_params.get("mainGroup")[0]
            sub_group = query_params.get("subGroup")[0]

            params_producto = {
                "bomIdType": bom_id_type,
                "cat": "60J",
                "lang": "es",
                "productClassId": "F",
                "scope": "F",
                "subAggregate": "n-r",
                "upds": "ND",
                "maingroup": main_group,
                "subGroup": sub_group,
                "serviceName": service_name,
                "vin": vin,
                # "_":
            }

            consulta_headers = self.headers.copy()
            consulta_headers.update({"Authorization": f"Bearer {self.access_token}"})

            consulta_producto = self.session.get(
                product_url, headers=consulta_headers, params=params_producto
            )
            print(consulta_producto.url)
            if consulta_producto.status_code == 200:
                response_data_product = consulta_producto.json()
                print(response_data_product)

            elif consulta_producto.status_code == 401:
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
                self.load_session_state()
                consulta_producto = self.session.get(
                    product_url, headers=consulta_headers, params=params_producto
                )

            elif consulta_producto.status_code == 500:
                print(consulta_producto.content)
                return {"error": consulta_producto.content}

            # Si hay información suficiente, hacemos la segunda consulta
            # if partno and name and bt_page and (maingroup or subgroup) and illustration_id:
            #     params_producto = {

            #         "lang": "es",
            #         "maingroup": maingroup,
            #         "subGroup": subgroup,
            #         "serviceName": service_name,
            #         "vin": vin
            #     }

            #     consulta_headers = self.headers.copy()
            #     consulta_headers.update({
            #         "Authorization": f"Bearer {self.access_token}"
            #     })

            #     consulta_producto = self.login_session.get(
            #         product_url, headers=consulta_headers, params=params_producto)

            #     if consulta_producto.status_code == 200:
            #         response_data_product = consulta_producto.json()

            #         # Buscar el nombre del bt_page en los 'crumbs'
            #         crumbs = response_data_product.get("crumbs", [])
            #         name_bt_page = None
            #         for crumb in crumbs:
            #             crumb_name = crumb.get("name", "")
            #             if crumb_name.startswith(bt_page):
            #                 name_bt_page = crumb_name
            #                 break  # Encontramos el nombre y salimos

            #         # Verificar si el partno es válido en la respuesta de productos
            #         valid_partno = None
            #         productos = response_data_product.get(
            #             "data", {}).get("records", [])
            #         for producto in productos:
            #             if producto['id'] != "_null":
            #                 producto_partno = producto['partno']
            #                 unavailable = producto.get("unavailable", False)

            #             if self.normalizar_partno(producto_partno) == self.normalizar_partno(partno) and not unavailable:
            #                 valid_partno = producto_partno
            #                 break  # Encontramos un partno válido

            #         if valid_partno:
            #             print(
            #                 f"REF: {valid_partno}, Nombre: {name}, Grupo: {name_bt_page}")


# 403
class SkodaApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SKODA", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        records = response_data.get("data", {}).get("records", [])
        print(len(records))
        output = defaultdict(dict)

        for record in records:

            path = record.get("p5goto", {}).get("ws", [])[0].get("path")
            parsed_path = urlparse(path)
            query_params = parse_qs(parsed_path.query)

            partno = record.get("recordContext", {}).get("bidata_part_no")
            values = record.get("values", {})
            name = values.get("name")

            payload = {}
            for p in query_params:
                if p == "_" or p == "upds":
                    continue
                payload[p] = query_params[p][0]

            # Si hay información suficiente, hacemos la segunda consulta

            consulta_headers = self.headers.copy()
            consulta_headers.update({"Authorization": f"Bearer {self.access_token}"})

            consulta_producto = self.session.get(
                product_url, headers=consulta_headers, params=payload
            )

            products = consulta_producto.json().get("data", {}).get("records", [])
            # print(len(products))
            for indice, product in enumerate(products):
                if indice >= 20:
                    break
                product_values = product.get("values", {})

                product_partno = (
                    product_values.get("partno", "").strip().replace(" ", "")
                )
                # partno_limpio = product_partno.replace(" ", "")

                product_description = (
                    product_values.get("description").strip().replace("\r\n", " ")
                )
                product_remark = product_values.get("remark", "").strip()

                # characteristic = product.get("characteristic")
                unavailable = product.get("unavailable")
                if unavailable or not product_partno:
                    continue
                output[product_description][product_remark] = product_partno
                print(dict(output))

        return dict(output)


# Url de OPEL esta mal, revisar
class OpelApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("OPEL", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")
        self.cat_id = None

    def extraer_cat_id(self, vin: str):
        """
        Extrae el catId dinámicamente siguiendo las redirecciones de OPEL
        """
        try:
            # URL inicial para obtener el catId
            initial_url = f"https://www.partslink24.com/opel/opel_parts/vin.action?mode=A0LW0ESES&lang=es&vin={vin}&startup=true"
            
            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            # Realizar la petición permitiendo redirecciones
            response = self.session.get(initial_url, headers=headers, allow_redirects=True)
            
            # Método 1: Extraer catId de la URL final
            final_url = response.url
            parsed_url = urlparse(final_url)
            params = parse_qs(parsed_url.query)
            
            if 'catId' in params:
                cat_id = params['catId'][0]
                print(f"catId extraído de URL: {cat_id}")
                self.cat_id = cat_id
                return cat_id
            
            # Método 2: Buscar en el historial de redirecciones
            for resp in response.history:
                if 'Location' in resp.headers:
                    location_url = resp.headers['Location']
                    parsed_location = urlparse(location_url)
                    location_params = parse_qs(parsed_location.query)
                    
                    if 'catId' in location_params:
                        cat_id = location_params['catId'][0]
                        self.cat_id = cat_id
                        return cat_id
            
            # Método 3: Buscar en headers de respuesta personalizados
            for header_name, header_value in response.headers.items():
                if 'catid' in header_name.lower() or 'cat-id' in header_name.lower():
                    print(f"catId encontrado en header {header_name}: {header_value}")
                    self.cat_id = header_value
                    return header_value
            
            # Método 4: Buscar en el contenido HTML si es necesario
            if 'text/html' in response.headers.get('Content-Type', ''):
                from urllib.parse import unquote
                content = response.text
                # Buscar patrones como catId=1 en el HTML
                import re
                cat_id_match = re.search(r'catId[=:](\d+)', content)
                if cat_id_match:
                    cat_id = cat_id_match.group(1)
                    print(f"catId extraído del HTML: {cat_id}")
                    self.cat_id = cat_id
                    return cat_id
            
            print("No se pudo extraer el catId")
            return None
            
        except Exception as e:
            print(f"Error al extraer catId: {e}")
            return None

    def obtener_cat_id(self, vin: Optional[str] = None) -> Optional[str]:
        """
        Método público para obtener el catId.
        
        Args:
            vin: VIN del vehículo (opcional si ya se tiene cat_id)
            
        Returns:
            str: El catId extraído o None si no se pudo obtener
        """
        # Si ya tenemos cat_id, lo devolvemos
        if hasattr(self, 'cat_id') and self.cat_id:
            return self.cat_id
            
        # Si no tenemos cat_id pero tenemos VIN, intentamos extraerlo
        if vin:
            return self.extraer_cat_id(vin)
            
        print("No se puede obtener catId: no hay cat_id existente ni VIN proporcionado")
        return None

    def buscar_pieza(
        self,
        vin: str,
        term: str,
        service_name: str,
        search_url: Optional[str] = None,
        product_url: Optional[str] = None,
        data_url: Optional[str] = None,
        page: Optional[str] = None,
        car: Optional[str] = None,
    ):
        # Extraer catId dinámicamente si no lo tenemos
        if not hasattr(self, 'cat_id') or not self.cat_id:
            cat_id = self.extraer_cat_id(vin)
            if not cat_id:
                # print("Error: No se pudo obtener el catId necesario para OPEL")
                return None
            self.cat_id = cat_id
        
        params = {
            "lang": "es",
            "page": page if page else "0",
            "term": term,
            "vin": vin,
        }
        
        # Agregar catId a los parámetros si está disponible
        if hasattr(self, 'cat_id') and self.cat_id:
            params["catId"] = self.cat_id

        headers = self.headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        palabra_clave = term.lower().strip()
        response = self.session.get(
            url=search_url or self.consulta_url,
            headers=headers,
            params=params,
        )
        # print(response.url)

        # OK + JSON
        if response.status_code == 200 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            parsed_response = self.procesar_resultados(
                response.json(),
                service_name,
                vin,
                product_url or self.producto_url,
                palabra_clave,
            )
            return parsed_response

        # 401/402 → Refresh → Retry
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            refrescar = self.refresh_access_token([service_name], is_refresh=True)
            if refrescar:
                self.save_session_state()
                self.load_session_state()
                headers = self.headers.copy()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url or self.consulta_url,
                    headers=headers,
                    params=params,
                )
                if (
                    response.status_code == 200
                    and "application/json" in response.headers.get("Content-Type", "")
                ):
                    return self.procesar_resultados(
                        response.json(),
                        service_name,
                        vin,
                        product_url or self.producto_url,
                        palabra_clave,
                    )

        # Re-login completo si sigue fallando
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                ok = self.refresh_access_token([service_name], is_refresh=False)
                if ok:
                    self.save_session_state()
                    self.load_session_state()
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(
                        url=search_url or self.consulta_url,
                        headers=headers,
                        params=params,
                    )
                    if (
                        response.status_code == 200
                        and "application/json"
                        in response.headers.get("Content-Type", "")
                    ):
                        return self.procesar_resultados(
                            response.json(),
                            service_name,
                            vin,
                            product_url or self.producto_url,
                            palabra_clave,
                        )

        if response is not None and response.status_code == 402:
            print(
                "Suscripción requerida para Opel. Verifica permisos de 'opel_parts' en tu cuenta."
            )
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        # Estructura tipo Nissan/Opel: items[]
        items = response_data.get("items", [])
        if not items:
            # print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
            return []

        results = []
        for item in items[:50]:
            item_url = item.get("url", "")
            # Construye URL absoluta para extraer parámetros
            full_url = "https://www.partslink24.com/opel/opel_parts/" + item_url
            parsed = urlparse(full_url)
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            # Intento de detalles del producto; algunos endpoints pueden responder HTML
            try:
                detail_resp = self.session.get(
                    product_url, headers=headers, params=params
                )
                details = (
                    detail_resp.json()
                    if detail_resp.status_code == 200
                    and "application/json"
                    in detail_resp.headers.get("Content-Type", "")
                    else None
                )
            except Exception:
                details = None

            results.append(
                {
                    "caption": item.get("caption"),
                    "partno": item.get("gmPartNo"),
                    "url": item_url,
                    "details": details,
                }
            )

        # Formateo en tabla legible
        def trunc(s, n):
            s = s or ""
            return (s[: n - 1] + "…") if len(s) > n else s

        # print("\n" + "=" * 100)
        # print(f"RESULTADOS OPEL — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)")
        # print("=" * 100)
        # header = f"{'PARTNO':<18} {'DESCRIPCIÓN':<40} {'URL':<25}"
        # print(header)
        # print("-" * 100)
        # for r in results:
        #     print(
        #         f"{trunc(r.get('partno',''),18):<18} "
        #         f"{trunc(r.get('caption',''),40):<40} "
        #         f"{trunc(r.get('url',''),25):<25}"
        #     )
        # print("=" * 100)

        return results

    def consultar_imagen_pieza_desde_url(self, item_url, base_url="https://www.partslink24.com", max_parts=None):
        """
        Consulta la URL de imagen de una pieza directamente desde la URL proporcionada en el item.
        Específico para OPEL.
        
        Args:
            item_url: URL del item (campo 'url' del resultado de búsqueda)
            base_url: URL base del servicio
            max_parts: Número máximo de piezas válidas a extraer (None = sin límite)
            
        Returns:
            dict: Información detallada de la pieza incluyendo diagramas e ilustraciones
        """
        try:
            # Construir URL completa para OPEL
            if item_url.startswith('vin-image-board.action') or not item_url.startswith('http'):
                url = f"{base_url}/opel/opel_parts/{item_url.lstrip('/')}"
            else:
                url = item_url
            
            # print(f"🔍 Consultando URL de imagen OPEL...")
            # print(f"📍 URL: {url}")
            
            # Realizar la petición con autenticación
            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"
            
            response = self.session.get(url, headers=headers, timeout=30)
            
            # Manejar códigos de estado de autenticación
            if response.status_code in [401, 402]:
                # print("🔄 Token expirado, intentando refrescar...")
                if self.refresh_access_token(self.service_name, is_refresh=True):
                    self.save_session_state()
                    self.load_session_state()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(url, headers=headers, timeout=30)
                else:
                    # print("🔄 Refresh falló, intentando re-login completo...")
                    if self.login():
                        self.refresh_access_token(self.service_name, is_refresh=False)
                        self.save_session_state()
                        headers["Authorization"] = f"Bearer {self.access_token}"
                        response = self.session.get(url, headers=headers, timeout=30)
                    else:
                        return {
                            "status": "error",
                            "message": "No se pudo autenticar después de varios intentos"
                        }
            
            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Error HTTP {response.status_code}: {response.reason}",
                    "url": url
                }
            
            content_type = response.headers.get('Content-Type', '').lower()
            
            # Para OPEL siempre esperamos HTML, no JSON
            if 'text/html' in content_type:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Buscar la tabla específica de OPEL: class="tc-table" id="nav-bomDetails-table"
                    target_table = soup.find('table', {'class': 'tc-table', 'id': 'nav-bomDetails-table'})
                    
                    if target_table:
                        valid_parts = []
                        
                        # Buscar todas las filas tr con clase "tc-row tc-data-row"
                        rows = target_table.find_all('tr', class_=re.compile(r'tc-row tc-data-row'))
                        
                        for row in rows:
                            # Si ya alcanzamos el límite máximo, salir del bucle
                            if max_parts is not None and len(valid_parts) >= max_parts:
                                break
                                
                            # Verificar que tenga valid="true"
                            valid_attr = row.get('valid', '').lower()
                            if valid_attr == 'true':
                                # Extraer gmNo
                                gm_no = row.get('gmno', '').strip()
                                
                                # Solo procesar si tiene gmNo y no está vacío
                                if gm_no and gm_no != ' ':
                                    # Extraer gmOpelNo
                                    gm_opel_no = row.get('gmopelno', '').strip()
                                    
                                    # Extraer caption
                                    caption = row.get('caption', '').strip()
                                    
                                    # Agregar a la lista en el orden solicitado: gmNo, gmOpelNo, caption
                                    valid_parts.append({
                                        'gmNo': gm_no,
                                        'gmOpelNo': gm_opel_no,
                                        'caption': caption
                                    })
                        
                        # Si hay piezas válidas, retornar directamente la lista
                        if valid_parts:
                            return valid_parts
                        else:
                            # Si no hay piezas válidas, retornar lista vacía
                            return []
                    else:
                        # Si no se encuentra la tabla, retornar lista vacía
                        return []
                    
                except Exception as e:
                    return {
                        "status": "error",
                        "message": f"Error al procesar HTML: {e}",
                        "url": url
                    }
            
            else:
                return {
                    "status": "error",
                    "message": f"Tipo de contenido no soportado: {content_type}",
                    "url": url
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en la consulta: {e}",
                "url": item_url
            }

    def buscar_y_consultar_imagenes(self, vin: str, term: str, aplicar_filtro: bool = True):
        """
        Busca piezas y consulta información de imagen para cada resultado.
        Combina resultados de búsqueda JSON y extracción HTML eliminando duplicados por gmNo.
        
        Args:
            vin: VIN del vehículo
            term: Término de búsqueda
            max_resultados: Número máximo de resultados a procesar
            
        Returns:
            Lista de resultados combinados sin duplicados por gmNo
        """
        try:
            # print(f"🔍 Iniciando búsqueda combinada para VIN: {vin}, término: '{term}'")
            
            # 1. OBTENER RESULTADOS DE BÚSQUEDA JSON (método buscar_pieza)
            # print("\n📋 Fase 1: Obteniendo resultados de búsqueda JSON...")
            resultados_busqueda = self.buscar_pieza(
                vin=vin,
                term=term,
                service_name=self.service_name
            )
            
            resultados_json = []
            if resultados_busqueda and isinstance(resultados_busqueda, list):
                # print(f"✅ Encontrados {len(resultados_busqueda)} resultados en búsqueda JSON")
                resultados_json = resultados_busqueda
            else:
                # print("⚠️ No se obtuvieron resultados de búsqueda JSON")
                pass
            
            # 2. OBTENER RESULTADOS DE EXTRACCIÓN HTML
            # print("\n🌐 Fase 2: Obteniendo resultados de extracción HTML...")
            resultados_html = []
            
            # Procesar cada resultado JSON para obtener información HTML
            for i, resultado in enumerate(resultados_json):
                item_url = resultado.get("url")
                if item_url:
                    # print(f"🔍 Extrayendo HTML del resultado {i+1}/{len(resultados_json)}")
                    piezas_html = self.consultar_imagen_pieza_desde_url(item_url)
                    
                    # Ahora piezas_html es directamente una lista de piezas válidas
                    if isinstance(piezas_html, list) and len(piezas_html) > 0:
                        resultados_html.append(piezas_html)
                    
                    time.sleep(0.1)  # Pausa para no sobrecargar el servidor
            
            # print(f"✅ Procesados {len(resultados_html)} resultados HTML")
            
            # 3. COMBINAR Y ELIMINAR DUPLICADOS POR gmNo
            # print("\n🔄 Fase 3: Combinando resultados y eliminando duplicados...")
            
            piezas_unicas = {}  # Diccionario para eliminar duplicados por gmNo
            estadisticas = {
                "total_json": len(resultados_json),
                "total_html": len(resultados_html),
                "piezas_html_extraidas": 0,
                "duplicados_eliminados": 0,
                "piezas_finales": 0
            }
            
            # Procesar resultados HTML y extraer piezas válidas
            for i, resultado_html in enumerate(resultados_html):
                # Ahora resultado_html es directamente una lista de piezas válidas
                if isinstance(resultado_html, list):
                    valid_parts = resultado_html
                    json_source = resultados_json[i] if i < len(resultados_json) else {}
                else:
                    # Compatibilidad con formato anterior (por si acaso)
                    valid_parts = resultado_html if isinstance(resultado_html, list) else []
                    json_source = {}
                
                estadisticas["piezas_html_extraidas"] += len(valid_parts)
                
                for pieza in valid_parts:
                    gm_no = pieza.get("gmNo", "").strip()
                    
                    if gm_no and gm_no != " ":
                        if gm_no in piezas_unicas:
                            # Duplicado encontrado - mantener el que tenga más información
                            estadisticas["duplicados_eliminados"] += 1
                            existing = piezas_unicas[gm_no]
                            
                            # Combinar información si es necesario
                            if not existing.get("json_source") and json_source:
                                existing["json_source"] = {
                                    "partno": json_source.get("partno"),
                                    "description": json_source.get("caption"),
                                    "url_original": json_source.get("url"),
                                    "details": json_source.get("details")
                                }
                        else:
                            # Nueva pieza única
                            pieza_completa = {
                                "gmNo": gm_no,
                                "gmOpelNo": pieza.get("gmOpelNo", ""),
                                "caption": pieza.get("caption", ""),
                                "source": "html_extraction",
                                "json_source": {
                                    "partno": json_source.get("partno"),
                                    "description": json_source.get("caption"),
                                    "url_original": json_source.get("url"),
                                    "details": json_source.get("details")
                                } if json_source else None,
                                "url_original": json_source.get("url", "") if json_source else ""
                            }
                            piezas_unicas[gm_no] = pieza_completa
            
            # Convertir diccionario a lista ordenada
            resultados_finales = list(piezas_unicas.values())
            estadisticas["piezas_antes_filtro"] = len(resultados_finales)
            
            # 3.5. FILTRAR POR RELEVANCIA CON EL TÉRMINO DE BÚSQUEDA (MEJORADO)
            if aplicar_filtro:
                def es_relevante(pieza, termino_busqueda):
                    """Verifica si una pieza es relevante al término de búsqueda con coincidencias flexibles"""
                    termino_original = termino_busqueda.strip()
                    termino_lower = termino_original.lower()
                    
                    if not termino_lower:
                        return True
                    
                    # Obtener campos específicos normalizados
                    caption = pieza.get('caption', '').lower().strip()
                    description = pieza.get('description', '').lower().strip()
                    gm_no = pieza.get('gmNo', '').lower().strip()
                    gm_opel_no = pieza.get('gmOpelNo', '').lower().strip()
                    
                    # Obtener descripción del JSON source si existe
                    json_desc = ""
                    if pieza.get('json_source') and pieza['json_source']:
                        json_desc = pieza['json_source'].get('description', '').lower().strip()
                    
                    # CRITERIO 1: Coincidencia exacta del término completo en caption (prioridad máxima)
                    if termino_lower in caption:
                        return True
                    
                    # CRITERIO 2: Coincidencia exacta del término completo en description
                    if termino_lower in description:
                        return True
                    
                    # CRITERIO 3: Coincidencia exacta del término completo en json_desc
                    if json_desc and termino_lower in json_desc:
                        return True
                    
                    # CRITERIO 4: Coincidencias parciales flexibles (para términos como "filtros")
                    # Dividir el término en palabras para búsqueda más granular
                    palabras_busqueda = [palabra.strip() for palabra in termino_lower.split() if palabra.strip() and len(palabra.strip()) >= 3]
                    
                    if palabras_busqueda:
                        # Buscar cada palabra en caption (más flexible)
                        for palabra in palabras_busqueda:
                            if palabra in caption:
                                return True
                        
                        # Buscar cada palabra en description (con mayor longitud mínima)
                        for palabra in palabras_busqueda:
                            if len(palabra) >= 4 and palabra in description:
                                return True
                        
                        # Buscar cada palabra en json_desc
                        if json_desc:
                            for palabra in palabras_busqueda:
                                if len(palabra) >= 4 and palabra in json_desc:
                                    return True
                    
                    # CRITERIO 5: Coincidencias en números de parte (muy específicas)
                    if len(termino_lower) >= 4:
                        if termino_lower in gm_no or termino_lower in gm_opel_no:
                            return True
                    
                    return False
                
                # Aplicar filtro de relevancia
                resultados_filtrados = [pieza for pieza in resultados_finales if es_relevante(pieza, term)]
                estadisticas["piezas_filtradas"] = len(resultados_filtrados)
                estadisticas["piezas_descartadas_por_filtro"] = len(resultados_finales) - len(resultados_filtrados)
                
                resultados_finales = resultados_filtrados
                estadisticas["piezas_finales"] = len(resultados_finales)
            else:
                # Si no se aplica filtro, mantener todas las piezas
                estadisticas["piezas_filtradas"] = len(resultados_finales)
                estadisticas["piezas_descartadas_por_filtro"] = 0
                estadisticas["piezas_finales"] = len(resultados_finales)
            
            # 4. MOSTRAR ESTADÍSTICAS Y RESULTADOS
            # print(f"\n📊 ESTADÍSTICAS DE COMBINACIÓN:")
            # print(f"   • Resultados JSON iniciales: {estadisticas['total_json']}")
            # print(f"   • Páginas HTML procesadas: {estadisticas['total_html']}")
            # print(f"   • Piezas extraídas de HTML: {estadisticas['piezas_html_extraidas']}")
            # print(f"   • Duplicados eliminados: {estadisticas['duplicados_eliminados']}")
            # print(f"   • Piezas antes del filtro: {estadisticas['piezas_antes_filtro']}")
            # if aplicar_filtro:
            #     print(f"   • Filtro de relevancia: ACTIVADO")
            #     print(f"   • Piezas descartadas por filtro: {estadisticas['piezas_descartadas_por_filtro']}")
            # else:
            #     print(f"   • Filtro de relevancia: DESACTIVADO")
            # print(f"   • Piezas únicas finales: {estadisticas['piezas_finales']}")
            
            # if resultados_finales:
            #     print(f"\n✅ PIEZAS ÚNICAS ENCONTRADAS:")
            #     for i, pieza in enumerate(resultados_finales, 1):  # Mostrar todos
            #         print(f"   {i}. gmNo: {pieza['gmNo']} | gmOpelNo: {pieza['gmOpelNo']} | {pieza['caption'][:50]}...")
            
            return {
                "piezas_unicas": resultados_finales,
                "estadisticas": estadisticas,
                "resultados_json_originales": resultados_json,
                "total_piezas": len(resultados_finales)
            }
            
        except Exception as e:
            print(f"❌ Error en buscar_y_consultar_imagenes: {e}")
            return {
                "piezas_unicas": [],
                "estadisticas": {"error": str(e)},
                "resultados_json_originales": [],
                "total_piezas": 0
            }


# acesso prohibido
class MitsubishiApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("MITSUBISHI", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.datos_url = brand_info.get("datos_url")

    def obtener_datos_coche(self, vin, service_name, search_url):
        """
        Obtiene todos los datos del coche desde PartsLink24 usando el VIN.
        """
        if not self.access_token:
            return None
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"
        payload = {"lang": "es", "serviceName": service_name, "q": vin}

        response = self.session.get(search_url, headers=headers, params=payload)
        path_info = response.json().get("data", {}).get("link", {}).get("path")

        parsed_url = urlparse(path_info)
        query_params = parse_qs(parsed_url.query)
        id_car = query_params["vehicle"]
        model_id = query_params["modelId"]

        return {"modelId": model_id, "vehicle": id_car}

        # # --- Plan B: Si falla con 401, refrescar token y reintentar ---
        # if response is not None and response.status_code == 401:
        #     refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
        #     if refrescar_token:
        #         self.save_session_state()
        #         self.load_session_state()
        #         response = self._realizar_consulta_custom(search_url, vin, service_name)
        #         if response and response.status_code == 200:
        #             return response.json()
        #
        # # --- Plan C: Si vuelve a fallar, hacer re-login completo y reintentar ---
        # if response is not None and response.status_code == 401:
        #     if os.path.exists(self.session_file):
        #         os.remove(self.session_file)
        #     logged = self.login(ALL_SERVICES)
        #     if logged:
        #         self.save_session_state()
        #         self.load_session_state()
        #         self.refresh_access_token(ALL_SERVICES, is_refresh=True)
        #         response = self._realizar_consulta_custom(search_url, vin, service_name)
        #         if response and response.status_code == 200:
        #             return response.json()
        # elif response is not None and response.status_code == 500:
        #     return {"error": "Error interno del servidor (500)."}
        #
        # # Si llegamos aquí, todos los intentos fallaron.
        # print("Error crítico: La consulta falló después de todos los intentos de recuperación.")
        # return None

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        print(response_data)
        demo = response_data.get("demo")
        if demo:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)

            logged = self.login(ALL_SERVICES)
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)

                response = self._realizar_consulta(
                    vin, query, service_name, self.consulta_url
                )
                response_data = response.json()

                car_data = self.obtener_datos_coche(vin, service_name, self.datos_url)
                print(response.json())

        records = response_data.json().get("data", {}).get("records", [])

        for record in records:
            path_info = record.get("p5goto", {}).get("ws", [])[0].get("path")
            parsed_url = urlparse(path_info)
            query_params = parse_qs(parsed_url.query)
            bomDetails = query_params.get("bomDetails", [None])[0]
            maingroup = query_params.get("mainGroup", [None])[0]
            subgroup = query_params.get("subGroup", [None])[0]
            upds = query_params.get("upds", [None])[0]
            modelId = query_params.get("modelId", [None])[0]

            params_producto = {
                "bomDetails": bomDetails,
                "lang": "es",
                "maingroup": maingroup,
                "modelId": "D32A",
                "serviceName": service_name,
                "subgroup": subgroup,
                "upds": upds,
                # "vehicle": "C608M409D",
                "vin": vin,
                # "_": str(int(time.time() * 1000)),  # Timestamp dinámico
            }
            consulta_headers = self.headers.copy()
            consulta_headers.update({"Authorization": f"Bearer {self.access_token}"})
            consulta_producto = self.session.get(
                product_url, headers=consulta_headers, params=params_producto
            )
            print(consulta_producto.url)
            print(query_params)

        return None


# Error 402
class NissanApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("NISSAN", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    # TERMINAR ESTA FUCION  Y EVALUAR LA POSIBILIDAD PARA AGREGAR UN NUEVO METODO QUE AGREGUE LOS PARAMS EXTRAS PARA EL RESTO DE CLASES
    def buscar_pieza(
        self,
        vin: str,
        term: str,
        service_name: str,
        search_url: Optional[str] = None,
        product_url: Optional[str] = None,
        data_url: Optional[str] = None,
        page: Optional[str] = None,
        car: Optional[str] = None,
    ):
        params = {
            "lang": "es",
            "serviceName": service_name,
            "vin": vin,
            "term": term,
            "page": page if page else "0",
        }

        headers = self.headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        palabra_clave = term.lower().strip()
        response = self.session.get(
            url=search_url or self.consulta_url,
            headers=headers,
            params=params,
        )

        # OK + JSON
        if response.status_code == 200 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            parsed_response = self.procesar_resultados(
                response.json(),
                service_name,
                vin,
                product_url or self.producto_url,
                palabra_clave,
            )
            return parsed_response

        # 401/402 → Refresh → Retry
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            refrescar = self.refresh_access_token([service_name], is_refresh=True)
            if refrescar:
                self.save_session_state()
                self.load_session_state()
                headers = self.headers.copy()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url or self.consulta_url,
                    headers=headers,
                    params=params,
                )
                if (
                    response.status_code == 200
                    and "application/json" in response.headers.get("Content-Type", "")
                ):
                    return self.procesar_resultados(
                        response.json(),
                        service_name,
                        vin,
                        product_url or self.producto_url,
                        palabra_clave,
                    )

        # Re-login completo si sigue fallando
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                ok = self.refresh_access_token([service_name], is_refresh=False)
                if ok:
                    self.save_session_state()
                    self.load_session_state()
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(
                        url=search_url or self.consulta_url,
                        headers=headers,
                        params=params,
                    )
                    if (
                        response.status_code == 200
                        and "application/json"
                        in response.headers.get("Content-Type", "")
                    ):
                        return self.procesar_resultados(
                            response.json(),
                            service_name,
                            vin,
                            product_url or self.producto_url,
                            palabra_clave,
                        )

        if response is not None and response.status_code == 402:
            print(
                "Suscripción requerida para Nissan. Verifica permisos de 'nissan_parts' en tu cuenta."
            )
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        items = response_data.get("items", [])
        if not items:
            print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
            return []

        results = []
        for item in items[:50]:
            item_url = item.get("url", "")
            full_url = "https://www.partslink24.com/nissan/nissan_parts/" + item_url
            parsed = urlparse(full_url)
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            try:
                detail_resp = self.session.get(
                    product_url, headers=headers, params=params
                )
                details = (
                    detail_resp.json()
                    if detail_resp.status_code == 200
                    and "application/json"
                    in detail_resp.headers.get("Content-Type", "")
                    else None
                )
            except Exception:
                details = None

            results.append(
                {
                    "caption": item.get("caption"),
                    "partno": item.get("partno"),
                    "pnc": item.get("pnc"),
                    "url": item_url,
                    "details": details,
                }
            )

        # Formateo en tabla legible
        def trunc(s, n):
            s = s or ""
            return (s[: n - 1] + "…") if len(s) > n else s

        print("\n" + "=" * 100)
        print(
            f"RESULTADOS NISSAN — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)"
        )
        print("=" * 100)
        header = f"{'PARTNO':<18} {'PNC':<12} {'DESCRIPCIÓN':<40} {'URL':<25}"
        print(header)
        print("-" * 100)
        for r in results:
            print(
                f"{trunc(r.get('partno',''),18):<18} "
                f"{trunc(r.get('pnc',''),12):<12} "
                f"{trunc(r.get('caption',''),40):<40} "
                f"{trunc(r.get('url',''),25):<25}"
            )
        print("=" * 100)

        return results


class MercedesApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("MERCEDES", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def _realizar_consulta(self, response_data, vin, service_name, search_url, query):

        try:

            vehicle_context = response_data.get("vehicleContext", {})
            cat = vehicle_context.get("cat")
            product_class_id = vehicle_context.get("productClassId")

            payload = {
                "cat": cat,
                "lang": "es",
                "productClassId": product_class_id,
                "serviceName": service_name,
                "vin": vin,
                "q": query,
            }

            headers = self.headers.copy()

            headers["Authorization"] = f"Bearer {self.access_token}"

            response = self.session.get(search_url, headers=headers, params=payload)

            return response.json()
        except requests.RequestException as e:
            print(f"Error de red durante la consulta: {e}")
            return None

    def buscar_pieza(
        self,
        vin,
        query,
        service_name,
        search_url,
        product_url,
        data_url: Optional[any] = None,
        car: Optional[str] = None,
    ):

        if not self.access_token:
            return None

        data_car = self.get_car_data(
            vin=vin, service_name=service_name, search_url=data_url
        )

        if data_car.status_code == 200:

            response = self._realizar_consulta(
                response_data=data_car.json(),
                vin=vin,
                service_name=service_name,
                search_url=search_url,
                query=query,
            )
            parsed_response = self.procesar_resultados(
                response, service_name, vin, product_url, query
            )
            return parsed_response

        if data_car.status_code == 401:
            refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                data_car = self.get_car_data(
                    vin=vin, service_name=service_name, search_url=data_url
                )
            if data_car.status_code == 200:
                response = self._realizar_consulta(
                    response_data=data_car.json(),
                    vin=vin,
                    service_name=service_name,
                    search_url=search_url,
                    query=query,
                )
                parsed_response = self.procesar_resultados(
                    response, service_name, vin, product_url, query
                )
                return parsed_response

        if data_car.status_code == 401:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
                data_car = self.get_car_data(
                    vin=vin, service_name=service_name, search_url=data_url
                )
                if data_car.status_code == 200:

                    response = self._realizar_consulta(
                        response_data=data_car.json(),
                        vin=vin,
                        service_name=service_name,
                        search_url=search_url,
                        query=query,
                    )
                    parsed_response = self.procesar_resultados(
                        response, service_name, vin, product_url, query
                    )
                    return parsed_response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        output = defaultdict(dict)
        print(response_data)
        records = response_data.get("data", {}).get("records", [])
        for record in records:
            path = record.get("p5goto", {}).get("ws", [])[0].get("path")
            parsed_path = urlparse(path)
            query_params = parse_qs(parsed_path.query)
            payload = {}
            for p in query_params:
                if p == "_" or p == "upds":
                    continue
                payload[p] = query_params[p][0]

            headers = self.headers.copy()
            headers.update({"Authorization": f"Bearer {self.access_token}"})
            response_part = self.session.get(
                url=product_url, headers=headers, params=payload
            )

            response_part_json = response_part.json()
            parts_records = response_part_json.get("data", {}).get("records", [])
            for indice, part in enumerate(parts_records):
                if indice >= 15:
                    break

                restriction = part.get("values", {}).get("restrictions")

                # if restriction:
                #     continue
                partno = part.get("partno")
                description = part.get("description")
                remark = part.get("values", {}).get("remark")
                position = part.get("pos")

                output[description][remark] = partno
                print(dict(output))
        return dict(output)


# 403
class RenaultApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("RENAULT", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def buscar_pieza(
        self,
        vin,
        query,
        service_name,
        search_url,
        product_url,
        data_url,
        car: Optional[str] = None,
    ):

        data_car = self.get_car_data(
            vin=vin, service_name=service_name, search_url=data_url
        )

        if data_car and data_car.status_code == 200:
            print(data_car.json())

            data_car_parsed = self.procesar_datos_coche(data_car.json())

        if data_car.status_code == 401:
            refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                data_car = self.get_car_data(
                    vin=vin, service_name=service_name, search_url=data_url
                )
                if data_car and data_car.status_code == 200:

                    data_car_parsed = self.procesar_datos_coche(data_car.json())

        if data_car.status_code == 401:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
                self.load_session_state()
                data_car = self.get_car_data(
                    vin=vin, service_name=service_name, search_url=data_url
                )
                if data_car and data_car.status_code == 200:
                    data_car_parsed = self.procesar_datos_coche(data_car.json())
                    print(data_car_parsed)

        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"

        params = {
            "catalog": data_car_parsed.get("catalog"),
            "engineFamily": data_car_parsed.get("engine_family"),
            "engineIndex": data_car_parsed.get("engine_index"),
            "engineLevel": data_car_parsed.get("engine_level"),
            "engineType": data_car_parsed.get("engine_type"),
            "gearboxFamily": data_car_parsed.get("gear_box_family"),
            "gearboxIndex": data_car_parsed.get("gear_box_index"),
            "gearboxType": data_car_parsed.get("gear_box_type"),
            "lang": "es",
            "model": data_car_parsed.get("model"),
            "serviceName": service_name,
            "vin": vin,
            "q": query,
        }

        response = self.session.get(url=search_url, headers=headers, params=params)

        parsed_response = self.procesar_resultados(
            response_data=response.json(),
            service_name=service_name,
            vin=vin,
            product_url=product_url,
        )
        # print(parsed_response)
        return parsed_response

    def procesar_datos_coche(self, response):
        print(response)
        path = response.get("data", {}).get("link", {}).get("path")

        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)
        catalog = query_params.get("catalog")[0]
        engine_family = query_params.get("engineFamily")[0]
        engine_index = query_params.get("engineIndex")[0]
        engine_level = query_params.get("engineLevel")[0]
        engine_type = query_params.get("engineType")[0]
        gear_box_family = query_params.get("gearboxFamily")[0]
        gear_box_index = query_params.get("gearboxIndex")[0]
        gear_box_type = query_params.get("gearboxType")[0]
        model = query_params.get("model")[0]
        return {
            "catalog": catalog,
            "engine_family": engine_family,
            "engine_index": engine_index,
            "engine_level": engine_level,
            "engine_type": engine_type,
            "gear_box_family": gear_box_family,
            "gear_box_index": gear_box_index,
            "gear_box_type": gear_box_type,
            "model": model,
        }

    def procesar_resultados(self, response_data, service_name, vin, product_url):
        numero_partes = defaultdict(list)
        records = response_data.get("data", {}).get("records", [])
        for indice, record in enumerate(records):
            if indice >= 10:
                break
            path = record.get("p5goto", {}).get("ws", [])[0].get("path")
            parsed_url = urlparse(path)
            query_params = parse_qs(parsed_url.query)
            payload = {}
            for p in query_params:
                if p == "_" or p == "upds":
                    continue
                payload[p] = query_params[p][0]

            headers = self.headers.copy()
            headers["Authorization"] = f"Bearer {self.access_token}"

            response_parts = self.session.get(
                url=product_url, headers=headers, params=payload
            )
            products = response_parts.json().get("data", {}).get("records", [])
            print(products)
            for product in products:
                unavailable = product.get("unavailable", False)
                if unavailable:
                    continue
                values = product.get("values", {})
                partno = values.get("partno")
                name = values.get("description", "N/A").lower().strip()

                if partno not in numero_partes[name]:
                    numero_partes[name].append(partno.strip())

                # print("-" * 20)
                # print(numero_partes)

            # print(response_parts.json())
            # print(payload)

        # print(numero_partes)
        print("diccionario\n")
        # time.sleep(10)
        print(dict(numero_partes))

        return dict(numero_partes)


class SeatApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("SEAT", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")
        self.image_url = brand_info.get("image_url")

    def get_image(self, image_url: str, query: str):

        parsed_url = urlparse(image_url)
        query_params = parse_qs(parsed_url.query)

        payload = {}

        for p in query_params:
            if p == "_" or p == "upds":
                continue
            payload[p] = query_params[p][0]

        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"

        response = self.session.get(url=self.image_url, headers=headers, params=payload)

        image = response.json().get("image")
        image_data = base64.b64decode(image)
        file_name = f"{query.replace(' ','_')}.png"
        with open(file_name, "wb") as img_file:
            img_file.write(image_data)

        print(image)
        return image

    def get_car_data(self, vin, service_name, search_url, car):
        header = self.headers.copy()
        header["Authorization"] = f"Bearer {self.access_token}"
        params = {"lang": "es", "q": vin, "serviceName": service_name, "p5v": "1.22.3"}

        response = self.session.get(url=search_url, headers=header, params=params)

        if response.status_code == 200:

            return response.json()

        if response.status_code == 401 or response.status_code == 402:
            self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            self.save_session_state()
            self.load_session_state()
            header = self.headers.copy()
            header["Authorization"] = f"Bearer {self.access_token}"
            response = self.session.get(url=search_url, headers=header, params=params)
            if response.status_code == 200:
                return response.json()

        if response.status_code == 401 or response.status_code == 402:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=False)
                self.save_session_state()
                self.load_session_state()

                header = self.headers.copy()
                header["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url, headers=header, params=params
                )
                if response.status_code == 200:
                    return response.json()
        return response

    def buscar_pieza(
        self, vin, query, service_name, search_url, product_url, data_url=None, car=None
    ):

        response_car = self.get_car_data(vin, service_name, data_url, car)
        crumbs = response_car.get("crumbs", [])
        if crumbs:
            data = response_car.get("data", {})
            narrow = data.get("narrowDownOptions", [])
            for n in narrow:
                payload = {}
                description = n.get("description", "")

                if car.capitalize() in description:
                    path = n.get("link", {}).get("path", "")
                    parsed_url = urlparse(path)
                    query_params = parse_qs(parsed_url.query)

                    for p in query_params:
                        if p == "_" or p == "upds":
                            continue
                        payload[p] = query_params[p][0]

                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"

                    response_car = self.session.get(
                        url=data_url, headers=headers, params=payload
                    )

                    vehicle_context = response_car.json().get("vehicleContext", {})
                    model_code = vehicle_context.get("modelCode")
                    model_id = vehicle_context.get("modelId")
                    request_params = {
                        "lang": "es",
                        "modelCode": model_code,
                        "modelId": model_id,
                        "serviceName": service_name,
                        "vin": vin,
                        "q": query,
                    }
                    response = self.session.get(
                        search_url, headers=headers, params=request_params
                    )
                    print(response.json())
                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, query
                    )

                    return parsed_response

                continue

        print(response_car)

        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"

        params = {
            "lang": "es",
            "serviceName": service_name,
            "vin": vin,
            "q": query,
            # "_": str(int(time.time() * 1000)),
        }
        response = self.session.get(search_url, headers=headers, params=params)

        print(response.json())

        parsed_response = self.procesar_resultados(
            response.json(), service_name, vin, product_url, query
        )

        return parsed_response

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
                params_producto = {}
                for p in query_params:
                    if p == "_" or p == "upds":
                        continue
                    params_producto[p] = query_params[p][0]

                consulta_headers = self.headers.copy()
                consulta_headers.update(
                    {"Authorization": f"Bearer {self.access_token}"}
                )

                consulta_producto = self.session.get(
                    product_url, headers=consulta_headers, params=params_producto
                )
                print(consulta_producto.json())
                image_url = (
                    consulta_producto.json()
                    .get("data", {})
                    .get("images", [])[0]
                    .get("uri")
                )

                base_image = self.get_image(image_url, query)

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
                print(productos_data)
                return productos_data

            except Exception as e:
                print(f"Ocurrió un error procesando un registro de categoría: {e}")
                return None


class AudiApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("AUDI", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

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
                print(consulta_producto.url)

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


# Error 402
class CitroenApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("CITROEN", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def buscar_pieza(
        self,
        vin,
        query,
        service_name,
        search_url,
        product_url,
        data_url: Optional[str] = None,
        car: Optional[str] = None,
    ):

        palabra_clave = query.lower().strip()

        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.access_token}"

        payload = {"lang": "es", "vin": vin, "term": palabra_clave, "page": "0"}

        response = self.session.get(url=search_url, params=payload, headers=headers)
        if response.status_code == 200:
            print(response.json())
            parsed_response = self.procesar_resultados(
                response_data=response.json(),
                service_name=service_name,
                vin=vin,
                product_url=product_url,
                query=palabra_clave,
            )
        if (
            response is not None
            and response.status_code == 401
            or response.status_code == 402
        ):
            # print("Intento 1 fallido (401). Refrescando token (Plan B)...")
            # Usamos la lista completa para refrescar
            refrescar_token = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
            if refrescar_token:
                self.save_session_state()
                self.load_session_state()
                response = self.session.get(
                    url=search_url, params=payload, headers=headers
                )
                if response and response.status_code == 200:
                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, palabra_clave
                    )
                    print(parsed_response)
                    return parsed_response
        if (
            response is not None
            and response.status_code == 401
            or response.status_code == 402
        ):
            # print("Intento 2 fallido (401). Realizando re-login completo (Plan C)...")
            # Usamos la lista completa para el nuevo login
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                # print("Archivo de sesión anterior eliminado para un nuevo login.")

            logged = self.login()
            if logged:
                self.save_session_state()
                self.load_session_state()
                self.refresh_access_token(ALL_SERVICES, is_refresh=True)
                self.save_session_state()
                self.load_session_state()
                response = self.session.get(
                    url=search_url, params=payload, headers=headers
                )
                if response and response.status_code == 200:
                    parsed_response = self.procesar_resultados(
                        response.json(), service_name, vin, product_url, palabra_clave
                    )
                    print(parsed_response)
                    return parsed_response
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        print(response_data)
        datos_pieza = []
        items = response_data.get("items", [])
        for item in items:
            item_partno = item.get("partnoHtml", "").replace(" ", "")

            partno_exist = any(
                d.get("numero_pieza") == item_partno for d in datos_pieza
            )
            if partno_exist:
                continue
            url = item.get("url")

            parsed_url = urlparse(url)
            query_params = parse_qs(parsed_url.query)
            payload = {}

            for p in query_params:
                payload[p] = query_params[p][0]

            headers = self.headers.copy()
            headers.update({"Authorization": f"Bearer {self.access_token}"})

            response_html = self.session.get(
                url=product_url, headers=headers, params=payload
            )
            print(response_html.content)
            soup = BeautifulSoup(response_html.text, "html.parser")
            regex_pattern = re.compile(r"^_nav-bom-table\d+$")
            filas_despiece = soup.find_all("tr", id=regex_pattern)

            print(len(filas_despiece))

            for fila in filas_despiece:
                # A. Verificar la celda de posición (posno tc-mcell)
                td_posno = fila.find("td", class_="posno")

                # Extraer el texto y limpiarlo. Si solo contiene &nbsp; o está vacío, resultará en ''
                if td_posno:
                    posno_text = td_posno.text.strip()

                    # Si la celda de posición está vacía después de limpiar el espacio (&nbsp;),
                    # saltar al siguiente registro (fila)
                    if not posno_text:
                        continue

                td_pieza = fila.find("td", class_="portnoFormatted")
                # Denominación
                td_denominacion = fila.find("td", class_="partName")

                # Extracción y limpieza
                numero_pieza = (
                    td_pieza.text.strip().replace("\xa0", " ").replace(" ", "")
                    if td_pieza
                    else "N/A"
                )
                denominacion = (
                    td_denominacion.text.strip() if td_denominacion else "N/A"
                )

                # Acumular los resultados (solo si al menos una pieza o denominación es válida,
                # aunque el filtro de posno ya debería haber funcionado)
                if numero_pieza != "N/A" or denominacion != "N/A":
                    datos_pieza.append(
                        {
                            "id": posno_text,
                            "numero_pieza": numero_pieza,
                            "denominacion": denominacion,
                        }
                    )

        print(datos_pieza)

        return datos_pieza


# Error 402
class PeugeotApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("PEUGEOT", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def buscar_pieza(
        self,
        vin: str,
        term: str,
        service_name: str,
        search_url: Optional[str] = None,
        product_url: Optional[str] = None,
        data_url: Optional[str] = None,
        page: Optional[str] = None,
        car: Optional[str] = None,
    ):
        params = {
            "lang": "es",
            "serviceName": service_name,
            "vin": vin,
            "term": term,
            "page": page if page else "0",
        }

        headers = self.headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        palabra_clave = term.lower().strip()
        response = self.session.get(
            url=search_url or self.consulta_url,
            headers=headers,
            params=params,
        )

        # OK + JSON
        if response.status_code == 200 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            parsed_response = self.procesar_resultados(
                response.json(),
                service_name,
                vin,
                product_url or self.producto_url,
                palabra_clave,
            )
            return parsed_response

        # 401/402 → Refresh → Retry
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            refrescar = self.refresh_access_token(service_name, is_refresh=True)
            if refrescar:
                self.save_session_state()
                self.load_session_state()
                headers = self.headers.copy()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url or self.consulta_url,
                    headers=headers,
                    params=params,
                )
                if (
                    response.status_code == 200
                    and "application/json" in response.headers.get("Content-Type", "")
                ):
                    return self.procesar_resultados(
                        response.json(),
                        service_name,
                        vin,
                        product_url or self.producto_url,
                        palabra_clave,
                    )

        # Re-login completo si sigue fallando
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                ok = self.refresh_access_token(service_name, is_refresh=False)
                if ok:
                    self.save_session_state()
                    self.load_session_state()
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(
                        url=search_url or self.consulta_url,
                        headers=headers,
                        params=params,
                    )
                    if (
                        response.status_code == 200
                        and "application/json"
                        in response.headers.get("Content-Type", "")
                    ):
                        return self.procesar_resultados(
                            response.json(),
                            service_name,
                            vin,
                            product_url or self.producto_url,
                            palabra_clave,
                        )

        if response is not None and response.status_code == 402:
            print(
                "Suscripción requerida para Peugeot. Verifica permisos de 'peugeot_parts' en tu cuenta."
            )
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        items = response_data.get("items", [])
        if not items:
            print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
            return []

        results = []
        for item in items[:50]:
            item_url = item.get("url", "")
            full_url = "https://www.partslink24.com/psa/peugeot_parts/" + item_url
            parsed = urlparse(full_url)
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            try:
                detail_resp = self.session.get(
                    product_url, headers=headers, params=params
                )
                details = (
                    detail_resp.json()
                    if detail_resp.status_code == 200
                    and "application/json"
                    in detail_resp.headers.get("Content-Type", "")
                    else None
                )
            except Exception:
                details = None

            results.append(
                {
                    "caption": item.get("captionHtml"),
                    "partno": item.get("partno"),
                    "url": item_url,
                }
            )

        # Formateo en tabla legible
        def trunc(s, n):
            s = s or ""
            return (s[: n - 1] + "…") if len(s) > n else s

        print("\n" + "=" * 100)
        print(
            f"RESULTADOS PEUGEOT — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)"
        )
        print("=" * 100)
        header = f"{'PARTNO':<18} {'DESCRIPCIÓN':<40} {'URL':<25}"
        print(header)
        print("-" * 100)
        for r in results:
            print(
                f"{trunc(r.get('partno',''),18):<18} "
                f"{trunc(r.get('caption',''),70):<70} "
                f"{trunc(r.get('url',''),25):<25}"
            )
        print("=" * 100)

        return results


class HyundaiApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("HYUNDAI", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def buscar_pieza(
        self,
        vin: str,
        term: str,
        service_name: str,
        search_url: Optional[str] = None,
        product_url: Optional[str] = None,
        data_url: Optional[str] = None,
        page: Optional[str] = None,
        car: Optional[str] = None,
    ):
        params = {
            "lang": "es",
            "serviceName": service_name,
            "vin": vin,
            "term": term,
            "page": page if page else "0",
        }

        headers = self.headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        palabra_clave = term.lower().strip()
        response = self.session.get(
            url=search_url or self.consulta_url,
            headers=headers,
            params=params,
        )

        # OK + JSON
        if response.status_code == 200 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            parsed_response = self.procesar_resultados(
                response.json(),
                service_name,
                vin,
                product_url or self.producto_url,
                palabra_clave,
            )
            return parsed_response

        # 401/402 → Refresh → Retry
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            refrescar = self.refresh_access_token(service_name, is_refresh=True)
            if refrescar:
                self.save_session_state()
                self.load_session_state()
                headers = self.headers.copy()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url or self.consulta_url,
                    headers=headers,
                    params=params,
                )
                if (
                    response.status_code == 200
                    and "application/json" in response.headers.get("Content-Type", "")
                ):
                    return self.procesar_resultados(
                        response.json(),
                        service_name,
                        vin,
                        product_url or self.producto_url,
                        palabra_clave,
                    )

        # Re-login completo si sigue fallando
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                ok = self.refresh_access_token(service_name, is_refresh=False)
                if ok:
                    self.save_session_state()
                    self.load_session_state()
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(
                        url=search_url or self.consulta_url,
                        headers=headers,
                        params=params,
                    )
                    if (
                        response.status_code == 200
                        and "application/json"
                        in response.headers.get("Content-Type", "")
                    ):
                        return self.procesar_resultados(
                            response.json(),
                            service_name,
                            vin,
                            product_url or self.producto_url,
                            palabra_clave,
                        )

        if response is not None and response.status_code == 402:
            print(
                "Suscripción requerida para Hyundai. Verifica permisos de 'hyundai_parts' en tu cuenta."
            )
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        items = response_data.get("items", [])
        if not items:
            print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
            return []

        results = []
        for item in items[:50]:
            item_url = item.get("url", "")
            full_url = (
                "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/"
                + item_url
            )
            parsed = urlparse(full_url)
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            try:
                detail_resp = self.session.get(
                    product_url, headers=headers, params=params
                )
                details = (
                    detail_resp.json()
                    if detail_resp.status_code == 200
                    and "application/json"
                    in detail_resp.headers.get("Content-Type", "")
                    else None
                )
            except Exception:
                details = None

            results.append(
                {
                    "caption": item.get("caption"),
                    "partno": item.get("partno"),
                    "pnc": item.get("pnc"),
                    "url": item_url,
                    "details": details,
                }
            )

        # Formateo en tabla legible
        def trunc(s, n):
            s = s or ""
            return (s[: n - 1] + "…") if len(s) > n else s

        print("\n" + "=" * 100)
        print(
            f"RESULTADOS HYUNDAI — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)"
        )
        print("=" * 100)
        header = f"{'PARTNO':<18} {'PNC':<12} {'DESCRIPCIÓN':<40} {'URL':<25}"
        print(header)
        print("-" * 100)
        for r in results:
            print(
                f"{trunc(r.get('partno',''),18):<18} "
                f"{trunc(r.get('pnc',''),12):<12} "
                f"{trunc(r.get('caption',''),40):<40} "
                f"{trunc(r.get('url',''),25):<25}"
            )
        print("=" * 100)

        return results


class KiaApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("KIA", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def buscar_pieza(
        self,
        vin: str,
        term: str,
        service_name: str,
        search_url: Optional[str] = None,
        product_url: Optional[str] = None,
        data_url: Optional[str] = None,
        page: Optional[str] = None,
        car: Optional[str] = None,
    ):
        params = {
            "lang": "es",
            "serviceName": service_name,
            "vin": vin,
            "term": term,
            "page": page if page else "0",
        }

        headers = self.headers.copy()
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        palabra_clave = term.lower().strip()
        response = self.session.get(
            url=search_url or self.consulta_url,
            headers=headers,
            params=params,
        )

        # OK + JSON
        if response.status_code == 200 and "application/json" in response.headers.get(
            "Content-Type", ""
        ):
            parsed_response = self.procesar_resultados(
                response.json(),
                service_name,
                vin,
                product_url or self.producto_url,
                palabra_clave,
            )
            return parsed_response

        # 401/402 → Refresh → Retry
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            refrescar = self.refresh_access_token(service_name, is_refresh=True)
            if refrescar:
                self.save_session_state()
                self.load_session_state()
                headers = self.headers.copy()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = self.session.get(
                    url=search_url or self.consulta_url,
                    headers=headers,
                    params=params,
                )
                if (
                    response.status_code == 200
                    and "application/json" in response.headers.get("Content-Type", "")
                ):
                    return self.procesar_resultados(
                        response.json(),
                        service_name,
                        vin,
                        product_url or self.producto_url,
                        palabra_clave,
                    )

        # Re-login completo si sigue fallando
        if response is not None and (
            response.status_code == 401 or response.status_code == 402
        ):
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            logged = self.login()
            if logged:
                ok = self.refresh_access_token(service_name, is_refresh=False)
                if ok:
                    self.save_session_state()
                    self.load_session_state()
                    headers = self.headers.copy()
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = self.session.get(
                        url=search_url or self.consulta_url,
                        headers=headers,
                        params=params,
                    )
                    if (
                        response.status_code == 200
                        and "application/json"
                        in response.headers.get("Content-Type", "")
                    ):
                        return self.procesar_resultados(
                            response.json(),
                            service_name,
                            vin,
                            product_url or self.producto_url,
                            palabra_clave,
                        )

        if response is not None and response.status_code == 402:
            print(
                "Suscripción requerida para KIA. Verifica permisos de 'kia_parts' en tu cuenta."
            )

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        items = response_data.get("items", [])
        if not items:
            print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
            return []

        results = []
        for item in items[:50]:
            item_url = item.get("url", "")
            full_url = (
                "https://www.partslink24.com/hyundai-kia-automotive-group/kia_parts/"
                + item_url
            )
            parsed = urlparse(full_url)
            params = {k: v[0] for k, v in parse_qs(parsed.query).items()}

            headers = self.headers.copy()
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            try:
                detail_resp = self.session.get(
                    product_url, headers=headers, params=params
                )
                details = (
                    detail_resp.json()
                    if detail_resp.status_code == 200
                    and "application/json"
                    in detail_resp.headers.get("Content-Type", "")
                    else None
                )
            except Exception:
                details = None

            results.append(
                {
                    "caption": item.get("caption"),
                    "partno": item.get("partno"),
                    "pnc": item.get("pnc"),
                    "url": item_url,
                    "details": details,
                }
            )

        # Formateo en tabla legible
        def trunc(s, n):
            s = s or ""
            return (s[: n - 1] + "…") if len(s) > n else s

        print("\n" + "=" * 100)
        print(
            f"RESULTADOS KIA — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)"
        )
        print("=" * 100)
        header = f"{'PARTNO':<18} {'PNC':<12} {'DESCRIPCIÓN':<40} {'URL':<25}"
        print(header)
        print("-" * 100)
        for r in results:
            print(
                f"{trunc(r.get('partno',''),18):<18} "
                f"{trunc(r.get('pnc',''),12):<12} "
                f"{trunc(r.get('caption',''),40):<40} "
                f"{trunc(r.get('url',''),25):<25}"
            )
        print("=" * 100)

        return results


def test(vin: str, brand: str, query: str, car: Optional[str] = None):
    # Usamos la clase específica de la marca para que sea más limpio
    if brand.upper() == "VW":
        session_manager = VwAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "BMW":
        session_manager = BmwAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "TOYOTA":
        session_manager = ToyotaAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SMART":
        session_manager = SmartAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "OPEL":
        # Para OPEL usamos funcionalidad avanzada con extracción de imágenes
        opel_api = OpelApi(ACCOUNT, USER, PASSWORD)
        
        print("Cargando estado de sesion anterior...")
        is_ready = opel_api.load_session_state()

        if not is_ready:
            logged_in = opel_api.login()
            if logged_in:
                is_ready = opel_api.refresh_access_token(ALL_SERVICES, is_refresh=False)
                if is_ready:
                    opel_api.save_session_state()

        if not is_ready:
            print("Fallo en la autenticación. No se puede continuar.")
            return

        print(f"\n🔧 Extrayendo catId para VIN: {vin}")
        cat_id = opel_api.obtener_cat_id(vin)
        if cat_id:
            print(f"✅ catId extraído exitosamente: {cat_id}")
        else:
            print("❌ No se pudo extraer el catId")

        print(f"\n🔍 Búsqueda con extracción de imágenes para: '{query}'")
        try:
            # Usar la funcionalidad avanzada que incluye extracción de imágenes
            resultados = opel_api.buscar_y_consultar_imagenes(vin, query, aplicar_filtro=False)
            
            if resultados and resultados.get("piezas_unicas"):
                piezas_unicas = resultados.get("piezas_unicas", [])
                
                # Función para limpiar caption (eliminar texto después de <br>)
                def limpiar_caption(caption):
                    if caption and '<br>' in caption:
                        return caption.split('<br>')[0].strip()
                    return caption or ""
                
                # Imprimir solo las piezas únicas
                print(f"\n📦 Piezas únicas encontradas ({len(piezas_unicas)}):")
                print("-" * 80)
                
                for pieza in piezas_unicas:
                    caption_limpio = limpiar_caption(pieza.get('caption', ''))
                    print(f"• {pieza.get('gmNo', 'N/A')} | {pieza.get('gmOpelNo', 'N/A')} | {caption_limpio}")
                    if pieza.get('url'):
                        print(f"  🔗 {pieza['url']}")
                
            else:
                print("❌ No se obtuvieron resultados")
                
        except Exception as e:
            print(f"❌ Error en la búsqueda avanzada: {e}")
            
        return  # Salir aquí para OPEL, no continuar con el flujo estándar
    elif brand.upper() == "NISSAN":
        session_manager = NissanApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MITUBISHI":
        session_manager = MitsubishiApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "FORD":
        session_manager = FordAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "RENAULT":
        session_manager = RenaultApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SEAT":
        session_manager = SeatApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "AUDI":
        session_manager = AudiApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "CITROEN":
        session_manager = CitroenApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "PEUGEOT":
        session_manager = PeugeotApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "HYUNDAI":
        session_manager = HyundaiApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "KIA":
        session_manager = KiaApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "MERCEDES":
        session_manager = MercedesApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "SKODA":
        session_manager = SkodaApi(ACCOUNT, USER, PASSWORD)
    else:
        # Aquí podrías añadir BmwAPI, etc.
        print(f"Marca {brand} no soportada.")
        return

    print("Cargando estado de sesion anterior...")
    is_ready = session_manager.load_session_state()

    if not is_ready:
        # print("No se encontro el archivo de sesion. Realizando login...")

        logged_in = session_manager.login()
        if logged_in:
            is_ready = session_manager.refresh_access_token(
                ALL_SERVICES, is_refresh=False
            )
            if is_ready:
                session_manager.save_session_state()

    if not is_ready:
        print("Fallo en la autenticación. No se puede continuar.")
        return

    session_manager.buscar_pieza(
        vin,
        query,
        session_manager.service_name,
        session_manager.consulta_url,
        session_manager.producto_url,
        session_manager.data_url,
        car,
    )


if __name__ == "__main__":
    num_args = len(sys.argv)

    if num_args < 4 or num_args > 5:
        print(
            "Error: Se requieren 3 argumentos: VIN, Marca y Pieza. Ejemplo: python partslink.py WVWZZZ1KZ4B024648 'vw' 'cerradura de puerta' 'golf'"
        )
        sys.exit(1)
    vin = sys.argv[1]
    marca = sys.argv[2]
    pieza = sys.argv[3]

    if num_args == 5:
        car = sys.argv[4]
    else:
        car = None

    # marca = "smart"
    # vin = "WME4513311K043393"
    # pieza = "Espejos retrovisores"

    #marca = "ford"
    #vin = "WF0JXXWPCJFM36230"
    #pieza = "Válvula/Recirculación Gases Escape"

    # marca = "nissan"
    # vin = "SJNFDAE11U1245311"
    # pieza = "panel"

    # marca = "kia"
    # vin = "KNEUP751256716941"
    # pieza = "puerta"

    # marca = "peugeot"
    # vin = "VF30U9HD8DS031095"
    # pieza = "puerta"

    # marca = "citroen"
    # vin = "VF7GJWJYB93233667"
    # pieza = "cerradura de puerta"

    # marca = "audi"
    # vin = "WAUZZZ8U6DR109036"
    # pieza = "kit de distribucion"

    # marca = "seat"
    # # vin = "VSSZZZ6LZ4R224453"
    # vin = "VSSZZZ1MZ3R068750"
    # pieza = "cerradura de puerta"
    # car = "toledo"

    # marca = "renault"
    # vin = "VF1LA050527117013"
    # pieza = "cerradura de puerta"

    # marca = "HYUNDAI"
    # vin = "KMHST81UADU066300"
    # pieza = "puerta"          # term

    marca = "OPEL"
    vin = "W0LMRF4SEEB062229"
    pieza = "filtros "

    # vin = "JTEBZ29J100180316"
    # marca = "toyota"
    # pieza = "cerradura de puerta"

    # marca = "VW"
    # pieza = "Medidor de aire"
    # vin = "WVWZZZ1KZ4B024648"

    # marca = "mitubishi"
    # vin = "4MBMND32ATE001965"
    # pieza = "Kit de distribucion"

    # marca = "BMW"
    # vin = "WBAPP51040A792442"
    # pieza = "motor"

    # marca = "mercedes"
    # vin = "WDD2040081A191979"
    # pieza = "grupo de interruptores"

    # marca = "skoda"
    # vin = "TMBCF46Y123582689"
    # pieza = "cerradura de puerta"

    # marca = "citroen"
    # vin = "VF7GJWJYB93233667"
    # pieza = "cerradura de puerta"

    # COMENTAR TODOS LOS PRINT SI YA NO HAY NADA QUE DEPURAR

    if not all([ACCOUNT, USER, PASSWORD, ALL_SERVICES]):
        print(
            "Error: Asegúrate de que 'Account', 'User', 'Password' y 'serviceNamesBMW' están en tu .env"
        )
    else:

        test(vin, marca, pieza, car)
