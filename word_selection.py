from flask import Blueprint, render_template, current_app, request, url_for, jsonify, send_from_directory, send_file
import os
import config
from word_cloud import generate_wordcloud
from datetime import datetime

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


@word_selection_bp.route('/word_cloud')
def word_cloud():
    folder_path = current_app.config['WORD_TSV_FOLDER_OUT']
    tsv_filename = None

    # Procura por arquivos TSV no diretório
    for file in os.listdir(folder_path):
        if file.endswith('.tsv'):
            tsv_filename = file
            break

    if tsv_filename is None:
        return "No TSV file found in the directory.", 404

    folder_in = os.path.join(folder_path, tsv_filename)

    folder_out = current_app.config['WORD_CLOUD_IMAGE']
    for file in os.listdir(folder_out):
        if file.endswith('_ACTIVE.png'):
            old_path = os.path.join(folder_out, file)
            new_path = os.path.join(folder_out, file.replace('_ACTIVE.png', '_DISABLED.png'))
            os.rename(old_path, new_path)

    # Cria o nome do novo arquivo com timestamp e "_ACTIVE.png"
    time_stamp = datetime.now().strftime("%Y%m%d%H%M")
    filename = f"{time_stamp}_ACTIVE.png"
    img_path = os.path.join(folder_out, filename)

    # Gera e salva a nova imagem de nuvem de palavras
    generate_wordcloud(folder_in, img_path)

    # Retorna o arquivo de imagem diretamente como resposta
    return send_file(img_path, mimetype='image/png')

