from flask import Blueprint, render_template

empleadomod = Blueprint('empleado', __name__, template_folder='templates')

@empleadomod.route('/empleado-index')
def empleadoIndex():
    return render_template('empleado-index.html')