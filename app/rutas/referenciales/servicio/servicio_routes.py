from flask import Blueprint, render_template

serviciomod = Blueprint('servicio', __name__, template_folder='templates')

@serviciomod.route('/servicio-index')
def servicioIndex():
    return render_template('servicio-index.html')
