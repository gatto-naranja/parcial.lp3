from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.meta.MetaDao import MetaDao

metaapi = Blueprint('metaapi', __name__)

# Trae todas las metas
@metaapi.route('/metas', methods=['GET'])
def getMetas():
    metadao = MetaDao()

    try:
        metas = metadao.getMetas()

        return jsonify({
            'success': True,
            'data': metas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las metas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@metaapi.route('/metas/<int:meta_id>', methods=['GET'])
def getMeta(meta_id):
    metadao = MetaDao()

    try:
        meta = metadao.getMetaById(meta_id)

        if meta:
            return jsonify({
                'success': True,
                'data': meta,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la meta con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener meta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva meta
@metaapi.route('/metas', methods=['POST'])
def addMeta():
    data = request.get_json()
    metadao = MetaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'fecha_inicio', 'fecha_finalizacion', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        fecha_inicio = data['fecha_inicio']
        fecha_finalizacion = data['fecha_finalizacion']
        estado = data['estado'].upper()

        meta_id = metadao.guardarMeta(descripcion, fecha_inicio, fecha_finalizacion, estado)
        if meta_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': meta_id, 'descripcion': descripcion, 'fecha_inicio': fecha_inicio, 
                         'fecha_finalizacion': fecha_finalizacion, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la meta. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar meta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@metaapi.route('/metas/<int:meta_id>', methods=['PUT'])
def updateMeta(meta_id):
    data = request.get_json()
    metadao = MetaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'fecha_inicio', 'fecha_finalizacion', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion'].upper()
    fecha_inicio = data['fecha_inicio']
    fecha_finalizacion = data['fecha_finalizacion']
    estado = data['estado'].upper()

    try:
        if metadao.updateMeta(meta_id, descripcion, fecha_inicio, fecha_finalizacion, estado):
            return jsonify({
                'success': True,
                'data': {'id': meta_id, 'descripcion': descripcion, 'fecha_inicio': fecha_inicio, 
                         'fecha_finalizacion': fecha_finalizacion, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la meta con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar meta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@metaapi.route('/metas/<int:meta_id>', methods=['DELETE'])
def deleteMeta(meta_id):
    metadao = MetaDao()

    try:
        # Usar el retorno de eliminarMeta para determinar el éxito
        if metadao.deleteMeta(meta_id):
            return jsonify({
                'success': True,
                'mensaje': f'Meta con ID {meta_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la meta con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar meta: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500