from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, mail, migrate
from flask import Flask, session, request, redirect, url_for

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.admin.routes import admin_bp
    from app.cli import register_cli

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    register_cli(app)

        @app.context_processor
    def inject_language():
        return {
            "lang": session.get("lang", "no")
        }

    @app.route("/set-language/<language>")
    def set_language(language):
        if language not in ["no", "en"]:
            language = "no"

        session["lang"] = language
        return redirect(request.referrer or url_for("main.index"))

    return app
