from script_base import run_api
import time

test = {
    "vw": {"Query": "Bomba de agua", "Bastidor": "WVWZZZ3CZHE004123"},
    "SMART": {"Query": "Espejos retrovisores", "Bastidor": "WME4513311K043393"},
    "TOYOTA": {"Query": "Suspension neumatica", "Bastidor": "JTEBZ29J100180316"},
    "OPEL": {"Query": "Anillos de airbag", "Bastidor": "W0LMRF4SEEB062229"},
    "NISSAN": {"Query": "Anillos de airbag", "Bastidor": "SJNFDAE11U1245311"},
    "MITSUBISHI": {"Query": "Kit de distribucion", "Bastidor": "4MBMND32ATE001965"},
    "MINI": {"Query": "Anillos de airbag", "Bastidor": "WMWMF31020TS59066"},
    "MERCEDES": {"Query": "Cerraduras", "Bastidor": "WDB9066131S470300"},
    "MERCEDES": {"Query": "BOTONERAS ELEVALUNAS", "Bastidor": "WDB90166611R885005"},
    "MERCEDES": {"Query": "Bomba de combustible", "Bastidor": "WDD1690061J391970"},
    "LANDROVER": {"Query": "Valvulas egr", "Bastidor": "SALLAAA146A374538"},
    "LANCIA": {"Query": "CUBRE PEDAL", "Bastidor": "ZLA17900013377390"},
    "KIA": {"Query": "Valvulas egr", "Bastidor": "KNEUP751256716941"},
    "HONDA": {"Query": "Arbol de levas", "Bastidor": "SHHEP23701U010050"},
    "FORD": {"Query": "BOMBA DE VACIO", "Bastidor": "WF0XXXTTFX8B77160"},
    "FIAT": {"Query": "intercooler", "Bastidor": "ZFA22300005602670"},
    "FIAT": {"Query": "BOTONERAS ELEVALUNAS", "Bastidor": "ZFA18200005166595"},
}

for make in test:
    print(make, test[make]["Query"], test[make]["Bastidor"])
    run_api(test[make]["Bastidor"], test[make]["Query"], make)
    time.sleep(15)
