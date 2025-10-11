import os


import requests
import hashlib
import re
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv


load_dotenv()
usuario = os.getenv("USER")
clave = os.getenv("PASSWORD")


class NacexAPI:

    def __init__(self, user, password):
        load_dotenv()
        self.user = user
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.url = "https://pda.nacex.com/nacex_ws/ws"

    def get_agency(self, codigo_postale: str, poblacion: Optional[str] = None):
        params = {
            "method": "getAgencia",
            "user": self.user,
            "pass": self.password,
            "data": f"cp={codigo_postale}",
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            response_data = response.text.split("|")
            response_dict = {
                "Codigo agencia": response_data[0],
                "Nombre de agencia": response_data[1],
                "Direccion": response_data[2],
                "Telefono": response_data[3],
            }

            print(response_dict)

            return response_dict

        except requests.exceptions.RequestException as e:
            print(e)
            return None
        except Exception as e:
            print(e)
            return None

    def get_statistics(self, tipo, fecha: Optional[str] = None):

        formato_fecha = ""
        if tipo == 1 and fecha:
            formato_fecha = datetime.strptime(fecha, "%d-%m-%Y %H:%M").strftime(
                "%d/%m/%Y"
            )
            # formato_fecha = fecha_dt.strftime("%d/%m/%Y")
        elif tipo >= 2 and fecha:
            formato_fecha = datetime.strptime(fecha, "%d-%m-%Y %H:%M").strftime(
                "%d/%m/%Y %H:%M"
            )

        # fecha.replace('-', '/')
        data_fields = {
            "tipo": tipo,
            "params": formato_fecha,
        }
        data = "|".join(f"{k}={v}" for k, v in data_fields.items())
        params = {
            "method": "getEstadisticas",
            "user": self.user,
            "pass": self.password,
            "data": data,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            response_data = []

            print(response.url)
            stadistics_list = response.text.split("|")

            for item in stadistics_list:
                stadistics = [x for x in item.split("~") if x.strip()]
                data_ditc = {}

                if len(stadistics) == 3:
                    data_ditc["Dia y Hora"] = stadistics[0]
                    data_ditc["S o N"] = stadistics[1]
                    data_ditc["Total de expediciones"] = stadistics[2]

                elif len(stadistics) == 5:
                    data_ditc["Dia de entrega"] = stadistics[0]
                    data_ditc["Hora de entrega"] = stadistics[1]
                    data_ditc["Estado"] = stadistics[2]
                    data_ditc["Codigo de estado"] = stadistics[3]
                    data_ditc["Total de expediciones"] = stadistics[4]

                elif len(stadistics) == 11:
                    data_ditc["Código único de la expedición"] = stadistics[0]
                    data_ditc["Agencia"] = stadistics[1]
                    data_ditc["Numero de expedición"] = stadistics[2]
                    data_ditc["Referencia de cliente"] = stadistics[3]
                    data_ditc["Población de entrega"] = stadistics[4]
                    data_ditc["Código postal de entrega"] = stadistics[5]
                    data_ditc["País de entrega"] = stadistics[6]
                    data_ditc["Día entrega"] = stadistics[7]
                    data_ditc["Hora entrega"] = stadistics[8]
                    data_ditc["Estado"] = stadistics[9]
                    data_ditc["Código del estado"] = stadistics[10]
                if data_ditc:
                    response_data.append(data_ditc)
            print(f"Respuesta: {response.text}")
            print(response_data)
            return response_data
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

        except Exception as e:
            print(f"Error durante la solicitud: {e}")

    def get_expedition(self, code_expe: str):

        params = {
            "method": "getExpedicion",
            "data": f"codeExp={code_expe}",
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)
            print("")
            print(response.text)
            return response.text

        except requests.exceptions.ConnectionError as e:
            print(e)
            return None

    def get_expedition_state(self, expe_code: str):
        """
        Obtenemos el estado de una expedicion a partir de su código.
        :param expe_code: Código de la expedición.
        """

        params = {
            "method": "getEstadoExpedicion",
            "data": f"expe_codigo={expe_code}",
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)
            data = response.text.split("|")

            response_dict = {
                "Identificador único de la expedición": data[0],
                "Fecha del estado (dd/mm/yyyy)": data[1],
                "Hora del estado (hh:mm)": data[2],
                "Observaciones del estado (persona entrega, plataforma, código de recogida,etc.)": data[
                    3
                ],
                "Estado (OK, RECOGIDO, TRANSITO, REPARTO, INCIDENCIA)": data[4],
                "Código del estado o incidencia (devuelve la última EXPEDICIÓN vinculada a esta referencia)": data[
                    5
                ],
                "Código de la agencia de origen": data[6],
                "Número de albaran de la agencia": data[7],
            }
            print(response_dict)
            return response_dict
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

        except Exception as e:
            print(f"Error durante la solicitud: {e}")

    def get_expe_codigo(self):
        """
        Get expedition code from NACEX.
        """

        params = {"method": "getExpeCodigo", "user": self.user, "pass": self.password}

        try:
            response = requests.get(self.url, params=params)
            print(response.url)
            response.raise_for_status()

            print(f"Respuesta: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

        except Exception as e:
            print(f"Error durante le solicitud: {e}")

    def get_tag(self, agencia: str, numero: str, model: Optional[str] = None):
        """
        Obtenemos la etiqueta de una expedición a partir de su código y modelo
        de etiquetadorar.

        :param expe_code: Código de la expedición.
        :param model: Modelo de la etiquetadora. Pueden ser: TECSV4_B, TECEV4_B, TECFV4_B, ZEBRA_B, IMAGEN_B o PDF_B

        """
        data_field = {"agencia": agencia, "albaran": numero, "modelo": model.upper()}
        data = "|".join(f"{k}={v}" for k, v in data_field.items())

        params = {
            "method": "getEtiqueta",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }
        # params = {
        #     "method": "getEtiqueta",
        #     "data": f"expe_codigo={expe_code}|modelo={model}",
        #     "user": self.user,
        #     "pass": self.password,
        # }

        try:
            response = requests.get(self.url, params=params)
            print(response.url)
            response.raise_for_status()

            print(f"Respuesta: {response.text}")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

        except Exception as e:
            print(f"Error durante la solicitud: {e}")

    def get_delivery_info(self, tipo: str, codigo: str, agencia: Optional[str] = None):
        """
        Obtenemos la información de entrega a partir de la fecha, servicio, frecuencia,
        código postal de recogida y entrega, y kilómetros.

        :param tipo: Tipo de servicio E o R, expedicion o recogida
        :param codigo: codigo de expedicion o recogida
        :param
        """

        data_fields = {
            "tipo": tipo,
            "codigo": codigo,
            # "agencia": agencia,
        }

        data = "|".join(f"{k}={v}" for k, v in data_fields.items())
        params = {
            "method": "getInfoEnvio",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

    def get_POD(self, code_expe: str, document_type: str, format: str, **kwargs):
        data_fields = {
            "codexp": code_expe,
            "doc_tipo": document_type.upper(),
            "formato": format.upper(),
        }

        data = "|".join(f"{k}={v}" for k, v in data_fields.items())
        params = {
            "method": "getPOD",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }

        try:

            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)

            return response
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")
            return {"OK": False, "error": str(e)}

    def get_PROXI(self, tpye: str, proxi_pais: str, proxi_cp: str, cod: str):
        data_fields = {
            "tipo": tpye,
            "cod": cod,
            "proxi_pais": proxi_pais,
            "proxi_cp": proxi_cp,
        }
        data = "|".join(f"{k}={v}" for k, v in data_fields.items())
        params = {
            "method": "getProxi",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)

            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")

    def edit_expedition(
        self,
        del_cli: str,
        num_cli: str,
        dep_cli: str,
        fecha: str,
        code_service: str,
        code_cobro: str,
        exceso_peso: str,
        ref_cli: str,
        envase_code: str,
        bultos: str,
        peso: str,
        nom_ent: str,
        dir_ent: str,
        pais_ent: str,
        cp_ent: str,
        pob_ent: str,
        tel_ent: str,
        expe_codigo: str,
        origen: str,
        albaran: str,
        ref: str,
    ):
        data_fields = {
            "del_cli": del_cli,
            "num_cli": num_cli,
            "dep_cli": dep_cli,
            "fec": fecha,
            "tip_ser": code_service,
            "tip_cob": code_cobro,
            "exc": exceso_peso,
            "ref_cli": ref_cli,
            "tip_env": envase_code,
            "bul": bultos,
            "kil": peso,
            "nom_ent": nom_ent,
            "dir_ent": dir_ent,
            "pais_ent": pais_ent,
            "cp_ent": cp_ent,
            "pob_ent": pob_ent,
            "tel_ent": tel_ent,
        }
        data = "|".join(f"{k}={v}" for k, v in data_fields.items())

        params = {
            "method": "editExpedicion",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)

            return response.text
        except Exception as e:
            print(e)
            return None

    def put_expedition(
        self,
        nom_ent,
        dir_ent,
        cp_ent,
        pob_ent,
        pais_ent,
        tel_ent,
        ret,
        obs1,
        impresora: Optional[str] = None,
        reembolso: Optional[any] = None,
    ):

        data_fields = {
            "del_cli": "2901",
            "num_cli": "10045",
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
            "seguimiento": "S",
        }
        data = "|".join(f"{k}={v}" for k, v in data_fields.items())
        params = {
            "method": "putExpedicion",
            "data": data,
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            print(response.url)
            response.raise_for_status()
            respuesta = response.text
            tracking_match = re.search(r"^(\d{9})\|", respuesta)
            albaran_match = re.search(r"\|(\d{4}/\d+)\|", respuesta)
            link_match = re.search(
                r"\|(https://www\\.nacex\\.com//seguimientoDetalle\\.do\\?[^|]+)\|",
                respuesta,
            )

            bloques = re.findall(r"\{[^}]+\|}", respuesta)

            if tracking_match and albaran_match:
                tracking = tracking_match.group(1)
                albaran = albaran_match.group(1)
                link = link_match.group(1) if link_match else ""

                tag = "".join(bloques)
                nombre_etiqueta = f"etiqueta_{albaran.replace('/', '')}.txt"

                with open(nombre_etiqueta, "w", encoding="utf-8") as f:
                    f.write(tag)

                print(response.json())
                etiqueta_impresa = True  # Placeholder for actual printing logic
                return {
                    "OK": True,
                    "tracking": tracking,
                    "albaran": albaran,
                    "link": link,
                    "etiqueta_path": nombre_etiqueta,
                    "etiqueta_impresa": etiqueta_impresa,
                }
            else:
                print("No se pudo extraer el código de seguimiento o albarán.")

            return response.text

        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")
            return {"OK": False, "error": str(e)}

    def cancel_expedition(self, expe_code: str):
        """
        Cancelamos una expedición.
        :param expe_code: Código de la expedición
        """

        params = {
            "method": "cancelExpedicion",
            "data": f"expe_codigo={expe_code}",
            "user": self.user,
            "pass": self.password,
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            print(response.url)

            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error de Conexion: {e}")


nacex_api = NacexAPI(usuario, clave)
# nacex_api.get_expedition_state("444279350")
# nacex_api.get_expe_codigo()
# nacex_api.get_agency("08100")
# nacex_api.get_PROXI('E', 'ES', '28010', '444306408')
# nacex_api.get_POD("444306408", "e", "PDF")
# nacex_api.get_delivery_info('E', '12473082')
nacex_api.get_tag("0826", "2901/12473082", "TECFV4_B")
# nacex_api.get_statistics(3, "15-07-2025 20:00")

# nacex_api.get_expedition('444306408')
# nacex_api.get_expedition_state("444306408")
