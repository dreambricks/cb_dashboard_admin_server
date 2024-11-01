from flask import Blueprint, render_template

tweet_selection_bp = Blueprint('tweet_selection', __name__)

@tweet_selection_bp.route('/tweet-selection')
def index():
    return render_template('tweet-selection.html')