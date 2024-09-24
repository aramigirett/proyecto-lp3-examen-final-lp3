from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.telefono.TelefonoDao import TelefonoDao

telapi = Blueprint('telapi', __name__)

# Trae todas las ciudades
@telapi.route('/telefonos', methods=['GET'])
def getTelefonos():
    teldao = TelefonoDao()

    try:
        telefonos = teldao.getTelefono()

        return jsonify({
            'success': True,
            'data': telefonos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las telefonos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@telapi.route('/telefonos/<int:telefono_id>', methods=['GET'])
def getTelefono(telefono_id):
    teldao = TelefonoDao()

    try:
        telefono = teldao.getTelefonoById(telefono_id)

        if telefono:
            return jsonify({
                'success': True,
                'data': telefono,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la telefono con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener telefono: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva telefono
@telapi.route('/telefonos', methods=['POST'])
def addTelefono():
    data = request.get_json()
    teldao = TelefonoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        telefono_id = teldao.guardarTelefono(descripcion)
        if telefono_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': telefono_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la telefono. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar telefono: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@telapi.route('/telefonos/<int:telefono_id>', methods=['PUT'])
def updateTelefono(telefono_id):
    data = request.get_json()
    teldao = TelefonoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if teldao.updateTelefono(telefono_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': telefono_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la telefono con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar telefono: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@telapi.route('/telefonos/<int:telefono_id>', methods=['DELETE'])
def deleteTelefono(telefono_id):
    teldao = TelefonoDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if teldao.deleteTelefono(telefono_id):
            return jsonify({
                'success': True,
                'mensaje': f'Telefono con ID {telefono_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la telefono con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar telefono: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
    