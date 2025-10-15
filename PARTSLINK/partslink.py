import requests
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
        "producto_url": "https://www.partslink24.com/psa/peugeot_parts/scope.action",
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
            print(response_login.content)
            print(self.session.cookies)
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
        data_url: Optional[any] = None,
    ):

        if not self.access_token:
            return None

        # --- Intento 1: Usar la sesión actual ---
        palabra_clave = query.lower().strip()
        response = self._realizar_consulta(vin, query, service_name, search_url)
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
        self, vin, query, service_name, search_url, product_url, data_url=None
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
            headers["Authorization"] = f"Bearer {self.access_token}"

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

    def buscar_pieza(self, vin, query, service_name, search_url, product_url, data_url):

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
        self, vin, query, service_name, search_url, product_url, data_url=None
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

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        print(response_data)
        return


class KiaApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("KIA", {})
        self.service_name = brand_info.get("service_name")
        self.consulta_url = brand_info.get("consulta_url")
        self.producto_url = brand_info.get("producto_url")
        self.data_url = brand_info.get("datos_url")

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        print(response_data)
        return


class OpelApi(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_info = BRAND_DATA.get("OPEL", {})
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
    ):
        params = {
            "lang": "es",
            "mode": "A0LW0ESES",
            "page": page if page else "0",
            "textKey": "",
            "term": term,
            "vin": vin,
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
        print(response.url)

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
                "Suscripción requerida para Opel. Verifica permisos de 'opel_parts' en tu cuenta."
            )
        return response

    def procesar_resultados(self, response_data, service_name, vin, product_url, query):
        # Estructura tipo Nissan/Opel: items[]
        items = response_data.get("items", [])
        if not items:
            print(f"No se encontraron resultados para '{query}' (VIN {vin}).")
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

        print("\n" + "=" * 100)
        print(
            f"RESULTADOS OPEL — VIN {vin} — Búsqueda: {query} — {len(results)} elemento(s)"
        )
        print("=" * 100)
        header = f"{'PARTNO':<18} {'DESCRIPCIÓN':<40} {'URL':<25}"
        print(header)
        print("-" * 100)
        for r in results:
            print(
                f"{trunc(r.get('partno',''),18):<18} "
                f"{trunc(r.get('caption',''),40):<40} "
                f"{trunc(r.get('url',''),25):<25}"
            )
        print("=" * 100)

        return results


class MitsubishiApi(PartsLink24API):
    pass


def test(vin: str, brand: str, query: str):
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
        session_manager = OpelApi(ACCOUNT, USER, PASSWORD)
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
    )


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(
            "Error: Se requieren 3 argumentos: VIN, Marca y Pieza. Ejemplo: python partslink.py WVWZZZ1KZ4B024648 'vw' 'cerradura de puerta'"
        )
        sys.exit(1)
    vin = sys.argv[1]
    marca = sys.argv[2]
    pieza = sys.argv[3]

    # marca = "smart"
    # vin = "WME4513311K043393"
    # pieza = "Espejos retrovisores"

    # marca = "FORD"
    # vin = "WF0JXXWPBJDR70419"
    # pieza = "Sistema de cerradura"

    # marca = "nissan"
    # vin = "SJNFDAE11U1245311"
    # pieza = "panel de puerta"

    # marca = "kia"
    # vin = "KNEUP751256716941"
    # pieza = "valvulas egr"

    # marca = "peugeot"
    # vin = "VF30U9HD8DS031095"
    # pieza = "kit de distribucion"

    # marca = "citroen"
    # vin = "VF7GJWJYB93233667"
    # pieza = "cerradura de puerta"

    # marca = "audi"
    # vin = "WAUZZZ8U6DR109036"
    # pieza = "kit de distribucion"

    # marca = "seat"
    # vin = "VSSZZZ6LZ4R224453"
    # pieza = "cerradura de puerta"

    # marca = "renault"
    # vin = "VF1JP0D0533150256"
    # pieza = "soporte conmutado"

    # marca = "OPEL"
    # vin = "W0LMRF4SEEB062229"
    # pieza = "cerradura de puerta"

    # vin = "JTEBZ29J100180316"
    # marca = "toyota"
    # pieza = "panel de puerta"

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

        test(vin, marca, pieza)
