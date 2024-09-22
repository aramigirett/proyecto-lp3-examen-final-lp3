from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.correo.CorreoDao import CorreoDao

correoapi = Blueprint('correoapi', __name__)

# Trae todas los correos
@correoapi.route('/correos', methods=['GET'])
def getCorreos():
    correodao = CorreoDao()

    try:
        correos = correodao.getCorreos()

        return jsonify({
            'success': True,
            'data': correos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas los correos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@correoapi.route('/correos/<int:correo_id>', methods=['GET'])
def getCorreo(correo_id):
    correodao = CorreoDao()

    try:
        correo = correodao.getCorreoById(correo_id)

        if correo:
            return jsonify({
                'success': True,
                'data': correo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el correo con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener correo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nuevo correo
@correoapi.route('/correos', methods=['POST'])
def addCorreo():
    data = request.get_json()
    correodao = CorreoDao()

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
        correo_id = correodao.guardarCorreo(descripcion)
        if correo_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': correo_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el correo. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar correo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@correoapi.route('/correos/<int:correo_id>', methods=['PUT'])
def updateCorreo(correo_id):
    data = request.get_json()
    correodao = CorreoDao()

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
        if correodao.updateCorreo(correo_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': correo_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el correo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar correo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@correoapi.route('/correos/<int:correo_id>', methods=['DELETE'])
def deleteCorreo(correo_id):
    correodao = CorreoDao()

    try:
        # Usar el retorno de eliminarCorreo para determinar el éxito
        if correodao.deleteCorreo(correo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Correo con ID {correo_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el correo con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar correo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500