from flask import Blueprint, render_template, current_app, request, url_for, jsonify, send_from_directory
import os

social_selection_bp = Blueprint('social', __name__)

@social_selection_bp.route('/download-social-csv/<filename>')
def download_social_csv(filename):
    folder_path = current_app.config['SOCIAL_CSV_FOLDER_OUT']
    return send_from_directory(folder_path, filename, as_attachment=True)

@social_selection_bp.route('/social-selection')
def social_index():
    folder_path = current_app.config['SOCIAL_CSV_FOLDER_IN']
    csv_filename = None

    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            csv_filename = file
            break

    if csv_filename is None:
        return "No CSV file found in the directory.", 404

    csv_path = os.path.join(folder_path, csv_filename)
    new_path = csv_path.replace("\\", "/")
    print(new_path)
    return render_template('social-selection.html', csv_path=new_path)

@social_selection_bp.route('/save_social_csv', methods=['POST'])
def save_social_csv():
    data = request.get_json()
    csv_content = data.get("csv", "")

    csv_filename = 'social_out.csv'
    folder_path = current_app.config['SOCIAL_CSV_FOLDER_OUT']
    csv_path = os.path.join(folder_path, csv_filename)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)

    download_url = url_for('social.download_social_csv', filename=csv_filename, _external=True)
    return jsonify({'download_url': download_url})
