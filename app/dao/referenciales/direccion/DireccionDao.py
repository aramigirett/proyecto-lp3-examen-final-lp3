# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DireccionDao:

    def getDirecciones(self):

        direccionSQL = """
        SELECT id, descripcion
        FROM direcciones
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(direccionSQL)
            direcciones = cur.fetchall() # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': direccion[0], 'descripcion': direccion[1]} for direccion in direcciones]

        except Exception as e:
            app.logger.error(f"Error al obtener todos las direcciones: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getDireccionById(self, id):

        direccionSQL = """
        SELECT id, descripcion
        FROM direcciones WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(direccionSQL, (id,))
            direccionEncontrada = cur.fetchone() # Obtener una sola fila
            if direccionEncontrada:
                return {
                        "id": direccionEncontrada[0],
                        "descripcion": direccionEncontrada[1]
                    }  # Retornar los datos de direccion
            else:
                return None # Retornar None si no se encuentra la direccion
        except Exception as e:
            app.logger.error(f"Error al obtener direccion: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarDireccion(self, descripcion):

        insertDireccionSQL = """
        INSERT INTO direcciones(descripcion) VALUES(%s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertDireccionSQL, (descripcion,))
            direccion_id = cur.fetchone()[0]
            con.commit() # se confirma la insercion
            return direccion_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar direccion: {str(e)}")
            con.rollback() # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateDireccion(self, id, descripcion):

        updateDireccionSQL = """
        UPDATE direcciones
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDireccionSQL, (descripcion, id,))
            filas_afectadas = cur.rowcount # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0 # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar direccion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteDireccion(self, id):

        updateDireccionSQL = """
        DELETE FROM direcciones
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateDireccionSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar direccion: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()