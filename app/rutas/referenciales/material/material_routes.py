from flask import Blueprint, render_template

materialmod = Blueprint('material', __name__, template_folder='templates')

@materialmod.route('/material-index')
def materialIndex():
    return render_template('material-index.html')