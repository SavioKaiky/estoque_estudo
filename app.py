"""
app.py
=======
Entry point da aplicação. Apenas inicializa extensões e registra blueprints.
Nenhuma lógica de negócio aqui.
"""

from flask import Flask, render_template
from config import Config
from database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Importa todos os models dentro do app context para o SQLAlchemy
    # resolver todos os db.relationship() antes de qualquer query.
    with app.app_context():
        import models  # noqa: F401

    from routes.insumos import insumos_bp
    from routes.produtos import produtos_bp
    from routes.producao import producao_bp

    app.register_blueprint(insumos_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(producao_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
