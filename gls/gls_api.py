import base64
import requests
import xml.etree.ElementTree as ET


uid_cliente = "6BAB7A53-3B6D-4D5A-9450-702D2FAC0B11"


class GlsApi:
    def __init__(self, uid_cliente, url="https://wsclientes.asmred.com/b2b.asmx"):
        self.uid_cliente = uid_cliente
        self.url = url

    def guardar_envio(self, datos_envio: dict):
        """Preparacion de datos de envio 📦:
        Construye el XML, envía la solicitud a GLS para crear un envío y procesa la respuesta.
        Recibe un diccionario con todos los datos necesarios para el envío.
        """
        xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
                <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
                  <soap12:Body>
                    <GrabaServicios xmlns="http://www.asmred.com/">
                      <docIn>
                        <Servicios uidcliente="{self.uid_cliente}" xmlns="http://www.asmred.com/">
                          <Envio>
                            <Fecha>{datos_envio["fecha"]}</Fecha>
                            <Servicio>{datos_envio["servicio"]}</Servicio>
                            <Horario>{datos_envio["horario"]}</Horario>
                            <Bultos>{datos_envio["bultos"]}</Bultos>
                            <Peso>{datos_envio["peso"]}</Peso>
                            <Portes>{datos_envio["portes"]}</Portes>
                            <Importes>
                              <Reembolso>{datos_envio["reem"]}</Reembolso>
                            </Importes>
                            <Remite>
                              <Nombre>{datos_envio["nombreOrg"]}</Nombre>
                              <Direccion>{datos_envio["direccionOrg"]}</Direccion>
                              <Poblacion>{datos_envio["poblacionOrg"]}</Poblacion>
                              <Pais>{datos_envio["codPaisOrg"]}</Pais>
                              <CP>{datos_envio["cpOrg"]}</CP>
                            </Remite>
                            <Destinatario>
                              <Nombre>{datos_envio["nombreDst"]}</Nombre>
                              <Direccion>{datos_envio["direccionDst"]}</Direccion>
                              <Poblacion>{datos_envio["poblacionDst"]}</Poblacion>
                              <Pais>{datos_envio["codPaisDst"]}</Pais>
                              <CP>{datos_envio["cpDst"]}</CP>
                              <Telefono>{datos_envio["tfnoDst"]}</Telefono>
                              <Email>{datos_envio["emailDst"]}</Email>
                              <NIF>{datos_envio["nif"]}</NIF>
                              <Observaciones>{datos_envio["observaciones"]}</Observaciones>
                            </Destinatario>
                            <Referencias> 
                              <Referencia tipo="C">{datos_envio["RefC"]}</Referencia>
                            </Referencias>
                            <DevuelveAdicionales>
                                <Etiqueta tipo="PDF"/>
                            </DevuelveAdicionales>
                          </Envio>
                        </Servicios>
                      </docIn>
                    </GrabaServicios>
                  </soap12:Body>
                </soap12:Envelope>
                """
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

        try:
            print("Enviando solicitud a GLS...")
            response = requests.post(
                self.url, data=xml_payload.encode("utf-8"), headers=headers
            )
            response.raise_for_status()
            print("Respuesta recibida con éxito.\n")
            print(response.content)

            # Procesamos la respuesta de la solicitud

            namespaces = {
                "soap": "http://www.w3.org/2003/05/soap-envelope",
                "asm": "http://www.asmred.com/",
            }
            root = ET.fromstring(response.content)
            result_container = root.find(".//asm:GrabaServiciosResult", namespaces)
            if result_container is not None:
                envio_resultado = result_container.find(".//{*}Envio", namespaces)
                if envio_resultado is not None:
                    resultado = envio_resultado.find("{*}Resultado", namespaces).get(
                        "return"
                    )
                    codbarras = envio_resultado.get("codbarras")
                    uid_respuesta = envio_resultado.get("uid")
                    codexp = envio_resultado.get("codexp")

                    # Aqui se puede obtener la etiqueta luego de registrar el envio

                    etiqueta_elemento = envio_resultado.find(".//{*}Etiqueta")
                    etiqueta_base64 = ""

                    if etiqueta_elemento is not None:
                        etiqueta_base64 = etiqueta_elemento.text
                        print("¡Etiqueta encontrada en la respuesta!\n")
                        print(etiqueta_base64)

                        if etiqueta_base64:
                            try:
                                etiqueta_pdf = base64.b64decode(etiqueta_base64)
                                with open("etiqueta.pdf", "wb") as f:
                                    f.write(etiqueta_pdf)
                                print("Etiqueta guardada en etiqueta.pdf")
                            except Exception as e:
                                print(f"Error al decodificar la etiqueta: {e}")

                    referencia_c = ""
                    referencias = envio_resultado.findall(
                        ".//{*}Referencia", namespaces
                    )

                    for ref in referencias:
                        if ref.get("tipo") == "C":
                            referencia_c = ref.text
                            break

                    print("¡Envío procesado correctamente!")
                    data_envio = {
                        "resultado": resultado,
                        "codbarras": codbarras,
                        "uid_respuesta": uid_respuesta,
                        "codexp": codexp,
                        "referencia_c": referencia_c,
                    }
                    return data_envio
                else:
                    error_msg = result_container.findtext(".//asm:Error", namespaces)
                    print(f"Error recibido de GLS: {error_msg}")
                    print(
                        "===================== RESPUESTA COMPLETA DEL SERVIDOR ====================="
                    )
                    print(response.text)
                    print(
                        "==========================================================================="
                    )

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")

        except Exception as e:
            print(f"Error inesperado: {e}")

    def get_etiqueta(self, code: str, tag_type: str):
        """
        Enviamos una solicitud SOAP para obtener una etiqueta de envío.

        Args:
            code (str): La referencia del cliente o el código de barras.
            tag_type (str): El tipo de etiqueta deseado (PDF, ZPL, JPG, PNG, EPL, DPL, XML, EPL_SEPARADO, PDF_SEPARADO).
                                 Se convertirá a mayúsculas antes de ser enviado.

        Returns:
            str: El contenido de la etiqueta codificada en base64, o un mensaje de error.
        """

        tag_type_upper = tag_type.upper()
        xml_payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:asm="http://www.asmred.com/">
<soap:Header/>
<soap:Body>
   <asm:EtiquetaEnvioV2>
      <uidcliente>{self.uid_cliente}</uidcliente>
      <asm:codigo>{code}</asm:codigo>
      <asm:tipoEtiqueta>{tag_type_upper}</asm:tipoEtiqueta>
   </asm:EtiquetaEnvioV2>
</soap:Body>
</soap:Envelope>"""

        headers = {"Content-Type": "text/xml; charset=utf-8"}
        try:
            response = requests.post(
                self.url, data=xml_payload.encode("utf-8"), headers=headers
            )
            response.raise_for_status()
            post_result = response.content
            print(f"Respuesta recibida")
            namespaces = {
                "soap": "http://www.w3.org/2003/05/soap-envelope",
                "ns_asm": "http://www.asmred.com/",
            }
            root = ET.fromstring(post_result)
            etiqueta_envio_v2_response = root.find(
                f".//{{{namespaces['ns_asm']}}}EtiquetaEnvioV2Response"
            )

            if etiqueta_envio_v2_response is None:
                print("No se encontro el elemento EtiquetaEnviaV2")
                return None

            etiqueta_v2_result = etiqueta_envio_v2_response.find(
                f"{{{namespaces['ns_asm']}}}EtiquetaEnvioV2Result"
            )
            if etiqueta_v2_result is None:
                print("Error: No se encontró el elemento EtiquetaEnvioV2Result.")
                return None
            etiquetas_element = etiqueta_v2_result.find("Etiquetas")
            if etiquetas_element is None:
                print("No se encontraron etiquetas dentro de EtiquetaEnvioV2Result.")
                return None

            etiqueta_content_element = etiquetas_element.find("Etiqueta")

            if etiqueta_content_element is not None:
                etiqueta_base64_data = etiqueta_content_element.text
                if etiqueta_base64_data:
                    print(
                        f"\n--- Contenido de la Etiqueta (Base64, primeros 100 caracteres) ---\n{etiqueta_base64_data}"
                    )
                    try:
                        etiqueta_decode_data = base64.b64decode(etiqueta_base64_data)
                        file_name = f"etiqueta_{code}_{tag_type_upper}.epl"
                        with open(file_name, "wb") as f:
                            f.write(etiqueta_decode_data)

                        return etiqueta_base64_data
                    except Exception as e:
                        print(f"Error al decodificar la etiqueta: {e}")
                        return None
                else:
                    print("El elemento <Etiqueta> se encontró, pero está vacío.")
                    return None
            else:
                print(
                    "No se encontró el elemento Etiqueta. La referencia podría ser inválida o el envío ya fue entregado."
                )
                return None

        except requests.exceptions.HTTPError as e:

            print(
                f"Error HTTP al llamar al WS de GLS: {e.response.status_code} - {e.response.text}"
            )

            return None

        except requests.exceptions.ConnectionError as e:

            print(f"Error de conexión al llamar al WS de GLS: {e}")

            return None

        except requests.exceptions.Timeout as e:

            print(f"Tiempo de espera agotado al llamar al WS de GLS: {e}")

            return None

        except ET.ParseError as e:

            print(f"Error al parsear el XML de respuesta: {e}")

            return None

        except Exception as e:

            print(f"Error inesperado: {e}")

            return None

    def get_expedition(self, referencia: str):
        """
        Obtenemos la informacion de un envio

        Args:
            referencia (str): La referencia del cliente del envío a buscar o codigo de barras

        Returns:
            dict: Un diccionario con los datos del envío
        """

        # URL del servicio GLS para este método
        url_wsdl = "https://wsclientes.asmred.com/b2b.asmx"

        # Construir el XML de la solicitud SOAP para GetExpCli
        xml_payload = f"""<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetExpCli xmlns="http://www.asmred.com/">
      <codigo>{referencia}</codigo>
      <uid>{self.uid_cliente}</uid>
    </GetExpCli>
  </soap12:Body>
</soap12:Envelope>"""

        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

        print(f"Enviando solicitud GetExpCli para la referencia: {referencia}")
        try:
            response = requests.post(
                url_wsdl, data=xml_payload.encode("utf-8"), headers=headers
            )
            response.raise_for_status()

            # print(f"Respuesta recibida:\n{response.text}")

            namespace_gls_uri = "http://www.asmred.com/"

            root = ET.fromstring(response.content)

            response_element = root.find(f".//{{{namespace_gls_uri}}}GetExpCliResponse")
            if response_element is None:
                print("Error: No se encontró el elemento GetExpCliResponse.")
                return None

            # Dentro de GetExpCliResponse, buscar GetExpCliResult
            result_element = response_element.find(
                f"{{{namespace_gls_uri}}}GetExpCliResult"
            )
            if result_element is None:
                print("Error: No se encontró el elemento GetExpCliResult.")
                return None

            # Encontrar el elemento 'exp' (expedición) dentro de expediciones
            expeditions = result_element.findall(".//exp")

            if not expeditions:
                print(f"No se encontró ningún envío con la referencia: {referencia}")
                return None

            expeditions_list = []
            for exp in expeditions:
                expedicion_data = {
                    "expedicion": exp.findtext("expedicion"),
                    "albaran": exp.findtext("albaran"),
                    "codexp": exp.findtext("codexp"),
                    "codbar": exp.findtext("codbar"),
                    "uidExp": exp.findtext("uidExp"),
                    "codplaza_cli": exp.findtext("codplaza_cli"),
                    "codcli": exp.findtext("codcli"),
                    "nmCliente": exp.findtext("nmCliente"),
                    "fecha": exp.findtext("fecha"),
                    "FPEntrega": exp.findtext("FPEntrega"),
                    "nombre_org": exp.findtext("nombre_org"),
                    "nif_org": exp.findtext("nif_org"),
                    "calle_org": exp.findtext("calle_org"),
                    "localidad_org": exp.findtext("localidad_org"),
                    "cp_org": exp.findtext("cp_org"),
                    "tfno_org": exp.findtext("tfno_org"),
                    "departamento_org": exp.findtext("departamento_org"),
                    "codpais_org": exp.findtext("codpais_org"),
                    "nombre_dst": exp.findtext("nombre_dst"),
                    "nif_dst": exp.findtext("nif_dst"),
                    "calle_dst": exp.findtext("calle_dst"),
                    "localidad_dst": exp.findtext("localidad_dst"),
                    "cp_dst": exp.findtext("cp_dst"),
                    "tfno_dst": exp.findtext("tfno_dst"),
                    "departamento_dst": exp.findtext("departamento_dst"),
                    "codpais_dst": exp.findtext("codpais_dst"),
                    "codServicio": exp.findtext("codServicio"),
                    "codHorario": exp.findtext("codHorario"),
                    "servicio": exp.findtext("servicio"),
                    "horario": exp.findtext("horario"),
                    "tipo_portes": exp.findtext("tipo_portes"),
                    "bultos": exp.findtext("bultos"),
                    "kgs": exp.findtext("kgs"),
                    "vol": exp.findtext("vol"),
                    "kgsvol_cli": exp.findtext("kgsvol_cli"),
                    "Observacion": exp.findtext("Observacion"),
                    "dac": exp.findtext("dac"),
                    "retorno": exp.findtext("retorno"),
                    "borrado": exp.findtext("borrado"),
                    "codestado": exp.findtext("codestado"),
                    "estado": exp.findtext("estado"),
                    "incidencia": exp.findtext("incidencia"),
                    "tracking": [],
                    "digitalizaciones": [],
                }

                tracking_list = exp.findall(".//tracking")
                for trk in tracking_list:
                    expedicion_data["tracking"].append(
                        {
                            "fecha": trk.findtext("fecha"),
                            "tipo": trk.findtext("tipo"),
                            "codigo": trk.findtext("codigo"),
                            "evento": trk.findtext("evento"),
                            "plaza": trk.findtext("plaza"),
                            "nombreplaza": trk.findtext("nombreplaza"),
                        }
                    )

                digitalizaciones_list = exp.findall(".//digitalizacion")
                for dig in digitalizaciones_list:
                    expedicion_data["digitalizaciones"].append(
                        {
                            "fecha": dig.findtext("fecha"),
                            "codtipo": dig.findtext("codtipo"),
                            "tipo": dig.findtext("tipo"),
                            "imagen": dig.findtext("imagen"),
                            "observaciones": dig.findtext("observaciones"),
                        }
                    )

                expeditions_list.append(expedicion_data)

            print(
                f"Se encontraron {len(expeditions_list)} envíos con la referencia: {referencia}"
            )
            print(expedicion_data)
            return expeditions_list

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return None
        except ET.ParseError as e:
            print(f"Error al parsear el XML de respuesta: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None


api_gls = GlsApi(uid_cliente)
datos_para_un_envio = {
    "fecha": "01/08/2025",
    "servicio": "96",
    "horario": "18",
    "bultos": "1",
    "peso": "1",
    "reem": "0",
    "nombreOrg": "Mi Tienda Online",
    "direccionOrg": "Calle Falsa 123",
    "poblacionOrg": "Springfield",
    "codPaisOrg": "ES",
    "cpOrg": "08100",
    "nombreDst": "Comprador Final",
    "direccionDst": "Avenida Siempre Viva 742",
    "poblacionDst": "Madrid",
    "codPaisDst": "ES",
    "cpDst": "28004",
    "tfnoDst": "912345678",
    "emailDst": "comprador@email.com",
    "observaciones": "Dejar en conserjería si no estoy.",
    "nif": "12345678Z",
    "portes": "P",
    "RefC": "982154321",
}


# api_gls.guardar_envio(datos_para_un_envio)

# api_gls.get_etiqueta("61771242432106001", "epl")
api_gls.get_expedition("61771242432106001")
