# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EquipoDao:

    def getEquipos(self):

        equipoSQL = """
        SELECT id, nombre, tipo, modelo, estado
        FROM equipo
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(equipoSQL)
            equipos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': equipo[0], 'nombre': equipo[1], 'tipo': equipo[2], 
                     'modelo': equipo[3], 'estado': equipo[4]} for equipo in equipos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los equipos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEquipoById(self, id):

        equipoSQL = """
        SELECT id, nombre, tipo, modelo, estado
        FROM equipo WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(equipoSQL, (id,))
            equipoEncontrado = cur.fetchone()  # Obtener una sola fila
            if equipoEncontrado:
                return {
                    "id": equipoEncontrado[0],
                    "nombre": equipoEncontrado[1],
                    "tipo": equipoEncontrado[2],
                    "modelo": equipoEncontrado[3],
                    "estado": equipoEncontrado[4]
                }  # Retornar los datos del equipo
            else:
                return None  # Retornar None si no se encuentra el equipo
        except Exception as e:
            app.logger.error(f"Error al obtener equipo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEquipo(self, nombre, tipo, modelo, estado):

        insertEquipoSQL = """
        INSERT INTO equipo(nombre, tipo, modelo, estado) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEquipoSQL, (nombre, tipo, modelo, estado,))
            equipo_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return equipo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar equipo: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEquipo(self, id, nombre, tipo, modelo, estado):

        updateEquipoSQL = """
        UPDATE equipo
        SET nombre=%s, tipo=%s, modelo=%s, estado=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEquipoSQL, (nombre, tipo, modelo, estado, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar equipo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEquipo(self, id):

        deleteEquipoSQL = """
        DELETE FROM equipo
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEquipoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar equipo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
