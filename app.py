from flask import Flask, redirect, url_for

import config
from map import map_bp
from photo import photo_bp
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
os.makedirs(app.config['TOP_PRODUCTS_FOLDER_OUT'], exist_ok=True)

@app.route('/alive')
def alive():
    return 'alive'

@app.route('/')
def index():
    return redirect(url_for('photo.upload_image'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)