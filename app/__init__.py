from flask import Flask, render_template
from flask_migrate import Migrate
from config import config
from app.models.ModelVideo import db

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from app.routes.Video import video_bp
        app.register_blueprint(video_bp, url_prefix='/api/video')
        
        # Ruta principal
        @app.route('/')
        def index():
            return render_template('index.html')
        
        return app
