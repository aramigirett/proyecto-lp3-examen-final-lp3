from flask import current_app as app
from app.conexion.Conexion import Conexion

class EstadoCivilDao:

    def getEstadosCiviles(self):
        estadocivilSQL = """
        SELECT id_estado_civil, estado_civil
        FROM estado_civil
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estadocivilSQL)
            estadosciviles = cur.fetchall()

            # Transformar los datos en una lista de diccionarios
            return [{'id_estado_civil': estadocivil[0], 'estado_civil': estadocivil[1]} for estadocivil in estadosciviles]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los Estados Civiles: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEstadoCivilById(self, id_estado_civil):
        estadocivilSQL = """
        SELECT id_estado_civil, estado_civil
        FROM estado_civil WHERE id_estado_civil=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(estadocivilSQL, (id_estado_civil,))
            estadocivilEncontrada = cur.fetchone()
            if estadocivilEncontrada:
                return {
                    "id_estado_civil": estadocivilEncontrada[0],
                    "estado_civil": estadocivilEncontrada[1]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener el estado civil: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEstadoCivil(self, estado_civil):
        insertEstadoCivilSQL = """
        INSERT INTO estado_civil(estado_civil) VALUES(%s) RETURNING id_estado_civil
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertEstadoCivilSQL, (estado_civil,))
            estadocivil_id = cur.fetchone()[0]
            con.commit()
            return estadocivil_id

        except Exception as e:
            app.logger.error(f"Error al insertar estado civil: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def updateEstadoCivil(self, id_estado_civil, estado_civil):
        updateEstadoCivilSQL = """
        UPDATE estado_civil
        SET estado_civil=%s
        WHERE id_estado_civil=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEstadoCivilSQL, (estado_civil, id_estado_civil))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0

        except Exception as e:
            app.logger.error(f"Error al actualizar Estado Civil: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEstadoCivil(self, id_estado_civil):
        deleteEstadoCivilSQL = """
        DELETE FROM estado_civil
        WHERE id_estado_civil=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEstadoCivilSQL, (id_estado_civil,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0

        except Exception as e:
            app.logger.error(f"Error al eliminar Estado Civil: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()