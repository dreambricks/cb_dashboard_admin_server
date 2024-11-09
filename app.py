from flask import Flask, redirect, url_for, abort, jsonify, Response

import config
from map import map_bp
from photo import photo_bp
from phrase import phrase_bp
from top_products import top_products_bp
from word_selection import word_selection_bp
from social_selection import social_selection_bp

import os

app = Flask(__name__)
app.secret_key = 'dbsupersecretkey'
app.config.from_pyfile('config.py')

app.register_blueprint(photo_bp)
app.register_blueprint(word_selection_bp)
app.register_blueprint(social_selection_bp)
app.register_blueprint(map_bp)
app.register_blueprint(top_products_bp)
app.register_blueprint(phrase_bp)

os.makedirs(app.config['PHOTO_FOLDER'], exist_ok=True)

os.makedirs(app.config['WORD_TSV_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['SOCIAL_TSV_FOLDER_IN'], exist_ok=True)

os.makedirs(app.config['WORD_TSV_FOLDER_OUT'], exist_ok=True)
os.makedirs(app.config['SOCIAL_TSV_FOLDER_OUT'], exist_ok=True)

os.makedirs(app.config['X_TSV_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['TIKTOK_TSV_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['INSTAGRAM_TSV_FOLDER_IN'], exist_ok=True)

os.makedirs(app.config['X_TSV_FOLDER_OUT'], exist_ok=True)
os.makedirs(app.config['TIKTOK_TSV_FOLDER_OUT'], exist_ok=True)
os.makedirs(app.config['INSTAGRAM_TSV_FOLDER_OUT'], exist_ok=True)

os.makedirs(app.config['MAP_TSV_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['MAP_TSV_FOLDER_EDITED'], exist_ok=True)

os.makedirs(app.config['TOP_PRODUCTS_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['TOP_PRODUCTS_FOLDER_EDITED'], exist_ok=True)

@app.route('/alive')
def alive():
    return 'alive'

@app.route('/')
def index():
    return redirect(url_for('photo.upload_image'))


@app.route('/get-tsv/<config_path>', methods=['GET'])
def get_first_tsv_file(config_path):
    folder_path =  app.config[f'{config_path}']

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)