from flask import Blueprint, render_template

product_selection_bp = Blueprint('product_selection', __name__)

@product_selection_bp.route('/product-selection')
def index():
    return render_template('product-selection.html')