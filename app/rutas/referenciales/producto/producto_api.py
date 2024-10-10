from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.producto.ProductoDao import ProductoDao

productoapi = Blueprint('productoapi', __name__)

# Trae todos los productos
@productoapi.route('/productos', methods=['GET'])
def getProductos():
    productodao = ProductoDao()

    try:
        productos = productodao.getProductos()

        return jsonify({
            'success': True,
            'data': productos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los productos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@productoapi.route('/productos/<int:producto_id>', methods=['GET'])
def getProducto(producto_id):
    productodao = ProductoDao()

    try:
        producto = productodao.getProductoById(producto_id)

        if producto:
            return jsonify({
                'success': True,
                'data': producto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el producto con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener producto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo producto
@productoapi.route('/productos', methods=['POST'])
def addProducto():
    data = request.get_json()
    productodao = ProductoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'precio', 'stock']

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
        precio = float(data['precio'])
        stock = int(data['stock'])

        producto_id = productodao.guardarProducto(nombre, descripcion, precio, stock)
        if producto_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': producto_id, 'nombre': nombre, 
                         'descripcion': descripcion, 'precio': precio, 'stock': stock},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el producto. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar producto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@productoapi.route('/productos/<int:producto_id>', methods=['PUT'])
def updateProducto(producto_id):
    data = request.get_json()
    productodao = ProductoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'descripcion', 'precio', 'stock']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombre = data['nombre'].upper()
    descripcion = data['descripcion'].upper()
    precio = float(data['precio'])
    stock = int(data['stock'])

    try:
        if productodao.updateProducto(producto_id, nombre, descripcion, precio, stock):
            return jsonify({
                'success': True,
                'data': {'id': producto_id, 'nombre': nombre, 
                         'descripcion': descripcion, 'precio': precio, 'stock': stock},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el producto con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar producto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@productoapi.route('/productos/<int:producto_id>', methods=['DELETE'])
def deleteProducto(producto_id):
    productodao = ProductoDao()

    try:
        # Usar el retorno de eliminarProducto para determinar el éxito
        if productodao.deleteProducto(producto_id):
            return jsonify({
                'success': True,
                'mensaje': f'Producto con ID {producto_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el producto con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar producto: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
