from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.pago.PagoDao import PagoDao

pagoapi = Blueprint('pagoapi', __name__)

# Trae todos los pagos
@pagoapi.route('/pagos', methods=['GET'])
def getPagos():
    pagodao = PagoDao()

    try:
        pagos = pagodao.getPagos()

        return jsonify({
            'success': True,
            'data': pagos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los pagos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pagoapi.route('/pagos/<int:pago_id>', methods=['GET'])
def getPago(pago_id):
    pagodao = PagoDao()

    try:
        pago = pagodao.getPagoById(pago_id)

        if pago:
            return jsonify({
                'success': True,
                'data': pago,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pago con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo pago
@pagoapi.route('/pagos', methods=['POST'])
def addPago():
    data = request.get_json()
    pagodao = PagoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'monto_pagado', 'fecha_pago', 'metodo_pago']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        monto_pagado = data['monto_pagado']
        fecha_pago = data['fecha_pago']
        metodo_pago = data['metodo_pago'].upper()

        pago_id = pagodao.guardarPago(descripcion, monto_pagado, fecha_pago, metodo_pago)
        if pago_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': pago_id, 'descripcion': descripcion, 'monto_pagado': monto_pagado, 
                         'fecha_pago': fecha_pago, 'metodo_pago': metodo_pago},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el pago. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pagoapi.route('/pagos/<int:pago_id>', methods=['PUT'])
def updatePago(pago_id):
    data = request.get_json()
    pagodao = PagoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion', 'monto_pagado', 'fecha_pago', 'metodo_pago']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion'].upper()
    monto_pagado = data['monto_pagado']
    fecha_pago = data['fecha_pago']
    metodo_pago = data['metodo_pago'].upper()

    try:
        if pagodao.updatePago(pago_id, descripcion, monto_pagado, fecha_pago, metodo_pago):
            return jsonify({
                'success': True,
                'data': {'id': pago_id, 'descripcion': descripcion, 'monto_pagado': monto_pagado, 
                         'fecha_pago': fecha_pago, 'metodo_pago': metodo_pago},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pago con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pagoapi.route('/pagos/<int:pago_id>', methods=['DELETE'])
def deletePago(pago_id):
    pagodao = PagoDao()

    try:
        # Usar el retorno de eliminarPago para determinar el éxito
        if pagodao.deletePago(pago_id):
            return jsonify({
                'success': True,
                'mensaje': f'Pago con ID {pago_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el pago con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar pago: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500