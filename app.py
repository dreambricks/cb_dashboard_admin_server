from flask import Flask, redirect, url_for

from photo import photo_bp
from product_selection import product_selection_bp
from tweet_selection import tweet_selection_bp

import os

app = Flask(__name__)

app.register_blueprint(photo_bp)
app.register_blueprint(product_selection_bp)
app.register_blueprint(tweet_selection_bp)

UPLOAD_FOLDER = 'static/photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/alive')
def alive():
    return 'alive'

@app.route('/')
def index():
    return redirect(url_for('photo.upload_image'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)