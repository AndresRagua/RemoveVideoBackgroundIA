from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .video import views as video_views
        app.register_blueprint(video_views.main, url_prefix='/api/video')

        return app
