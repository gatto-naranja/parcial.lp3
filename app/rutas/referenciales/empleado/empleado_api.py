from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.empleado.EmpleadoDao import EmpleadoDao

empleadoapi = Blueprint('empleadoapi', __name__)

# Trae todos los empleados
@empleadoapi.route('/empleados', methods=['GET'])
def getEmpleados():
    empleadodao = EmpleadoDao()

    try:
        empleados = empleadodao.getEmpleados()

        return jsonify({
            'success': True,
            'data': empleados,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los empleados: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@empleadoapi.route('/empleados/<int:empleado_id>', methods=['GET'])
def getEmpleado(empleado_id):
    empleadodao = EmpleadoDao()

    try:
        empleado = empleadodao.getEmpleadoById(empleado_id)

        if empleado:
            return jsonify({
                'success': True,
                'data': empleado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el empleado con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener empleado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo empleado
@empleadoapi.route('/empleados', methods=['POST'])
def addEmpleado():
    data = request.get_json()
    empleadodao = EmpleadoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'cargo', 'telefono']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cargo = data['cargo'].upper()
        telefono = data['telefono']

        empleado_id = empleadodao.guardarEmpleado(nombre, apellido, cargo, telefono)
        if empleado_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': empleado_id, 'nombre': nombre, 'apellido': apellido, 
                         'cargo': cargo, 'telefono': telefono},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el empleado. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar empleado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@empleadoapi.route('/empleados/<int:empleado_id>', methods=['PUT'])
def updateEmpleado(empleado_id):
    data = request.get_json()
    empleadodao = EmpleadoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'cargo', 'telefono']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    apellido = data['apellido'].upper()
    cargo = data['cargo'].upper()
    telefono = data['telefono']

    try:
        if empleadodao.updateEmpleado(empleado_id, nombre, apellido, cargo, telefono):
            return jsonify({
                'success': True,
                'data': {'id': empleado_id, 'nombre': nombre, 'apellido': apellido, 
                         'cargo': cargo, 'telefono': telefono},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el empleado con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar empleado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@empleadoapi.route('/empleados/<int:empleado_id>', methods=['DELETE'])
def deleteEmpleado(empleado_id):
    empleadodao = EmpleadoDao()

    try:
        # Usar el retorno de eliminarEmpleado para determinar el éxito
        if empleadodao.deleteEmpleado(empleado_id):
            return jsonify({
                'success': True,
                'mensaje': f'Empleado con ID {empleado_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el empleado con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar empleado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
