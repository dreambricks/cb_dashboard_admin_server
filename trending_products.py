from flask import Blueprint, request, redirect, url_for, render_template, Response, current_app, jsonify, \
    send_from_directory
import os
import pandas as pd

import config

trending_products_bp = Blueprint('trending_products', __name__)


@trending_products_bp.route('/trending-products')
def trending_products():
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']
    files = [filename for filename in os.listdir(folder_path) if filename.endswith('.tsv')]
    return render_template('trending_products.html', files=files)


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
