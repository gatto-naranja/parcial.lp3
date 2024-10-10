from flask import Blueprint, render_template

vehiculomod = Blueprint('vehiculo', __name__, template_folder='templates')

@vehiculomod.route('/vehiculo-index')
def vehiculoIndex():
    return render_template('vehiculo-index.html')