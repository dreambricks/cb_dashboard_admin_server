from flask import Blueprint, render_template, current_app, request, url_for, jsonify, send_from_directory
import os

social_selection_bp = Blueprint('social', __name__)

@social_selection_bp.route('/social-selection')
def social_index():
    x_csv_folder_in = current_app.config['X_CSV_FOLDER_IN']
    tiktok_csv_folder_in = current_app.config['TIKTOK_CSV_FOLDER_IN']
    instagram_csv_folder_in = current_app.config['INSTAGRAM_CSV_FOLDER_IN']

    def get_csv_path(folder):
        for file in os.listdir(folder):
            if file.endswith('.csv'):
                return os.path.join(folder, file).replace("\\", "/")
        return None

    x_new_path = get_csv_path(x_csv_folder_in)
    tiktok_new_path = get_csv_path(tiktok_csv_folder_in)
    instagram_new_path = get_csv_path(instagram_csv_folder_in)

    if not x_new_path or not tiktok_new_path or not instagram_new_path:
        return "No CSV file found in one or more directories.", 404

    print(f'x_new_path: {x_new_path}')
    print(f'tiktok_new_path: {tiktok_new_path}')
    print(f'instagram_new_path: {instagram_new_path}')

    return render_template(
        'social-selection.html',
        x_csv_folder_in=x_new_path,
        tiktok_csv_folder_in=tiktok_new_path,
        instagram_csv_folder_in=instagram_new_path
    )


@social_selection_bp.route('/download-social-csv/<platform>/<filename>')
def download_social_csv(platform, filename):
    # Seleciona a pasta de saída com base na plataforma
    if platform == 'x':
        folder_path = current_app.config['X_CSV_FOLDER_OUT']
    elif platform == 'tiktok':
        folder_path = current_app.config['TIKTOK_CSV_FOLDER_OUT']
    elif platform == 'instagram':
        folder_path = current_app.config['INSTAGRAM_CSV_FOLDER_OUT']
    else:
        return "Invalid platform specified.", 400

    return send_from_directory(folder_path, filename, as_attachment=True)


@social_selection_bp.route('/save_social_csv/<platform>', methods=['POST'])
def save_social_csv(platform):
    print(platform)
    data = request.get_json()
    csv_content = data.get("csv", "")

    csv_filename = f'{platform}_out.csv'

    if platform == 'x':
        folder_path = current_app.config['X_CSV_FOLDER_OUT']
    elif platform == 'tiktok':
        folder_path = current_app.config['TIKTOK_CSV_FOLDER_OUT']
    elif platform == 'instagram':
        folder_path = current_app.config['INSTAGRAM_CSV_FOLDER_OUT']
    else:
        return jsonify({"error": "Invalid platform specified"}), 400

    csv_path = os.path.join(folder_path, csv_filename)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)

    download_url = url_for('social.download_social_csv', platform=platform, filename=csv_filename, _external=True)
    return jsonify({'download_url': download_url})
