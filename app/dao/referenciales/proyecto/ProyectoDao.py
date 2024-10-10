# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProyectoDao:

    def getProyectos(self):

        proyectoSQL = """
        SELECT id, nombre, fecha_inicio, fecha_fin, estado
        FROM proyecto
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proyectoSQL)
            proyectos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': proyecto[0], 'nombre': proyecto[1], 'fecha_inicio': proyecto[2], 
                     'fecha_fin': proyecto[3], 'estado': proyecto[4]} for proyecto in proyectos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los proyectos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProyectoById(self, id):

        proyectoSQL = """
        SELECT id, nombre, fecha_inicio, fecha_fin, estado
        FROM proyecto WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proyectoSQL, (id,))
            proyectoEncontrado = cur.fetchone()  # Obtener una sola fila
            if proyectoEncontrado:
                return {
                    "id": proyectoEncontrado[0],
                    "nombre": proyectoEncontrado[1],
                    "fecha_inicio": proyectoEncontrado[2],
                    "fecha_fin": proyectoEncontrado[3],
                    "estado": proyectoEncontrado[4]
                }  # Retornar los datos del proyecto
            else:
                return None  # Retornar None si no se encuentra el proyecto
        except Exception as e:
            app.logger.error(f"Error al obtener proyecto: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProyecto(self, nombre, fecha_inicio, fecha_fin, estado):

        insertProyectoSQL = """
        INSERT INTO proyecto(nombre, fecha_inicio, fecha_fin, estado) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertProyectoSQL, (nombre, fecha_inicio, fecha_fin, estado,))
            proyecto_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return proyecto_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar proyecto: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateProyecto(self, id, nombre, fecha_inicio, fecha_fin, estado):

        updateProyectoSQL = """
        UPDATE proyecto
        SET nombre=%s, fecha_inicio=%s, fecha_fin=%s, estado=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProyectoSQL, (nombre, fecha_inicio, fecha_fin, estado, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar proyecto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProyecto(self, id):

        deleteProyectoSQL = """
        DELETE FROM proyecto
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteProyectoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar proyecto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
