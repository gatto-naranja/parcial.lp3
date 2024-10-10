from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.equipo.EquipoDao  import EquipoDao

equipoapi = Blueprint('equipoapi', __name__)

# Trae todos los equipos
@equipoapi.route('/equipos', methods=['GET'])
def getEquipos():
    equipodao = EquipoDao()

    try:
        equipos = equipodao.getEquipos()

        return jsonify({
            'success': True,
            'data': equipos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los equipos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@equipoapi.route('/equipos/<int:equipo_id>', methods=['GET'])
def getEquipo(equipo_id):
    equipodao = EquipoDao()

    try:
        equipo = equipodao.getEquipoById(equipo_id)

        if equipo:
            return jsonify({
                'success': True,
                'data': equipo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el equipo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener equipo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo equipo
@equipoapi.route('/equipos', methods=['POST'])
def addEquipo():
    data = request.get_json()
    equipodao = EquipoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'tipo', 'modelo', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        tipo = data['tipo'].upper()
        modelo = data['modelo'].upper()
        estado = data['estado'].upper()

        equipo_id = equipodao.guardarEquipo(nombre, tipo, modelo, estado)
        if equipo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': equipo_id, 'nombre': nombre, 
                         'tipo': tipo, 'modelo': modelo, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el equipo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar equipo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@equipoapi.route('/equipos/<int:equipo_id>', methods=['PUT'])
def updateEquipo(equipo_id):
    data = request.get_json()
    equipodao = EquipoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'tipo', 'modelo', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    tipo = data['tipo'].upper()
    modelo = data['modelo'].upper()
    estado = data['estado'].upper()

    try:
        if equipodao.updateEquipo(equipo_id, nombre, tipo, modelo, estado):
            return jsonify({
                'success': True,
                'data': {'id': equipo_id, 'nombre': nombre, 
                         'tipo': tipo, 'modelo': modelo, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el equipo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar equipo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@equipoapi.route('/equipos/<int:equipo_id>', methods=['DELETE'])
def deleteEquipo(equipo_id):
    equipodao = EquipoDao()

    try:
        # Usar el retorno de eliminarEquipo para determinar el éxito
        if equipodao.deleteEquipo(equipo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Equipo con ID {equipo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el equipo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar equipo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
