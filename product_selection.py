from flask import Blueprint, render_template, current_app, request, url_for, jsonify
import os

product_selection_bp = Blueprint('product_selection', __name__)


@product_selection_bp.route('/product-selection')
def index():
    csv_filename = 'produtos.csv'
    csv_path = os.path.join(current_app.config['PRODUCT_CSV_FOLDER'], csv_filename)
    new_path = csv_path.replace("\\", "/")
    print(new_path)
    return render_template('product-selection.html', csv_path=new_path)


@product_selection_bp.route('/save_csv', methods=['POST'])
def save_csv():
    data = request.get_json()
    csv_content = data.get("csv", "")

    csv_filename = 'produtos.csv'
    csv_path = os.path.join(current_app.config['PRODUCT_CSV_FOLDER'], csv_filename)

    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)

    download_url = url_for('static', filename=f'products_csv/{csv_filename}', _external=True)

    return jsonify({'download_url': download_url})
