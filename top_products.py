from flask import Blueprint, current_app, render_template, request, jsonify
import os

import config

top_products_bp = Blueprint('top_products', __name__)


@top_products_bp.route('/top-products')
def index():
    folder_path = current_app.config['TOP_PRODUCTS_FOLDER_IN']
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
    return render_template('top-products.html', tsv_path=new_path, product_edited=config.PRODUCT_EDITED)


@top_products_bp.route('/save-edited-table', methods=['POST'])
def save_edited_table():
    data = request.json.get('data')
    if data:
        output_path = os.path.join(current_app.config['TOP_PRODUCTS_FOLDER_OUT'], 'edited_table.tsv')
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
