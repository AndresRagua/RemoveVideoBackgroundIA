import os
import numpy as np
import cv2
from tqdm import tqdm
import tensorflow as tf
from concurrent.futures import ThreadPoolExecutor

# Definir el tamaño de las imágenes para la entrada del modelo
H = 512
W = 512

def process_frame(frame, model, W, H, w, h):
    """
    Procesa un solo frame de video utilizando el modelo de segmentación para eliminar el fondo.
    
    Parámetros:
    - frame: el frame del video a procesar.
    - model: el modelo de segmentación.
    - W, H: dimensiones de entrada del modelo.
    - w, h: dimensiones originales del frame.

    Retorna:
    - final_frame: el frame procesado con el fondo eliminado y reemplazado por un color específico.
    """
    ori_frame = frame  # Guardar el frame original
    frame = cv2.resize(frame, (W, H))  # Redimensionar el frame al tamaño de entrada del modelo
    frame = np.expand_dims(frame, axis=0)  # Añadir una dimensión para el batch (1, H, W, 3)
    frame = frame / 255.0  # Normalizar los valores de los píxeles a [0, 1]

    # Predecir la máscara utilizando el modelo
    mask = model.predict(frame, verbose=0)[0][:, :, -1]
    mask = cv2.resize(mask, (w, h))  # Redimensionar la máscara al tamaño original del frame
    mask = mask.astype(np.float32)
    mask = np.expand_dims(mask, axis=-1)  # Añadir una dimensión para canales (h, w, 1)

    # Crear las máscaras de foto y fondo
    photo_mask = mask
    background_mask = np.abs(1 - mask)  # Invertir la máscara
    masked_frame = ori_frame * photo_mask  # Aplicar la máscara de foto al frame original

    # Crear la máscara de fondo con un color específico (magenta)
    background_mask = np.concatenate([background_mask, background_mask, background_mask], axis=-1)  # Convertir a 3 canales
    background_mask = background_mask * [255, 0, 255]  # Asignar el color magenta al fondo
    final_frame = masked_frame + background_mask  # Combinar la máscara de foto con la de fondo
    final_frame = final_frame.astype(np.uint8)  # Convertir a entero de 8 bits

    return final_frame  # Retornar el frame final procesado

def process_video(video_path, video_name, model_path, output_folder):
    """
    Procesa un video completo eliminando el fondo de cada frame utilizando un modelo de segmentación.

    Parámetros:
    - video_path: la ruta del video a procesar.
    - video_name: el nombre del video.
    - model_path: la ruta del modelo de segmentación guardado.
    - output_folder: la carpeta donde se guardarán los videos procesados.

    Retorna:
    - output_filename_mp4, output_filename_webm: los nombres de los archivos de video procesados.
    """
    # Verificar si la ruta del video existe
    if not os.path.exists(video_path):
        print(f"Video path {video_path} does not exist.")
        return None

    # Cargar el modelo de segmentación
    model = tf.keras.models.load_model(model_path)

    # Leer los frames del video
    vs = cv2.VideoCapture(video_path)
    if not vs.isOpened():
        print(f"Error opening video stream or file: {video_path}")
        return None

    ret, frame = vs.read()
    if not ret:
        print(f"Failed to read the first frame from {video_path}")
        vs.release()
        return None

    # Obtener las dimensiones del frame
    h, w, _ = frame.shape
    vs.release()

    # Configurar los escritores de video para los formatos MP4 y WebM
    fourcc_mp4 = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc_webm = cv2.VideoWriter_fourcc(*'vp80')
    output_filename_mp4 = f'{video_name.split(".")[0]}_output.mp4'
    output_filename_webm = f'{video_name.split(".")[0]}_output.webm'
    output_filepath_mp4 = os.path.join(output_folder, output_filename_mp4)
    output_filepath_webm = os.path.join(output_folder, output_filename_webm)

    out_mp4 = cv2.VideoWriter(output_filepath_mp4, fourcc_mp4, 30, (w, h), True)
    out_webm = cv2.VideoWriter(output_filepath_webm, fourcc_webm, 30, (w, h), True)

    cap = cv2.VideoCapture(video_path)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Procesar cada frame en paralelo utilizando un pool de hilos
            future = executor.submit(process_frame, frame, model, W, H, w, h)
            futures.append(future)

        # Escribir los frames procesados en los archivos de salida
        for future in tqdm(futures, total=len(futures)):
            final_frame = future.result()
            out_mp4.write(final_frame)
            out_webm.write(final_frame)

    cap.release()
    out_mp4.release()
    out_webm.release()

    print("Completed!")
    return output_filename_mp4, output_filename_webm
