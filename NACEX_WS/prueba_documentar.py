from nacex_api import documentar_nacex

#documentar_nacex(nom_ent, dir_ent, cp_ent, pob_ent, pais_ent, tel_ent, reembolso, ret, obs1, impresora=r"\\\\192.168.3.169\\nacex")

resultado = documentar_nacex(
    nom_ent="Prueba Api 02072025",
    dir_ent="Calle Ejemplo 123",
    cp_ent="29010",
    pob_ent="MALAGA",
    pais_ent="ES",
    tel_ent="600112233",
    reembolso=29.99,
    ret="N",
    obs1="BOX-100 - COAD-010",
)

if resultado["OK"]:
    print("✅ Envío documentado correctamente:")
    print(f"Albarán: {resultado['albaran']}")
    print(f"Link: {resultado['link']}")
    print(f"Etiqueta guardada en: {resultado['etiqueta_path']}")
else:
    print("❌ Fallo al documentar el envío:")
    print(resultado.get("error"))