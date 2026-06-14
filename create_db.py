from app import create_app
from database import db
import models  # noqa: F401 — importa todos via __init__.py

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco criado com sucesso!")