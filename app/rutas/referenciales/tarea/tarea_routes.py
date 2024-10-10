from flask import Blueprint, render_template

tareamod = Blueprint('tarea', __name__, template_folder='templates')

@tareamod.route('/tarea-index')
def tareaIndex():
    return render_template('tarea-index.html')