from flask import Blueprint, request, redirect, url_for, render_template, Response, current_app, jsonify, \
    send_from_directory
import os

import config

trending_products_bp = Blueprint('trending_products', __name__)


@trending_products_bp.route('/trending-products')
def trending_products():
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']
    files = [filename for filename in os.listdir(folder_path) if filename.endswith('.tsv')]
    return render_template('trending_products.html', files=files,
                           trending_products_edited=config.TRENDING_PRODUCTS_EDITED)


@trending_products_bp.route('/download-tsv/<filename>')
def download_tsv(filename):
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']
    return send_from_directory(folder_path, filename)


@trending_products_bp.route('/save_tables', methods=['POST'])
def save_tables():
    data = request.get_json()

    if not os.path.exists(current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED']):
        os.makedirs(current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED'])

    for table in data:
        file_path = os.path.join(current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED'], table['filename'])
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(table['content'])

    return jsonify({"message": "Arquivos salvos com sucesso!"}), 200


@trending_products_bp.route('/toggle_trending_products_edited', methods=['POST'])
def toggle_trending_edited():
    data = request.get_json()
    if 'trendingProductsEdited' in data:
        new_value = data['trendingProductsEdited']

        try:
            with open('config.py', 'r') as file:
                config_content = file.readlines()
        except FileNotFoundError:
            return jsonify({'error': 'Arquivo config.py não encontrado'}), 500

        updated = False
        for i, line in enumerate(config_content):
            if line.startswith('TRENDING_PRODUCTS_EDITED'):
                config_content[i] = f'TRENDING_PRODUCTS_EDITED = {new_value}\n'
                updated = True
                break

        if not updated:
            config_content.append(f'TRENDING_PRODUCTS_EDITED = {new_value}\n')

        try:
            with open('config.py', 'w') as file:
                file.writelines(config_content)
        except Exception as e:
            return jsonify({'error': f'Erro ao atualizar config.py: {str(e)}'}), 500

        return jsonify({'message': 'TRENDING_PRODUCTS_EDITED atualizado com sucesso!'})
    return jsonify({'error': 'Dados inválidos'}), 400
