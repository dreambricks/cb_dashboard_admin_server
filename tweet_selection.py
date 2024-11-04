from flask import Blueprint, render_template, request, current_app, url_for, jsonify
import os

tweet_selection_bp = Blueprint('tweet_selection', __name__)

@tweet_selection_bp.route('/tweet-selection')
def index():
    return render_template('tweet-selection.html')


@tweet_selection_bp.route('/save_tweets_csv', methods=['POST'])
def save_csv():
    data = request.get_json()
    csv_content = data.get("csv", "")

    csv_filename = 'tweets.csv'
    csv_path = os.path.join(current_app.config['PRODUCT_CSV_FOLDER'], csv_filename)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)

    download_url = url_for('static', filename=f'products_csv/{csv_filename}', _external=True)

    return jsonify({'download_url': download_url})