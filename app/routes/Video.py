from flask import Blueprint, request, jsonify, send_from_directory, current_app, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from video import process_video  # Importar la función de procesamiento de video
from app.models.ModelVideo import db, Video  # Importar solo Video
from datetime import datetime
import os

video_bp = Blueprint('video_bp', __name__)

@video_bp.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Crear una entrada en la base de datos para el video subido
        video = Video(input_video_path=filepath)
        db.session.add(video)
        db.session.commit()

        # Process the video
        output_filename_mp4, output_filename_webm = process_video(filepath, filename, current_app.config['MODEL_PATH'], current_app.config['OUTPUT_FOLDER'])
        output_filepath_mp4 = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename_mp4)
        output_filepath_webm = os.path.join(current_app.config['OUTPUT_FOLDER'], output_filename_webm)

        # Actualizar la entrada en la base de datos con el video procesado
        video.output_video_path = output_filepath_mp4
        video.process_time = datetime.utcnow()
        db.session.commit()

        return render_template('download.html', original_filename=filename, processed_filename_webm=output_filename_webm, processed_filename_mp4=output_filename_mp4)

    return render_template('upload.html')

@video_bp.route('/download', methods=['GET'])
def download_video_page():
    original_filename = request.args.get('original_filename')
    processed_filename = request.args.get('processed_filename')
    return render_template('download.html', original_filename=original_filename, processed_filename=processed_filename)

@video_bp.route('/download/video/<filename>', methods=['GET'])
def download_video(filename):
    return send_from_directory(directory=current_app.config['OUTPUT_FOLDER'], filename=filename, as_attachment=True)
