from flask import Blueprint, render_template

beneficiomod = Blueprint('beneficio', __name__, template_folder='templates')

@beneficiomod.route('/beneficio-index')
def beneficioIndex():
    return render_template('beneficio-index.html')