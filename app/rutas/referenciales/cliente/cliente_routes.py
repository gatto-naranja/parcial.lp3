from flask import Blueprint, render_template

clientemod = Blueprint('cliente', __name__, template_folder='templates')

@clientemod.route('/cliente-index')
def clienteIndex():
    return render_template('cliente-index.html')