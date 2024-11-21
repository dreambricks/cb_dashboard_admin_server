from flask import Blueprint, current_app, render_template, request, jsonify, url_for, send_from_directory, abort, \
    Response
import os
import config
import shutil

top_products_bp = Blueprint('top_products', __name__)


@top_products_bp.route('/top-products')
def index():
    folder_path = current_app.config['TOP_PRODUCTS_FOLDER_IN']
    folder_path_edited = current_app.config.get('TOP_REQUESTS')

    def get_tsv_path(folder):
        for file in os.listdir(folder):
            if file.endswith('.tsv'):
                return os.path.join(folder, file).replace("\\", "/")
        return None

    tsv_path = get_tsv_path(folder_path)
    tsv_path_edited = get_tsv_path(folder_path_edited)

    if not tsv_path:
        return "No TSV file found in the input directory.", 404

    config_path = os.path.join(current_app.root_path, 'config.py')
    product_edited = None
    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('PRODUCT_EDITED'):
                value = line.split('=')[1].strip().strip('"').strip("'")
                product_edited = value.lower() == 'true'
                break

    if product_edited is None:
        return "PRODUCT_EDITED not found in config.py", 500

    print(f"Original TSV Path: {tsv_path}")
    if tsv_path_edited:
        print(f"Edited TSV Path: {tsv_path_edited}")

    return render_template(
        'top-products.html',
        tsv_path=tsv_path,
        tsv_file_edited=tsv_path_edited,
        product_edited=product_edited
    )


@top_products_bp.route('/save-edited-top-products', methods=['POST'])
def save_edited_products():
    data = request.json.get('data')
    if data:
        output_path = os.path.join(current_app.config['TOP_REQUESTS'], 'top_product_edited.tsv')
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(data)
            return jsonify({"message": "File saved successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No data provided"}), 400


@top_products_bp.route('/toggle_product_edited', methods=['POST'])
def toggle_map_edited():
    data = request.get_json()
    if 'productEdited' in data:
        new_value = data['productEdited']

        try:
            with open('config.py', 'r') as file:
                config_content = file.readlines()
        except FileNotFoundError:
            return jsonify({'error': 'Arquivo config.py não encontrado'}), 500

        updated = False
        for i, line in enumerate(config_content):
            if line.startswith('PRODUCT_EDITED'):
                config_content[i] = f'PRODUCT_EDITED = {new_value}\n'
                updated = True
                break

        if not updated:
            config_content.append(f'PRODUCT_EDITED = {new_value}\n')

        try:
            with open('config.py', 'w') as file:
                file.writelines(config_content)
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar config.py: {str(e)}'}), 500

        return jsonify({'message': 'PRODUCT_EDITED atualizado com sucesso!'})
    return jsonify({'error': 'Dados inválidos'}), 400


@top_products_bp.route('/download_top_products_link')
def download_map_link():
    if config.PRODUCT_EDITED:
        filename = 'top_product_edited.tsv'
    else:
        filename = 'top_products.tsv'

    download_url = url_for('top_products.download_file', filename=filename, _external=True)

    return jsonify({"download_url": download_url})


@top_products_bp.route('/download_top_products/<filename>')
def download_file(filename):
    if config.PRODUCT_EDITED:
        folder_path = config.TOP_REQUESTS
    else:
        folder_path = config.TOP_PRODUCTS_FOLDER_IN
    print(folder_path)

    return send_from_directory(directory=folder_path, path=filename, as_attachment=True)


@top_products_bp.route('/get-top-product-tsv', methods=['GET'])
def get_first_tsv_file():

    config_path = os.path.join(current_app.root_path, 'config.py')
    product_edited = None
    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('PRODUCT_EDITED'):
                value = line.split('=')[1].strip().strip('"').strip("'")
                product_edited = value.lower() == 'true'
                break

    if product_edited is None:
        return "PRODUCT_EDITED not found in config.py", 500

    if product_edited:
        folder_path = config.TOP_REQUESTS
    else:
        folder_path = config.TOP_PRODUCTS_FOLDER_IN

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(folder_path)
        abort(404, description="Pasta não encontrada ou caminho inválido.")

    for filename in os.listdir(folder_path):
        if filename.endswith('.tsv'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            response = Response(content, content_type='text/plain; charset=utf-8')

            return response

    abort(404, description="Nenhum arquivo .tsv encontrado na pasta.")


@top_products_bp.route('/reset_top_products_table', methods=['POST'])
def reset_table():
    try:
        source_folder = config.TOP_PRODUCTS_FOLDER_IN
        target_file = os.path.join(config.TOP_REQUESTS, 'top_product_edited.tsv')

        source_file = next((f for f in os.listdir(source_folder) if f.endswith('.tsv')), None)
        if source_file is None:
            return jsonify({"error": "Nenhum arquivo TSV encontrado na pasta de origem."}), 404

        source_file_path = os.path.join(source_folder, source_file)

        shutil.copy(source_file_path, target_file)

        return jsonify({"message": "Tabela resetada com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



