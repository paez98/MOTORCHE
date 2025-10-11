from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import time  # Importar la librería time para usar time.sleep()


def get_barcoder_from_frame(frame):
    """
    Adapta tu función original para trabajar con un frame de OpenCV.
    Procesa un frame de imagen (arreglo NumPy) para decodificar códigos de barras.
    """
    try:
        # OpenCV lee las imágenes como arreglos NumPy en formato BGR.
        # Pillow (PIL) espera imágenes en formato RGB, así que convertimos.
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image_rgb)

        code_match = decode(image)

        if not code_match:
            # print('No se encontraron codigos en este frame')
            return []

        resultados = []

        for codigo in code_match:
            data_decodificada = codigo.data.decode("utf-8")
            tipo_codigo = codigo.type
            print(f"  Tipo: {tipo_codigo}")
            print(f"  Datos: {data_decodificada}")

            resultados.append({"tipo": tipo_codigo, "datos": data_decodificada})
        return resultados
    except Exception as e:
        print(f"Ocurrió un error al procesar el frame: {e}")
        return []


def read_barcode_from_usb_phone_camera():
    """
    Lee el stream de video de la cámara web (iVCam o similar)
    y busca códigos de barras en tiempo real, con una pausa después de la detección.
    """
    # cv2.VideoCapture(0) intenta abrir la primera cámara detectada en tu sistema.
    # Si tienes otras cámaras (webcam integrada, etc.), iVCam podría ser 1, 2, etc.
    # Si 0 no funciona, prueba con 1, 2, 3...
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        print("Asegúrate de que iVCam Client esté ejecutándose en tu PC.")
        print(
            "Asegúrate de que iVCam App esté ejecutándose en tu teléfono y conectado."
        )
        print(
            "Prueba cambiando el índice de la cámara en 'cv2.VideoCapture(0)' a 1, 2, etc."
        )
        return

    # --- Configuración de Resolución (Opcional, para mejorar la calidad si es necesario) ---
    # Define la resolución deseada. Prueba con resoluciones comunes.
    # iVCam debería ser compatible con resoluciones más altas en su versión gratuita o con una configuración adecuada.
    desired_width = 1280
    desired_height = 720

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(
        f"Resolución de la cámara (Solicitada: {desired_width}x{desired_height}, Real: {actual_width}x{actual_height})"
    )

    print("Cámara detectada. Escaneando códigos de barras... (Presiona 'q' para salir)")

    barcode_detected_time = 0  # Variable para registrar el último tiempo de detección

    while True:
        ret, frame = cap.read()

        if not ret:
            print("No se pudo recibir un frame. Saliendo...")
            break

        # Verifica si ha pasado suficiente tiempo desde la última detección
        # Si barcode_detected_time es 0 (primera vez) o si han pasado más de 5 segundos
        if time.time() - barcode_detected_time > 5:  # Pausa de 5 segundos
            resultados = get_barcoder_from_frame(frame)

            if resultados:
                # Si se encuentra un código, actualiza el tiempo de la última detección
                barcode_detected_time = time.time()
                # Aquí puedes agregar la lógica para guardar el código, etc.
                # También podrías emitir un sonido o vibrar el teléfono si es posible
                # para indicar una lectura exitosa.
                print(
                    "--- Código de barras leído. Esperando 5 segundos antes de escanear de nuevo ---"
                )

        # Muestra el frame en una ventana
        cv2.imshow('Barcode Scanner (Press "q" to quit)', frame)

        # Espera 1 milisegundo por una tecla. Si la tecla 'q' es presionada, sale del bucle.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    read_barcode_from_usb_phone_camera()
