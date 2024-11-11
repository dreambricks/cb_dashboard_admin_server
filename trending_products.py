from flask import Blueprint, request, render_template, current_app, jsonify, send_from_directory, Response
import os
import config
import shutil
import pandas as pd

trending_products_bp = Blueprint('trending_products', __name__)


@trending_products_bp.route('/trending-products')
def trending_products():
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']
    files = [filename for filename in os.listdir(folder_path) if filename.endswith('.tsv')]

    folder_path_edited = current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED']
    files_edited = [filename for filename in os.listdir(folder_path_edited) if filename.endswith('.tsv')]

    config_path = os.path.join(current_app.root_path, 'config.py')
    trending_products_edited = None
    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('TRENDING_PRODUCTS_EDITED'):
                value = line.split('=')[1].strip().strip('"').strip("'")
                trending_products_edited = value.lower() == 'true'
                break

    if trending_products_edited is None:
        return "TRENDING_PRODUCTS_EDITED not found in config.py", 500

    return render_template('trending_products.html', files=files, files_edited=files_edited,
                           trending_products_edited=trending_products_edited)


@trending_products_bp.route('/download-tsv/<filename>')
def download_tsv(filename):
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']
    return send_from_directory(folder_path, filename)


@trending_products_bp.route('/download-tsv-edited/<filename>')
def download_tsv_edited(filename):
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED']
    return send_from_directory(folder_path, filename)


@trending_products_bp.route('/save_trending_products_tables', methods=['POST'])
def save_tables():
    data = request.get_json()
    folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED']

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    for table in data:
        file_path = os.path.join(folder_path, table['filename'])
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


@trending_products_bp.route('/reset_trending_products_tables', methods=['POST'])
def reset_trending_products_tables():
    try:
        for filename in os.listdir(config.TRENDING_PRODUCTS_FOLDER_EDITED):
            file_path = os.path.join(config.TRENDING_PRODUCTS_FOLDER_EDITED, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        for filename in os.listdir(config.TRENDING_PRODUCTS_FOLDER_IN):
            src_file = os.path.join(config.TRENDING_PRODUCTS_FOLDER_IN, filename)
            dest_file = os.path.join(config.TRENDING_PRODUCTS_FOLDER_EDITED, filename)
            shutil.copy(src_file, dest_file)

        return jsonify({"success": True, "message": "Tabelas resetadas com sucesso!"})
    except Exception as e:
        print("Erro ao resetar tabelas:", e)
        return jsonify({"success": False, "error": str(e)})


@trending_products_bp.route('/get-trending-products', methods=['GET'])
def get_trending_products():

    config_path = os.path.join(current_app.root_path, 'config.py')
    trending_products_edited = None
    with open(config_path, 'r') as file:
        for line in file:
            if line.startswith('TRENDING_PRODUCTS_EDITED'):
                value = line.split('=')[1].strip().strip('"').strip("'")
                trending_products_edited = value.lower() == 'true'
                break

    if trending_products_edited is None:
        return "TRENDING_PRODUCTS_EDITED not found in config.py", 500

    if trending_products_edited:
        folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_EDITED']
    else:
        folder_path = current_app.config['TRENDING_PRODUCTS_FOLDER_IN']


    tsv_files = [f for f in os.listdir(folder_path) if f.endswith('.tsv')]

    if not tsv_files:
        return Response("No .tsv files found in the specified folder", status=404, mimetype='text/plain')

    combined_df = pd.DataFrame()

    for idx, file_name in enumerate(tsv_files):
        file_path = os.path.join(folder_path, file_name)

        df = pd.read_csv(file_path, sep='\t')

        df['categoria'] = os.path.splitext(file_name)[0]

        if idx == 0:
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    tsv_data = combined_df.to_csv(sep='\t', index=False)

    return Response(tsv_data, mimetype='text/plain; charset=utf-8')
