from flask import Blueprint, render_template, current_app, request, url_for, jsonify, send_from_directory
import os

word_selection_bp = Blueprint('word_selection', __name__)

@word_selection_bp.route('/download-word-tsv/<filename>')
def download_word_tsv(filename):
    folder_path = current_app.config['WORD_TSV_FOLDER_OUT']
    return send_from_directory(folder_path, filename, as_attachment=True)

@word_selection_bp.route('/word-selection')
def index():
    folder_path = current_app.config['WORD_TSV_FOLDER_IN']
    tsv_filename = None

    for file in os.listdir(folder_path):
        if file.endswith('.tsv'):
            tsv_filename = file
            break

    if tsv_filename is None:
        return "No TSV file found in the directory.", 404

    tsv_path = os.path.join(folder_path, tsv_filename)
    new_path = tsv_path.replace("\\", "/")
    print(new_path)
    return render_template('word-selection.html', tsv_path=new_path)

@word_selection_bp.route('/save_tsv', methods=['POST'])
def save_tsv():
    data = request.get_json()
    tsv_content = data.get("tsv", "")

    tsv_filename = 'words_out.tsv'
    folder_path = current_app.config['WORD_TSV_FOLDER_OUT']
    tsv_path = os.path.join(folder_path, tsv_filename)

    with open(tsv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(tsv_content)

    download_url = url_for('word_selection.download_word_tsv', filename=tsv_filename, _external=True)
    return jsonify({'download_url': download_url})
