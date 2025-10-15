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
        "datos_url":"https://www.partslink24.com/psa/citroen_parts/vin-group.action?hintstoken=162166eb-8a1a-4a29-8d0b-b6f4ebc5ba8f&mode=A0LW0ESES&vin=VF7YCTMFB12A07065&lang=es&upds=2024.02.13+09%3A27%3A21+CET&openVinDialog=true",
        "datos_url_base":"https://www.partslink24.com/psa/citroen_parts/vin-group.action"
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
        "datos_url":"https://www.partslink24.com/fiatspa/fiatp_parts/vin-group.action?hintstoken=c97f7c35-1449-44a3-8259-03e1b6e5e423&mode=A0LW0ESES&sincom=&vin=ZFA19900000250470&lang=es&upds=2025.09.17+10%3A40%3A29+CEST&openVinDialog=true",
        "datos_url_base":"https://www.partslink24.com/fiatspa/fiatp_parts/vin-group.action"
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
        "datos_url":"https://www.partslink24.com/ford/fordp_parts/vin-group.action?hintstoken=d3e6872c-2047-407c-ba45-7b91e84f0b2a&mode=A0LW0ESES&vin=WF0DXXGAKDDP19269&lang=es&upds=2025.10.01+10%3A59%3A36+CEST&openVinDialog=true",
        "datos_url_base":"https://www.partslink24.com/ford/fordp_parts/vin-group.action"
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
        "datos_url": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/vin-group.action?hintstoken=a8cd3c04-8a1f-486f-8689-8d7b00b31c38&mode=A0LW0ESES&vin=KMFAB17RPHK008211&lang=es&upds=2025.09.30+06%3A41%3A41+UTC&openVinDialog=true",
        "datos_url_base": "https://www.partslink24.com/hyundai-kia-automotive-group/hyundai_parts/vin-group.action"
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
        "datos_url": "https://www.partslink24.com/iveco/iveco_parts/vin-group.action?mode=A0LW0ESES&vin=ZCFC3070105209146&lang=es&upds=2025.09.26+18%3A46%3A59+CEST&openVinDialog=true",
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

# Añadir después de la clase PartsLink24API y antes de las implementaciones específicas

class HtmlAPI(PartsLink24API):
    """
    Clase base para todas las APIs que devuelven HTML en lugar de JSON.
    Implementa la lógica común para manejar la autenticación y las solicitudes.
    """
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        self.datos_url = None  # Debe ser definido por las subclases
    
    def obtener_datos_coche(self, vin, service_name=None, datos_url=None):
        """
        Método para obtener datos del coche para APIs HTML.
        Asegura que el token de acceso esté presente y se incluya en la solicitud.
        """
        if service_name is None:
            service_name = self.service_name
        
        if datos_url is None and self.datos_url:
            datos_url = self.datos_url
        
        # Verificar si tenemos un token de acceso válido y forzar un refresh
        print(f"🔄 {self.__class__.__name__} - Forzando refresh del token de acceso...")
        success = self.refresh_access_token(ALL_SERVICES, is_refresh=True)
        if not success or not self.access_token:
            print(f"❌ {self.__class__.__name__} - No se pudo obtener un token de acceso válido")
            return None
        
        print(f"🔍 {self.__class__.__name__} - Enviando consulta para VIN: {vin}")
        
        # Preparar datos para enviar en el POST
        payload = {
            'vin': vin,
            'lang': 'es',
            'mode': 'A0LW0ESES',
            'openVinDialog': 'true'
        }
        
        # Headers para la petición - IMPORTANTE: Incluir el token en los headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest',
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'text/html,application/xhtml+xml,application/xml',
            'Referer': 'https://www.partslink24.com/'
        }
        
        # Asegurar que el token está en las cookies de la sesión
        self.session.cookies.set('access_token', self.access_token)
        
        # Guardar el estado de la sesión para asegurar que las cookies se mantienen
        self.save_session_state()
        
        print(f"🔐 {self.__class__.__name__} - Token de acceso: {self.access_token[:10]}...")
        print(f"📤 {self.__class__.__name__} - Payload enviado: {payload}")
        print(f"🌐 {self.__class__.__name__} - URL destino: {self.datos_url_base}")

        # Hacer petición POST con el VIN en el payload
        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
        
        print(f"📥 {self.__class__.__name__} - Respuesta recibida - Status: {response.status_code}")
        
        # Verificar si la respuesta indica modo demo (sin autenticación)
        if response.status_code == 200 and response.text:
            if "NOT_LOGGED_IN_DEMO" in response.text or "demo\":true" in response.text or "Esta función no está disponible en el modo de demostración" in response.text:
                print(f"⚠️ {self.__class__.__name__} - Respuesta en modo demo. Problema de autenticación detectado.")
                print("Intentando nuevamente con login forzado...")

                # Eliminar archivo de sesión para forzar login limpio
                import os
                if os.path.exists(self.session_file):
                    os.remove(self.session_file)
                    print(f"🗑️ {self.__class__.__name__} - Archivo de sesión eliminado")

                # Forzar login completo y nuevo token - usar servicio específico
                login_success = self.login(self.service_name)
                if login_success:
                    print(f"✅ {self.__class__.__name__} - Login exitoso")
                    token_success = self.refresh_access_token(self.service_name, is_refresh=False)
                    if token_success:
                        print(f"✅ {self.__class__.__name__} - Token refrescado exitosamente")
                        self.save_session_state()

                        # Actualizar headers con nuevo token
                        headers['Authorization'] = f'Bearer {self.access_token}'
                        self.session.cookies.set('access_token', self.access_token)

                        # Reintentar la solicitud
                        response = self.session.post(self.datos_url_base, data=payload, headers=headers)
                        print(f"📥 {self.__class__.__name__} - Respuesta del segundo intento - Status: {response.status_code}")

                        # Verificar si el segundo intento también falló
                        if "NOT_LOGGED_IN_DEMO" in response.text or "demo\":true" in response.text or "Esta función no está disponible en el modo de demostración" in response.text:
                            print(f"❌ {self.__class__.__name__} - El segundo intento también falló. El servicio puede requerir autenticación especial.")
                    else:
                        print(f"❌ {self.__class__.__name__} - Error al refrescar token")
                else:
                    print(f"❌ {self.__class__.__name__} - Error en login")

        return response
