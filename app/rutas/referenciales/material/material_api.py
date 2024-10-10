from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.material.MaterialDao import MaterialDao

materialapi = Blueprint('materialapi', __name__)

# Trae todos los materiales
@materialapi.route('/materiales', methods=['GET'])
def getMateriales():
    materialdao = MaterialDao()

    try:
        materiales = materialdao.getMateriales()

        return jsonify({
            'success': True,
            'data': materiales,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los materiales: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@materialapi.route('/materiales/<int:material_id>', methods=['GET'])
def getMaterial(material_id):
    materialdao = MaterialDao()

    try:
        material = materialdao.getMaterialById(material_id)

        if material:
            return jsonify({
                'success': True,
                'data': material,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el material con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener material: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo material
@materialapi.route('/materiales', methods=['POST'])
def addMaterial():
    data = request.get_json()
    materialdao = MaterialDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'costo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        descripcion = data['descripcion'].upper()
        costo = data['costo']

        material_id = materialdao.guardarMaterial(nombre, descripcion, costo)
        if material_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': material_id, 'nombre': nombre, 'descripcion': descripcion, 
                         'costo': costo},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el material. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar material: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@materialapi.route('/materiales/<int:material_id>', methods=['PUT'])
def updateMaterial(material_id):
    data = request.get_json()
    materialdao = MaterialDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'costo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    descripcion = data['descripcion'].upper()
    costo = data['costo']

    try:
        if materialdao.updateMaterial(material_id, nombre, descripcion, costo):
            return jsonify({
                'success': True,
                'data': {'id': material_id, 'nombre': nombre, 'descripcion': descripcion, 
                         'costo': costo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el material con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar material: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@materialapi.route('/materiales/<int:material_id>', methods=['DELETE'])
def deleteMaterial(material_id):
    materialdao = MaterialDao()

    try:
        # Usar el retorno de eliminarMaterial para determinar el éxito
        if materialdao.deleteMaterial(material_id):
            return jsonify({
                'success': True,
                'mensaje': f'Material con ID {material_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el material con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar material: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
