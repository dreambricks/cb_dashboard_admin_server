from random import randint
from flask import Blueprint, render_template, request, current_app, redirect, url_for, jsonify
import os

photo_bp = Blueprint('photo', __name__)


@photo_bp.route('/upload_photo', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':

        if 'files' not in request.files:
            return "Nenhum arquivo encontrado."

        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return "Nenhum arquivo selecionado."

        for filename in os.listdir(current_app.config['PHOTO_FOLDER']):
            if filename.endswith('_ACTIVE.jpg'):
                disabled_filename = filename.replace('_ACTIVE', '_DISABLED')
                os.rename(
                    os.path.join(current_app.config['PHOTO_FOLDER'], filename),
                    os.path.join(current_app.config['PHOTO_FOLDER'], disabled_filename)
                )

        for file in files:
            if file.filename:
                filename = f"{randint(0, 9999999)}_ACTIVE.jpg"
                file_path = os.path.join(current_app.config['PHOTO_FOLDER'], filename)
                file.save(file_path)

        return redirect(url_for('photo.upload_image'))

    active_images = [
        filename for filename in os.listdir(current_app.config['PHOTO_FOLDER'])
        if filename.endswith('_ACTIVE.jpg')
    ]

    return render_template('photo.html', active_images=active_images)


@photo_bp.route('/active_images', methods=['GET'])
def get_active_images():
    upload_folder = current_app.config['PHOTO_FOLDER']

    active_images = [
        url_for('static', filename=f'photos/{filename}', _external=True)
        for filename in os.listdir(upload_folder)
        if filename.endswith('_ACTIVE.jpg')
    ]

    return jsonify(active_images=active_images), 200
