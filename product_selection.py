import pandas as pd
from flask import Blueprint, render_template, current_app
import os


product_selection_bp = Blueprint('product_selection', __name__)


@product_selection_bp.route('/product-selection')
def index():
    return render_template('product-selection.html')
