from flask import Blueprint, render_template

metamod = Blueprint('meta', __name__, template_folder='templates')

@metamod.route('/meta-index')
def metaIndex():
    return render_template('meta-index.html')