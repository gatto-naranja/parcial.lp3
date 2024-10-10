from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.beneficio.BeneficioDao import BeneficioDao

beneficioapi = Blueprint('beneficioapi', __name__)

# Trae todos los beneficios
@beneficioapi.route('/beneficios', methods=['GET'])
def getBeneficios():
    beneficiodao = BeneficioDao()

    try:
        beneficios = beneficiodao.getBeneficios()

        return jsonify({
            'success': True,
            'data': beneficios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los beneficios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@beneficioapi.route('/beneficios/<int:beneficio_id>', methods=['GET'])
def getBeneficio(beneficio_id):
    beneficiodao = BeneficioDao()

    try:
        beneficio = beneficiodao.getBeneficioById(beneficio_id)

        if beneficio:
            return jsonify({
                'success': True,
                'data': beneficio,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el beneficio con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener beneficio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo beneficio
@beneficioapi.route('/beneficios', methods=['POST'])
def addBeneficio():
    data = request.get_json()
    beneficiodao = BeneficioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'duracion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        nombre = data['nombre'].upper()
        descripcion = data['descripcion'].upper()
        duracion = data['duracion'].upper()
        beneficio_id = beneficiodao.guardarBeneficio(nombre, descripcion, duracion)
        if beneficio_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': beneficio_id, 'nombre': nombre, 'descripcion': descripcion, 'duracion': duracion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el beneficio. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar beneficio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@beneficioapi.route('/beneficios/<int:beneficio_id>', methods=['PUT'])
def updateBeneficio(beneficio_id):
    data = request.get_json()
    beneficiodao = BeneficioDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'duracion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    nombre = data['nombre'].upper()
    descripcion = data['descripcion'].upper()
    duracion = data['duracion'].upper()
    try:
        if beneficiodao.updateBeneficio(beneficio_id, nombre, descripcion, duracion):
            return jsonify({
                'success': True,
                'data': {'id': beneficio_id, 'nombre': nombre, 'descripcion': descripcion, 'duracion': duracion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el beneficio con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar beneficio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@beneficioapi.route('/beneficios/<int:beneficio_id>', methods=['DELETE'])
def deleteBeneficio(beneficio_id):
    beneficiodao = BeneficioDao()

    try:
        # Usar el retorno de eliminarBeneficio para determinar el éxito
        if beneficiodao.deleteBeneficio(beneficio_id):
            return jsonify({
                'success': True,
                'mensaje': f'Beneficio con ID {beneficio_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el beneficio con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar beneficio: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
