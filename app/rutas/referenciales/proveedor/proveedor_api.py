from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.proveedor.ProveedorDao import ProveedorDao

proveedorapi = Blueprint('proveedorapi', __name__)

# Trae todos los proveedores
@proveedorapi.route('/proveedores', methods=['GET'])
def getProveedores():
    proveedordao = ProveedorDao()

    try:
        proveedores = proveedordao.getProveedores()

        return jsonify({
            'success': True,
            'data': proveedores,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los proveedores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proveedorapi.route('/proveedores/<int:proveedor_id>', methods=['GET'])
def getProveedor(proveedor_id):
    proveedordao = ProveedorDao()

    try:
        proveedor = proveedordao.getProveedorById(proveedor_id)

        if proveedor:
            return jsonify({
                'success': True,
                'data': proveedor,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo proveedor
@proveedorapi.route('/proveedores', methods=['POST'])
def addProveedor():
    data = request.get_json()
    proveedordao = ProveedorDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'direccion', 'telefono', 'correo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        direccion = data['direccion'].upper()
        telefono = data['telefono']
        correo = data['correo'].lower()

        proveedor_id = proveedordao.guardarProveedor(nombre, direccion, telefono, correo)
        if proveedor_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'nombre': nombre, 'direccion': direccion, 
                         'telefono': telefono, 'correo': correo},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el proveedor. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proveedorapi.route('/proveedores/<int:proveedor_id>', methods=['PUT'])
def updateProveedor(proveedor_id):
    data = request.get_json()
    proveedordao = ProveedorDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'direccion', 'telefono', 'correo']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    direccion = data['direccion'].upper()
    telefono = data['telefono']
    correo = data['correo'].lower()

    try:
        if proveedordao.updateProveedor(proveedor_id, nombre, direccion, telefono, correo):
            return jsonify({
                'success': True,
                'data': {'id': proveedor_id, 'nombre': nombre, 'direccion': direccion, 
                         'telefono': telefono, 'correo': correo},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@proveedorapi.route('/proveedores/<int:proveedor_id>', methods=['DELETE'])
def deleteProveedor(proveedor_id):
    proveedordao = ProveedorDao()

    try:
        # Usar el retorno de eliminarProveedor para determinar el éxito
        if proveedordao.deleteProveedor(proveedor_id):
            return jsonify({
                'success': True,
                'mensaje': f'Proveedor con ID {proveedor_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el proveedor con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar proveedor: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
