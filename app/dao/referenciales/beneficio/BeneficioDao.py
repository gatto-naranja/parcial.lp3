# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class BeneficioDao:

    def getBeneficios(self):

        beneficioSQL = """
        SELECT id, nombre, descripcion, duracion
        FROM beneficio
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(beneficioSQL)
            beneficios = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': beneficio[0], 'nombre': beneficio[1], 'descripcion': beneficio[2], 
                     'duracion': beneficio[3]} for beneficio in beneficios]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los beneficios: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getBeneficioById(self, id):

        beneficioSQL = """
        SELECT id, nombre, descripcion, duracion
        FROM beneficio WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(beneficioSQL, (id,))
            beneficioEncontrado = cur.fetchone()  # Obtener una sola fila
            if beneficioEncontrado:
                return {
                    "id": beneficioEncontrado[0],
                    "nombre": beneficioEncontrado[1],
                    "descripcion": beneficioEncontrado[2],
                    "duracion": beneficioEncontrado[3]
                }  # Retornar los datos del beneficio
            else:
                return None  # Retornar None si no se encuentra el beneficio
        except Exception as e:
            app.logger.error(f"Error al obtener beneficio: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarBeneficio(self, nombre, descripcion, duracion):

        insertBeneficioSQL = """
        INSERT INTO beneficio(nombre, descripcion, duracion) 
        VALUES(%s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertBeneficioSQL, (nombre, descripcion, duracion,))
            beneficio_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return beneficio_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar beneficio: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateBeneficio(self, id, nombre, descripcion, duracion):

        updateBeneficioSQL = """
        UPDATE beneficio
        SET nombre=%s, descripcion=%s, duracion=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateBeneficioSQL, (nombre, descripcion, duracion, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar beneficio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteBeneficio(self, id):

        deleteBeneficioSQL = """
        DELETE FROM beneficio
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteBeneficioSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar beneficio: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
