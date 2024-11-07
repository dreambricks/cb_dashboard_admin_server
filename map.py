from flask import Blueprint, render_template, request, current_app, redirect, url_for, jsonify, send_from_directory, \
    abort, Response
import os
import config

map_bp = Blueprint('map', __name__)


@map_bp.route('/map')
def index():
    folder_path = current_app.config['MAP_TSV_FOLDER_IN']
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

    return render_template('map.html', tsv_file=new_path, map_edited=config.MAP_EDITED)


@map_bp.route('/save_table', methods=['POST'])
def salvar_tabela():
    try:
        data = request.json
        if not data or 'table' not in data:
            return jsonify({'error': 'Dados da tabela ausentes'}), 400

        output_path = os.path.join(current_app.config['MAP_TSV_FOLDER_EDITED'], 'map_tsv_edited.tsv')

        with open(output_path, 'w', encoding='utf-8') as file:
            for row in data['table']:
                file.write('\t'.join(row) + '\n')

        return jsonify({'message': 'Tabela salva com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@map_bp.route('/toggle_map_edited', methods=['POST'])
def toggle_map_edited():
    data = request.get_json()
    if 'mapEdited' in data:
        new_value = data['mapEdited']

        try:
            with open('config.py', 'r') as file:
                config_content = file.readlines()
        except FileNotFoundError:
            return jsonify({'error': 'Arquivo config.py não encontrado'}), 500

        updated = False
        for i, line in enumerate(config_content):
            if line.startswith('MAP_EDITED'):
                config_content[i] = f'MAP_EDITED = {new_value}\n'
                updated = True
                break

        if not updated:
            config_content.append(f'MAP_EDITED = {new_value}\n')

        try:
            with open('config.py', 'w') as file:
                file.writelines(config_content)
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar config.py: {str(e)}'}), 500

        return jsonify({'message': 'MAP_EDITED atualizado com sucesso!'})
    return jsonify({'error': 'Dados inválidos'}), 400


@map_bp.route('/download_map_link')
def download_map_link():
    if config.MAP_EDITED:
        filename = 'map_tsv_in.tsv'
    else:
        filename = 'map_tsv_edited.tsv'

    download_url = url_for('map.download_file', filename=filename, _external=True)

    return jsonify({"download_url": download_url})


@map_bp.route('/download_map/<filename>')
def download_file(filename):
    if config.MAP_EDITED:
        folder_path = config.MAP_TSV_FOLDER_EDITED
    else:
        folder_path = config.MAP_TSV_FOLDER_IN

    return send_from_directory(directory=folder_path, path=filename, as_attachment=True)

@map_bp.route('/get-map-tsv', methods=['GET'])
def get_first_tsv_file():
    if config.MAP_EDITED:
        folder_path = config.MAP_TSV_FOLDER_EDITED
    else:
        folder_path = config.MAP_TSV_FOLDER_IN

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(folder_path)
        abort(404, description="Pasta não encontrada ou caminho inválido.")

    for filename in os.listdir(folder_path):
        if filename.endswith('.tsv'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            response = Response(content, content_type='text/plain')

            return response

    abort(404, description="Nenhum arquivo .tsv encontrado na pasta.")
