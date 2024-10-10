from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.tarea.TareaDao import TareaDao

tareaapi = Blueprint('tareaapi', __name__)

# Trae todas las tareas
@tareaapi.route('/tareas', methods=['GET'])
def getTareas():
    tareadao = TareaDao()

    try:
        tareas = tareadao.getTareas()

        return jsonify({
            'success': True,
            'data': tareas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las tareas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tareaapi.route('/tareas/<int:tarea_id>', methods=['GET'])
def getTarea(tarea_id):
    tareadao = TareaDao()

    try:
        tarea = tareadao.getTareaById(tarea_id)

        if tarea:
            return jsonify({
                'success': True,
                'data': tarea,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarea con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener tarea: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva tarea
@tareaapi.route('/tareas', methods=['POST'])
def addTarea():
    data = request.get_json()
    tareadao = TareaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['responsable', 'descripcion', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        responsable = data['responsable'].upper()
        descripcion = data['descripcion'].upper()
        estado = data['estado'].upper()
        tarea_id = tareadao.guardarTarea(responsable, descripcion, estado)
        if tarea_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': tarea_id, 'responsable': responsable, 'descripcion': descripcion, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la tarea. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar tarea: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tareaapi.route('/tareas/<int:tarea_id>', methods=['PUT'])
def updateTarea(tarea_id):
    data = request.get_json()
    tareadao = TareaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['responsable', 'descripcion', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    responsable = data['responsable'].upper()
    descripcion = data['descripcion'].upper()
    estado = data['estado'].upper()
    try:
        if tareadao.updateTarea(tarea_id, responsable, descripcion, estado):
            return jsonify({
                'success': True,
                'data': {'id': tarea_id, 'responsable': responsable, 'descripcion': descripcion, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarea con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar tarea: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@tareaapi.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def deleteTarea(tarea_id):
    tareadao = TareaDao()

    try:
        # Usar el retorno de eliminarTarea para determinar el éxito
        if tareadao.deleteTarea(tarea_id):
            return jsonify({
                'success': True,
                'mensaje': f'Tarea con ID {tarea_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la tarea con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar tarea: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500