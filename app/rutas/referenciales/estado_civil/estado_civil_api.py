from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.estado_civil.EstadoCivilDao import EstadoCivilDao

estacivapi = Blueprint('estacivapi', __name__)

# Lista de valores permitidos para estado_civil
VALORES_ESTADO_CIVIL_PERMITIDOS = ['Casado/a', 'Soltero/a', 'Divorciado/a', 'Amancebado', 'Concubinato']

# Trae todos los Estados Civiles
@estacivapi.route('/estadocivil', methods=['GET'])
def getEstadosCiviles():
    estacivdao = EstadoCivilDao()

    try:
        estadosciviles = estacivdao.getEstadosCiviles()

        return jsonify({
            'success': True,
            'data': estadosciviles,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los Estados Civiles: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estacivapi.route('/estadocivil/<int:id>', methods=['GET'])
def getEstadoCivil(id):
    estacivdao = EstadoCivilDao()

    try:
        estado_civil = estacivdao.getEstadoCivilById(id)

        if estado_civil:
            return jsonify({
                'success': True,
                'data': estado_civil,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado civil con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener estado civil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo Estado Civil
@estacivapi.route('/estadocivil', methods=['POST'])
def addEstadoCivil():
    data = request.get_json()
    estacivdao = EstadoCivilDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['estado_civil']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    estado_civil = data['estado_civil'].capitalize()

    # Validar si el valor está permitido por el CHECK
    if estado_civil not in VALORES_ESTADO_CIVIL_PERMITIDOS:
        return jsonify({
            'success': False,
            'error': f'El valor "{estado_civil}" no es válido. Debe ser uno de los siguientes: {", ".join(VALORES_ESTADO_CIVIL_PERMITIDOS)}.'
        }), 400

    try:
        id = estacivdao.guardarEstadoCivil(estado_civil)
        if id is not None:
            return jsonify({
                'success': True,
                'data': {'id': id, 'estado_civil': estado_civil},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el Estado Civil. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar Estado Civil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estacivapi.route('/estadocivil/<int:id>', methods=['PUT'])
def updateEstadoCivil(id):
    data = request.get_json()
    estacivdao = EstadoCivilDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['estado_civil']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    estado_civil = data['estado_civil'].capitalize()

    # Validar si el valor está permitido por el CHECK
    if estado_civil not in VALORES_ESTADO_CIVIL_PERMITIDOS:
        return jsonify({
            'success': False,
            'error': f'El valor "{estado_civil}" no es válido. Debe ser uno de los siguientes: {", ".join(VALORES_ESTADO_CIVIL_PERMITIDOS)}.'
        }), 400

    try:
        if estacivdao.updateEstadoCivil(id, estado_civil):
            return jsonify({
                'success': True,
                'data': {'id': id, 'estado_civil': estado_civil},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado civil con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar Estado Civil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@estacivapi.route('/estadocivil/<int:id>', methods=['DELETE'])
def deleteEstadoCivil(id):
    estacivdao = EstadoCivilDao()

    try:
        # Usar el retorno de deleteEstadoCivil para determinar el éxito
        if estacivdao.deleteEstadoCivil(id):
            return jsonify({
                'success': True,
                'mensaje': f'Estado Civil con ID {id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el estado civil con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar Estado Civil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500