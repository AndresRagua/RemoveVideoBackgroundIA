from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_video_path = db.Column(db.String(200), nullable=False)
    output_video_path = db.Column(db.String(200))
    upload_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    process_time = db.Column(db.DateTime)

    def __init__(self, input_video_path):
        self.input_video_path = input_video_path
