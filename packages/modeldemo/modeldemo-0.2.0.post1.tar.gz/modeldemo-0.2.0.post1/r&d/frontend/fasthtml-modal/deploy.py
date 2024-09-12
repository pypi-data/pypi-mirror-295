from app import fasthtml_app
from modal import App, Image, asgi_app

image = Image.debian_slim(python_version="3.11").pip_install("python-fasthtml")

app = App("fasthtml-modal-template")


@app.function(image=image)
@asgi_app()
def get():
    return fasthtml_app
