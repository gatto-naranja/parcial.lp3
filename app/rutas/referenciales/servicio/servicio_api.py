from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.servicio.ServicioDao import ServicioDao

servicioapi = Blueprint('servicioapi', __name__)

# Trae todos los servicios
@servicioapi.route('/servicios', methods=['GET'])
def getServicios():
    serviciodao = ServicioDao()

    try:
        servicios = serviciodao.getServicios()

        return jsonify({
            'success': True,
            'data': servicios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los servicios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@servicioapi.route('/servicios/<int:servicio_id>', methods=['GET'])
def getServicio(servicio_id):
    serviciodao = ServicioDao()

    try:
        servicio = serviciodao.getServicioById(servicio_id)

        if servicio:
            return jsonify({
                'success': True,
                'data': servicio,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el servicio con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo servicio
@servicioapi.route('/servicios', methods=['POST'])
def addServicio():
    data = request.get_json()
    serviciodao = ServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'costo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        costo = float(data['costo'])
        servicio_id = serviciodao.guardarServicio(descripcion, costo)
        if servicio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': servicio_id, 'descripcion': descripcion, 'costo': costo},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el servicio. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@servicioapi.route('/servicios/<int:servicio_id>', methods=['PUT'])
def updateServicio(servicio_id):
    data = request.get_json()
    serviciodao = ServicioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'costo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    descripcion = data['descripcion']
    costo = float(data['costo'])

    try:
        if serviciodao.updateServicio(servicio_id, descripcion.upper(), costo):
            return jsonify({
                'success': True,
                'data': {'id': servicio_id, 'descripcion': descripcion, 'costo': costo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el servicio con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@servicioapi.route('/servicios/<int:servicio_id>', methods=['DELETE'])
def deleteServicio(servicio_id):
    serviciodao = ServicioDao()

    try:
        # Usar el retorno de eliminarServicio para determinar el éxito
        if serviciodao.deleteServicio(servicio_id):
            return jsonify({
                'success': True,
                'mensaje': f'Servicio con ID {servicio_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el servicio con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar servicio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
