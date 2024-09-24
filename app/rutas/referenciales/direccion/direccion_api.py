from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.direccion.DireccionDao import DireccionDao

direapi = Blueprint('direapi', __name__)

# Trae todas las direcciones
@direapi.route('/direcciones', methods=['GET'])
def getDirecciones():
    direcciondao = DireccionDao()

    try:
        direcciones = direcciondao.getDirecciones()

        return jsonify({
            'success': True,
            'data': direcciones,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las direcciones: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@direapi.route('/direcciones/<int:direccion_id>', methods=['GET'])
def getDireccion(direccion_id):
    direcciondao = DireccionDao()

    try:
        direccion = direcciondao.getDireccionById(direccion_id)

        if direccion:
            return jsonify({
                'success': True,
                'data': direccion,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la direccion con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener direccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva direccion
@direapi.route('/direcciones', methods=['POST'])
def addDireccion():
    data = request.get_json()
    direcciondao = DireccionDao()

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
        direccion_id = direcciondao.guardarDireccion(descripcion)
        if direccion_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': direccion_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la direccion. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar direccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@direapi.route('/direcciones/<int:direccion_id>', methods=['PUT'])
def updateDireccion(direccion_id):
    data = request.get_json()
    direcciondao = DireccionDao()

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
        if direcciondao.updateDireccion(direccion_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': direccion_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la direccion con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar direccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@direapi.route('/direcciones/<int:direccion_id>', methods=['DELETE'])
def deleteDireccion(direccion_id):
    direcciondao = DireccionDao()

    try:
        # Usar el retorno de eliminarDireccion para determinar el éxito
        if direcciondao.deleteDireccion(direccion_id):
            return jsonify({
                'success': True,
                'mensaje': f'Direccion con ID {direccion_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la direccion con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar direccion: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
  