class BmwAPI(PartsLink24API):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        # Cargamos los datos específicos de BMW
        brand_data = BRAND_DATA.get("BMW", {})
        self.service_name = brand_data.get("service_name")
        self.datos_url = brand_data["datos_url"]

   


class FordAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["FORD"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class FiatAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["FIAT"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class CitroenAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["CITROEN"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]


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
class HyundaiApi(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["HYUNDAI"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class KiaAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["KIA"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]
        
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


class PeugeotAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["PEUGEOT"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class NissanAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["NISSAN"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class VolvoAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["VOLVO"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class OpelAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["OPEL"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class LanciaAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["LANCIA"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

class IvecoAPI(HtmlAPI):
    def __init__(self, account, user, password):
        super().__init__(account, user, password)
        brand_data = BRAND_DATA["IVECO"]
        self.service_name = brand_data["service_name"]
        self.datos_url = brand_data["datos_url"]
        self.datos_url_base = brand_data["datos_url_base"]

def procesar_respuesta_html(response, vin, marca, datos_url):
    """
    Función para procesar respuestas HTML de marcas como Peugeot, Nissan y Volvo.
    Extrae dinámicamente todos los pares campo-valor de la tabla vinInfoTable.
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
            "html_file": html_filename,
            "campos": {}  # Diccionario para almacenar todos los campos dinámicamente
        }

        if tabla_info:
            print(f"✅ Tabla vinInfoTable encontrada para {marca}")

            # Extraer todas las filas de la tabla
            filas = tabla_info.find_all('tr')

            for fila in filas:
                celdas = fila.find_all('td')

                # Procesar filas con 2 celdas (campo-valor)
                if len(celdas) == 2:
                    campo = celdas[0].get_text(strip=True)
                    valor = celdas[1].get_text(strip=True)
                    # Almacenar directamente el par campo-valor
                    if campo and valor:
                        datos_coche["campos"][campo] = valor

                # Procesar filas con 4 celdas (dos pares campo-valor)
                elif len(celdas) == 4:
                    campo1 = celdas[0].get_text(strip=True)
                    valor1 = celdas[1].get_text(strip=True)
                    campo2 = celdas[2].get_text(strip=True)
                    valor2 = celdas[3].get_text(strip=True)

                    # Almacenar ambos pares
                    if campo1 and valor1:
                        datos_coche["campos"][campo1] = valor1
                    if campo2 and valor2:
                        datos_coche["campos"][campo2] = valor2

            print(f"✅ Datos del vehículo {marca} extraídos exitosamente")
            print(f"📋 Campos extraídos: {list(datos_coche['campos'].keys())}")

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

        # Mostrar todos los campos dinámicamente
        campos = datos_coche.get('campos', {})
        if campos:
            for campo, valor in campos.items():
                print(f"{campo}: {valor}")
        else:
            print("No se encontraron campos extraídos")

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
    MARCAS_HTML = ["PEUGEOT", "NISSAN", "VOLVO", "OPEL", "LANCIA", "KIA", "IVECO", "HYUNDAI","FORD","FIAT","CITROEN"]
    
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
    elif brand.upper() == "HYUNDAI":
        session_manager = HyundaiApi(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "FORD":
        session_manager = FordAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "FIAT":
        session_manager = FiatAPI(ACCOUNT, USER, PASSWORD)
    elif brand.upper() == "CITROEN":
        session_manager = CitroenAPI(ACCOUNT, USER, PASSWORD)
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
