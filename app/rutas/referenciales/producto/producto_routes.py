from flask import Blueprint, render_template

productomod = Blueprint('producto', __name__, template_folder='templates')

@productomod.route('/producto-index')
def productoIndex():
    return render_template('producto-index.html')