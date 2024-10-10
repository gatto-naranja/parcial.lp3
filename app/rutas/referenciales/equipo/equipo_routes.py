from flask import Blueprint, render_template

equipomod = Blueprint('equipo', __name__, template_folder='templates')

@equipomod.route('/equipo-index')
def equipoIndex():
    return render_template('equipo-index.html')