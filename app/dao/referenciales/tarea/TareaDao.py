# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TareaDao:

    def getTareas(self):

        tareaSQL = """
        SELECT id, responsable, descripcion, estado
        FROM tarea
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tareaSQL)
            tareas = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': tarea[0], 'responsable': tarea[1], 'descripcion': tarea[2], 'estado': tarea[3]} for tarea in tareas]

        except Exception as e:
            app.logger.error(f"Error al obtener todas las tareas: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getTareaById(self, id):

        tareaSQL = """
        SELECT id, responsable, descripcion, estado
        FROM tarea WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(tareaSQL, (id,))
            tareaEncontrada = cur.fetchone()  # Obtener una sola fila
            if tareaEncontrada:
                return {
                        "id": tareaEncontrada[0],
                        "responsable": tareaEncontrada[1],
                        "descripcion": tareaEncontrada[2],
                        "estado": tareaEncontrada[3]
                    }  # Retornar los datos de la tarea
            else:
                return None  # Retornar None si no se encuentra la tarea
        except Exception as e:
            app.logger.error(f"Error al obtener tarea: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarTarea(self, responsable, descripcion, estado):

        insertTareaSQL = """
        INSERT INTO tarea(responsable, descripcion, estado) VALUES(%s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertTareaSQL, (responsable, descripcion, estado))
            tarea_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return tarea_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar tarea: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateTarea(self, id, responsable, descripcion, estado):

        updateTareaSQL = """
        UPDATE tarea
        SET responsable=%s, descripcion=%s, estado=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateTareaSQL, (responsable, descripcion, estado, id))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar tarea: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteTarea(self, id):

        deleteTareaSQL = """
        DELETE FROM tarea
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteTareaSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar tarea: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()