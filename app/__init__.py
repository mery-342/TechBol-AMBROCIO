import os
from flask import Flask, render_template
from .extensions import db, migrate

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "techbol-clave"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "techbol.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models  # para que las migraciones detecten los modelos

    from .clientes import bp_clientes
    from .productos import bp_productos
    from .pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix="/clientes")
    app.register_blueprint(bp_productos, url_prefix="/productos")
    app.register_blueprint(bp_pedidos, url_prefix="/pedidos")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app