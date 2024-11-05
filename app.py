from flask import Flask, redirect, url_for

from photo import photo_bp
from word_selection import word_selection_bp
from social_selection import social_selection_bp

import os

app = Flask(__name__)
app.secret_key = 'dbsupersecretkey'
app.config.from_pyfile('config.py')

app.register_blueprint(photo_bp)
app.register_blueprint(word_selection_bp)
app.register_blueprint(social_selection_bp)

os.makedirs(app.config['PHOTO_FOLDER'], exist_ok=True)

os.makedirs(app.config['WORD_CSV_FOLDER_IN'], exist_ok=True)
os.makedirs(app.config['SOCIAL_CSV_FOLDER_IN'], exist_ok=True)

os.makedirs(app.config['WORD_CSV_FOLDER_OUT'], exist_ok=True)
os.makedirs(app.config['SOCIAL_CSV_FOLDER_OUT'], exist_ok=True)

@app.route('/alive')
def alive():
    return 'alive'

@app.route('/')
def index():
    return redirect(url_for('photo.upload_image'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)