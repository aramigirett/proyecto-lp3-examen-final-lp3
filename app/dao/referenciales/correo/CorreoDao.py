# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CorreoDao:

    def getCorreos(self):

        correoSQL = """
        SELECT id, descripcion
        FROM correos
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(correoSQL)
            correos = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': correo[0], 'descripcion': correo[1]} for correo in correos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los correos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getCorreoById(self, id):

        correoSQL = """
        SELECT id, descripcion
        FROM correos WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(correoSQL, (id,))
            correoEncontrada = cur.fetchone() # Obtener una sola fila
            if correoEncontrada:
                return {
                        "id": correoEncontrada[0],
                        "descripcion": correoEncontrada[1]
                    }  # Retornar los datos de correos
            else:
                return None # Retornar None si no se encuentra el correo
        except Exception as e:
            app.logger.error(f"Error al obtener correo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarCorreo(self, descripcion):

        insertCorreoSQL = """
        INSERT INTO correos(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertCorreoSQL, (descripcion,))
            correo_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return correo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar correo: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateCorreo(self, id, descripcion):

        updateCorreoSQL = """
        UPDATE correos
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCorreoSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar correo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteCorreo(self, id):

        updateCorreoSQL = """
        DELETE FROM correos
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateCorreoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar correo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()