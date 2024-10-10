from flask import Blueprint, render_template

proveedormod = Blueprint('proveedor', __name__, template_folder='templates')

@proveedormod.route('/proveedor-index')
def proveedorIndex():
    return render_template('proveedor-index.html')