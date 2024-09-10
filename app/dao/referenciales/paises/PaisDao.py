# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion 

class PaisDao:
    
    def getPaises(self):

        paisSQL = """
        SELECT id, descripcion
        FROM paises
        """
        #objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
          cur.execute(paisSQL)
          #trae datos de db
          lista_paises = cur.fetchall()
          print(lista_paises)
          #retorno de datos
          lista_ordenada = []
          for item in lista_paises:
              lista_ordenada.append({
                  "id": item[0],
                  "descripcion": item[1]
                })
          return lista_ordenada
        except con.Error as e:
           app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def getPaisById(self, id):

        paisSQL = """
        SELECT id, descripcion
        FROM paises WHERE id=%s
        """
        #objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
          cur.execute(paisSQL, (id,))
          #trae datos de db
          paisEncontrada = cur.fetchone()
          #retorno de datos
          return {
                    "id": paisEncontrada[0],
                    "descripcion": paisEncontrada[1]
                }
        except con.Error as e:
             app.logger.info(e)
        finally:
            cur.close()
            con.close()

    def guardarPais(self, descripcion):
        
        insertPaisSQL = """
        INSERT INTO paises(descripcion) VALUES(%s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        #Ejecucion exitosa
        try:
            cur.execute(insertPaisSQL, (descripcion,))
            #se confirma la isercion
            con.commit()

            return True

        #si algo falla aqui
        except con.Error as e:
            app.logger.info(e)
            
        #siempre se va a ejecutar
        finally:
            cur.close()
            con.close()

        return False    
          
    def updatePais(self, id, descripcion):

        updatePaisSQL = """
        UPDATE paises
        SET descripcion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updatePaisSQL, (descripcion, id,))
            # se confirma la insercion
            con.commit()

            return True

        # Si algo fallo entra aqui
        except con.Error as e:
            app.logger.info(e)

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

        return False
    
    def deletePais(self, id):

        updatePaisSQL = """
        DELETE FROM paises
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(updatePaisSQL, (id,))
            # se confirma la insercion
            con.commit()

            return True

        # Si algo fallo entra aqui
        except con.Error as e:
            app.logger.info(e)

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

        return False        
    