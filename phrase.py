from flask import Blueprint, request, redirect, url_for, render_template, Response
import os

import config

phrase_bp = Blueprint('phrase', __name__)


def get_saved_phrase():
    return config.PHRASE

def update_phrase_in_config(phrase):
    if not os.path.exists('config.py'):
        with open('config.py', 'w') as config_file:
            config_file.write(f'PHRASE = "{phrase}"\n')
    else:
        with open('config.py', 'r') as config_file:
            lines = config_file.readlines()

        updated = False
        with open('config.py', 'w') as config_file:
            for line in lines:
                if line.startswith('PHRASE ='):
                    config_file.write(f'PHRASE = "{phrase}"\n')
                    updated = True
                else:
                    config_file.write(line)
            if not updated:
                config_file.write(f'PHRASE = "{phrase}"\n')


@phrase_bp.route('/phrase', methods=['GET', 'POST'])
def phrase():
    if request.method == 'POST':
        phrase = request.form['phrase']
        update_phrase_in_config(phrase)
        return redirect(url_for('photo.upload_image'))

    saved_phrase = get_saved_phrase()
    return render_template('phrase.html', phrase=saved_phrase)


@phrase_bp.route('/get-phrase')
def get_phrase():
    phrase = config.PHRASE
    response = Response(phrase, content_type='text/plain; charset=utf-8')

    return response