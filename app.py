import os
from flask import Flask, render_template, abort, send_file
import markdown

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICES_DIR = os.path.join(BASE_DIR, "services")


def list_services():
    """Ritorna la lista delle cartelle dentro services/."""
    if not os.path.exists(SERVICES_DIR):
        return []
    return [
        name for name in os.listdir(SERVICES_DIR)
        if os.path.isdir(os.path.join(SERVICES_DIR, name))
    ]


def get_service_image(service_name):
    """Ritorna il percorso dell'immagine PNG se esiste, altrimenti None."""
    image_path = os.path.join(SERVICES_DIR, service_name, f"{service_name}.png")
    if os.path.exists(image_path):
        return f"/services/{service_name}/{service_name}.png"
    return None


@app.route("/")
def index():
    services = list_services()
    # Crea una lista di tuple (nome, immagine_url) per ogni servizio
    services_with_images = [
        (s, get_service_image(s)) for s in services
    ]
    return render_template("index.html", services_with_images=services_with_images)


@app.route("/service/<service_name>")
def service_page(service_name):
    service_path = os.path.join(SERVICES_DIR, service_name)
    readme_path = os.path.join(service_path, "readme.md")

    if not os.path.exists(readme_path):
        abort(404)

    with open(readme_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=["fenced_code"])

    return render_template("service.html", service_name=service_name, content=html_content)


@app.route("/services/<service_name>/<filename>")
def serve_service_file(service_name, filename):
    """Serve static files from service directories."""
    service_path = os.path.join(SERVICES_DIR, service_name)
    if not os.path.exists(service_path):
        abort(404)
    
    file_path = os.path.join(service_path, filename)
    # Security check to prevent directory traversal
    if not os.path.abspath(file_path).startswith(os.path.abspath(service_path)):
        abort(403)
    
    if not os.path.exists(file_path):
        abort(404)
    
    return send_file(file_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
