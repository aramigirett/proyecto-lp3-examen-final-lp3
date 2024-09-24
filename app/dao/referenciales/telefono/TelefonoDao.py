# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TelefonoDao:

    def getTelefono(self):

        telefonoSQL = """
        SELECT id, descripcion
        FROM telefonos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(telefonoSQL)
            telefonos = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': telefono[0], 'descripcion': telefono[1]} for telefono in telefonos]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las telefonos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTelefonoById(self, id):

        telefonoSQL = """
        SELECT id, descripcion
        FROM telefonos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(telefonoSQL, (id,))
            telefonoEncontrada = cur.fetchone() # Obtener una sola fila
            if telefonoEncontrada:
                return {
                        "id": telefonoEncontrada[0],
                        "descripcion": telefonoEncontrada[1]
                    }  # Retornar los datos de telefono
            else:
                return None # Retornar None si no se encuentra el telefono
        except Exception as e:
            app.logger.error(f"Error al obtener telefono: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTelefono(self, descripcion):

        insertTelefonoSQL = """
        INSERT INTO telefonos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertTelefonoSQL, (descripcion,))
            telefono_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return telefono_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar telefono: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateTelefono(self, id, descripcion):

        updateTelefonoSQL = """
        UPDATE telefonos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTelefonoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar telefono: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTelefono(self, id):

        updateTelefonoSQL = """
        DELETE FROM telefonos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTelefonoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar telefono: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()