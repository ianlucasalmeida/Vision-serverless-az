# Nota: A conversão DOCX para PDF em um ambiente Linux (padrão do Azure Functions)
# pode ser complexa e exigir dependências como LibreOffice.
# Este é um exemplo simplificado. Para produção, considere usar uma API de terceiros ou um contêiner customizado.
# Abaixo, um exemplo de "unir PDFs" que é mais direto.

import logging
import azure.functions as func
import io
from PyPDF2 import PdfMerger
from ..shared_code import blob_helpers
import time

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Função "ProcessarPDF" acionada.')
    
    action = req.form.get('action')
    if action == 'merge':
        files = req.files.getlist('files')
        if not files or len(files) < 2:
            return func.HttpResponse('{"error": "São necessários pelo menos 2 arquivos para unir."}', status_code=400, mimetype="application/json")
        
        merger = PdfMerger()
        for pdf_file in files:
            merger.append(io.BytesIO(pdf_file.read()))

        output_stream = io.BytesIO()
        merger.write(output_stream)
        merger.close()
        output_stream.seek(0)
        
        new_filename = f"merged_{int(time.time())}.pdf"
        download_url = blob_helpers.upload_to_blob(
            'converted-pdfs', new_filename, output_stream.getvalue(), return_url=True
        )
        
        return func.HttpResponse(f'{{"download_url": "{download_url}"}}', mimetype="application/json")

    return func.HttpResponse('{"error": "Ação não implementada."}', status_code=400, mimetype="application/json")