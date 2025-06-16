import logging
import azure.functions as func
import io
from moviepy.editor import ImageSequenceClip
import numpy as np
from PIL import Image
from ..shared_code import blob_helpers
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função "CriarSlideshow" acionada.')

    try:
        files = req.files.getlist('images')
        duration = float(req.form.get('duration', 2.0)) # Duração de cada imagem

        if not files:
            return func.HttpResponse('{"error": "Nenhuma imagem enviada."}', status_code=400, mimetype="application/json")
        
        image_frames = []
        for file in files:
            # Converte cada imagem para um array numpy, que o moviepy usa
            img = Image.open(io.BytesIO(file.read())).convert("RGB")
            image_frames.append(np.array(img))

        # Cria o clipe de vídeo com as imagens, definindo a duração de cada frame
        clip = ImageSequenceClip(image_frames, durations=[duration] * len(image_frames))
        
        output_filename_temp = "temp_video.mp4"
        # Escreve o vídeo em um arquivo temporário (moviepy precisa de um caminho de arquivo)
        # codec e áudio podem ser ajustados conforme necessidade
        clip.write_videofile(f"/tmp/{output_filename_temp}", codec="libx264", fps=24, audio=False)

        # Lê o arquivo de vídeo gerado para fazer upload
        with open(f"/tmp/{output_filename_temp}", "rb") as f:
            video_bytes = f.read()

        new_filename = f"slideshow_{int(time.time())}.mp4"
        download_url = blob_helpers.upload_to_blob(
            'generated-videos', new_filename, video_bytes, return_url=True
        )

        return func.HttpResponse(f'{{"download_url": "{download_url}"}}', mimetype="application/json")

    except Exception as e:
        logging.error(f"Erro em CriarSlideshow: {e}")
        return func.HttpResponse('{"error": "Erro interno no servidor ao criar o slideshow."}', status_code=500, mimetype="application/json")