from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.vehiculo.VehiculoDao import VehiculoDao

vehiculoapi = Blueprint('vehiculoapi', __name__)

# Trae todos los vehiculos
@vehiculoapi.route('/vehiculos', methods=['GET'])
def getVehiculos():
    vehiculodao = VehiculoDao()

    try:
        vehiculos = vehiculodao.getVehiculos()

        return jsonify({
            'success': True,
            'data': vehiculos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los vehiculos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiculoapi.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def getVehiculo(vehiculo_id):
    vehiculodao = VehiculoDao()

    try:
        vehiculo = vehiculodao.getVehiculoById(vehiculo_id)

        if vehiculo:
            return jsonify({
                'success': True,
                'data': vehiculo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo vehiculo
@vehiculoapi.route('/vehiculos', methods=['POST'])
def addVehiculo():
    data = request.get_json()
    vehiculodao = VehiculoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['marca', 'modelo', 'año', 'matricula']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        marca = data['marca'].upper()
        modelo = data['modelo'].upper()
        año = data['año']
        matricula = data['matricula'].upper()

        vehiculo_id = vehiculodao.guardarVehiculo(marca, modelo, año, matricula)
        if vehiculo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'marca': marca, 'modelo': modelo, 
                         'año': año, 'matricula': matricula},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el vehiculo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiculoapi.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def updateVehiculo(vehiculo_id):
    data = request.get_json()
    vehiculodao = VehiculoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['marca', 'modelo', 'año', 'matricula']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    marca = data['marca'].upper()
    modelo = data['modelo'].upper()
    año = data['año']
    matricula = data['matricula'].upper()

    try:
        if vehiculodao.updateVehiculo(vehiculo_id, marca, modelo, año, matricula):
            return jsonify({
                'success': True,
                'data': {'id': vehiculo_id, 'marca': marca, 'modelo': modelo, 
                         'año': año, 'matricula': matricula},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@vehiculoapi.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def deleteVehiculo(vehiculo_id):
    vehiculodao = VehiculoDao()

    try:
        # Usar el retorno de eliminarVehiculo para determinar el éxito
        if vehiculodao.deleteVehiculo(vehiculo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Vehiculo con ID {vehiculo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el vehiculo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar vehiculo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
