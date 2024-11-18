from flask import Blueprint, current_app, render_template, request, jsonify, send_from_directory
import os

subtitle_bp = Blueprint('subtitle', __name__)


@subtitle_bp.route('/subtitle', methods=['GET', 'POST'])
def subtitle():
    return render_template('subtitles.html')


@subtitle_bp.route('/dynamic/legendas')
def serve_subtitles():
    subtitles_folder_path = current_app.config['SUBTITLES_FOLDER']
    subtitles_tsv_filename = None

    for file in os.listdir(subtitles_folder_path):
        if file.endswith('.tsv'):
            subtitles_tsv_filename = file
            break

    if subtitles_tsv_filename is None:
        return "No TSV file found in the directory.", 404

    return send_from_directory(subtitles_folder_path, subtitles_tsv_filename)



@subtitle_bp.route('/save_subtitle', methods=['POST'])
def save_tsv():
    try:
        # Valida se o JSON recebido contém a chave 'tsv'
        data = request.json.get('tsv')
        if not data:
            return jsonify({"error": "No TSV data provided."}), 400

        # Obtém o caminho da pasta onde os arquivos de legenda estão localizados
        subtitles_folder_path = current_app.config['SUBTITLES_FOLDER']
        subtitles_tsv_filename = None

        # Encontra o primeiro arquivo .tsv na pasta
        for file in os.listdir(subtitles_folder_path):
            if file.endswith('.tsv'):
                subtitles_tsv_filename = file
                break

        if subtitles_tsv_filename is None:
            return jsonify({"error": "No TSV file found in the subtitles folder."}), 404

        subtitles_tsv_path = os.path.join(subtitles_folder_path, subtitles_tsv_filename)

        # Tenta escrever os dados no arquivo
        with open(subtitles_tsv_path, 'w', encoding='utf-8') as file:
            file.write(data)

        return jsonify({"message": "File saved successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



