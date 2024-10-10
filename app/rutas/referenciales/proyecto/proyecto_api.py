from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.proyecto.ProyectoDao import ProyectoDao

proyectoapi = Blueprint('proyectoapi', __name__)

# Trae todos los proyectos
@proyectoapi.route('/proyectos', methods=['GET'])
def getProyectos():
    proyectodao = ProyectoDao()

    try:
        proyectos = proyectodao.getProyectos()

        return jsonify({
            'success': True,
            'data': proyectos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los proyectos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proyectoapi.route('/proyectos/<int:proyecto_id>', methods=['GET'])
def getProyecto(proyecto_id):
    proyectodao = ProyectoDao()

    try:
        proyecto = proyectodao.getProyectoById(proyecto_id)

        if proyecto:
            return jsonify({
                'success': True,
                'data': proyecto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proyecto con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener proyecto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo proyecto
@proyectoapi.route('/proyectos', methods=['POST'])
def addProyecto():
    data = request.get_json()
    proyectodao = ProyectoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'fecha_inicio', 'fecha_fin', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        estado = data['estado'].upper()

        proyecto_id = proyectodao.guardarProyecto(nombre, fecha_inicio, fecha_fin, estado)
        if proyecto_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': proyecto_id, 'nombre': nombre, 
                         'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 
                         'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el proyecto. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar proyecto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proyectoapi.route('/proyectos/<int:proyecto_id>', methods=['PUT'])
def updateProyecto(proyecto_id):
    data = request.get_json()
    proyectodao = ProyectoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'fecha_inicio', 'fecha_fin', 'estado']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    fecha_inicio = data['fecha_inicio']
    fecha_fin = data['fecha_fin']
    estado = data['estado'].upper()

    try:
        if proyectodao.updateProyecto(proyecto_id, nombre, fecha_inicio, fecha_fin, estado):
            return jsonify({
                'success': True,
                'data': {'id': proyecto_id, 'nombre': nombre, 
                         'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 
                         'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proyecto con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar proyecto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proyectoapi.route('/proyectos/<int:proyecto_id>', methods=['DELETE'])
def deleteProyecto(proyecto_id):
    proyectodao = ProyectoDao()

    try:
        # Usar el retorno de eliminarProyecto para determinar el éxito
        if proyectodao.deleteProyecto(proyecto_id):
            return jsonify({
                'success': True,
                'mensaje': f'Proyecto con ID {proyecto_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proyecto con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar proyecto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
