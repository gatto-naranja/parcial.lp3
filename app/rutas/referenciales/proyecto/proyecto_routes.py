from flask import Blueprint, render_template

proyectomod = Blueprint('proyecto', __name__, template_folder='templates')

@proyectomod.route('/proyecto-index')
def proyectoIndex():
    return render_template('proyecto-index.html')