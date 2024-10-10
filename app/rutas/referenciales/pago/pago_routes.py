from flask import Blueprint, render_template

pagomod = Blueprint('pago', __name__, template_folder='templates')

@pagomod.route('/pago-index')
def pagoIndex():
    return render_template('pago-index.html')