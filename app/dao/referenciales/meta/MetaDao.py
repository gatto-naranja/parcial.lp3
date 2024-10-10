# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MetaDao:

    def getMetas(self):

        metaSQL = """
        SELECT id, descripcion, fecha_inicio, fecha_finalizacion, estado
        FROM meta
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(metaSQL)
            metas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': meta[0], 'descripcion': meta[1], 'fecha_inicio': meta[2], 
                     'fecha_finalizacion': meta[3], 'estado': meta[4]} for meta in metas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las metas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMetaById(self, id):

        metaSQL = """
        SELECT id, descripcion, fecha_inicio, fecha_finalizacion, estado
        FROM meta WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(metaSQL, (id,))
            metaEncontrada = cur.fetchone()  # Obtener una sola fila
            if metaEncontrada:
                return {
                    "id": metaEncontrada[0],
                    "descripcion": metaEncontrada[1],
                    "fecha_inicio": metaEncontrada[2],
                    "fecha_finalizacion": metaEncontrada[3],
                    "estado": metaEncontrada[4]
                }  # Retornar los datos de la meta
            else:
                return None  # Retornar None si no se encuentra la meta
        except Exception as e:
            app.logger.error(f"Error al obtener meta: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMeta(self, descripcion, fecha_inicio, fecha_finalizacion, estado):

        insertMetaSQL = """
        INSERT INTO meta(descripcion, fecha_inicio, fecha_finalizacion, estado) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertMetaSQL, (descripcion, fecha_inicio, fecha_finalizacion, estado,))
            meta_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return meta_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar meta: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateMeta(self, id, descripcion, fecha_inicio, fecha_finalizacion, estado):

        updateMetaSQL = """
        UPDATE meta
        SET descripcion=%s, fecha_inicio=%s, fecha_finalizacion=%s, estado=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMetaSQL, (descripcion, fecha_inicio, fecha_finalizacion, estado, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar meta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMeta(self, id):

        deleteMetaSQL = """
        DELETE FROM meta
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMetaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar meta: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
