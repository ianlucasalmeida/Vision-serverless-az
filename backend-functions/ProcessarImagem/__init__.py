import logging
import azure.functions as func
from PIL import Image, ImageOps
import io
from ..shared_code import blob_helpers
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função "ProcessarImagem" acionada.')

    try:
        action = req.form.get('action')
        file = req.files.get('file')

        if not action or not file:
            return func.HttpResponse('{"error": "Ação e arquivo são obrigatórios."}', status_code=400, mimetype="application/json")

        original_filename = file.filename
        file_bytes = file.read()

        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

        if action == 'bw':
            processed_image = ImageOps.grayscale(image)
        elif action == 'sepia':
            # Cria um filtro Sépia
            sepia_filter = Image.new('RGB', image.size)
            for i in range(image.width):
                for j in range(image.height):
                    r, g, b = image.getpixel((i, j))
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    sepia_filter.putpixel((i, j), (min(255, tr), min(255, tg), min(255, tb)))
            processed_image = sepia_filter
        else:
            return func.HttpResponse('{"error": "Ação desconhecida."}', status_code=400, mimetype="application/json")

        output_stream = io.BytesIO()
        processed_image.save(output_stream, format='PNG')
        output_stream.seek(0)

        new_filename = f"{action}_{int(time.time())}_{original_filename}.png"
        
        download_url = blob_helpers.upload_to_blob(
            'converted-images', new_filename, output_stream.getvalue(), return_url=True
        )

        return func.HttpResponse(f'{{"download_url": "{download_url}"}}', mimetype="application/json")

    except Exception as e:
        logging.error(f"Erro em ProcessarImagem: {e}")
        return func.HttpResponse('{"error": "Erro interno no servidor ao processar a imagem."}', status_code=500, mimetype="application/json")