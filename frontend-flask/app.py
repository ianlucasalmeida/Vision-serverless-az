from flask import Flask, render_template
import os

app = Flask(__name__)

# Recomenda-se obter as URLs das Funções a partir de variáveis de ambiente
# Para facilitar, vamos defini-las aqui, mas lembre-se de substituí-las.
FUNCTION_URLS = {
    "image": os.environ.get("IMAGE_FUNCTION_URL", "URL_DA_FUNCAO_DE_IMAGEM"),
    "pdf": os.environ.get("PDF_FUNCTION_URL", "URL_DA_FUNCAO_DE_PDF"),
    "video": os.environ.get("VIDEO_FUNCTION_URL", "URL_DA_FUNCAO_DE_VIDEO"),
    "slideshow": os.environ.get("SLIDESHOW_FUNCTION_URL", "URL_DA_FUNCAO_DE_SLIDESHOW")
}

@app.route('/')
def index():
    """Página inicial com links para as ferramentas."""
    return render_template('index.html')

@app.route('/image-converter')
def image_converter():
    """Página para conversão de imagens."""
    return render_template('image_converter.html', function_url=FUNCTION_URLS["image"])

@app.route('/pdf-tools')
def pdf_tools():
    """Página para as ferramentas de PDF."""
    return render_template('pdf_tools.html', function_url=FUNCTION_URLS["pdf"])

@app.route('/video-converter')
def video_converter():
    """Página para conversão de vídeo."""
    return render_template('video_converter.html', function_url=FUNCTION_URLS["video"])

@app.route('/slideshow-creator')
def slideshow_creator():
    """Página para criação de slideshows."""
    return render_template('slideshow_creator.html', function_url=FUNCTION_URLS["slideshow"])

if __name__ == '__main__':
    app.run(debug=True)