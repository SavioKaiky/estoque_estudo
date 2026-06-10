from flask import Flask
from config import Config
from database import db
from flask import render_template


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from routes.insumos import insumos_bp
    from routes.produtos2 import produtos_bp
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
    app.run(debug=False)