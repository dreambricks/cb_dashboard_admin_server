from flask import Blueprint, render_template, current_app, request, url_for, jsonify, send_from_directory
import os

word_selection_bp = Blueprint('word_selection', __name__)

@word_selection_bp.route('/download-word-csv/<filename>')
def download_word_csv(filename):
    folder_path = current_app.config['WORD_CSV_FOLDER_OUT']
    return send_from_directory(folder_path, filename, as_attachment=True)

@word_selection_bp.route('/word-selection')
def index():
    folder_path = current_app.config['WORD_CSV_FOLDER_IN']
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
    return render_template('word-selection.html', csv_path=new_path)


@word_selection_bp.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.get_json()
    csv_content = data.get("csv", "")

    csv_filename = 'words_out.csv'
    folder_path = current_app.config['WORD_CSV_FOLDER_OUT']
    csv_path = os.path.join(folder_path, csv_filename)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)

    download_url = url_for('word_selection.download_word_csv', filename=csv_filename, _external=True)
    return jsonify({'download_url': download_url})
