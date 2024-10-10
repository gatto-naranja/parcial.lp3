# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EmpleadoDao:

    def getEmpleados(self):

        empleadoSQL = """
        SELECT id, nombre, apellido, cargo, telefono
        FROM empleado
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(empleadoSQL)
            empleados = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': empleado[0], 'nombre': empleado[1], 'apellido': empleado[2], 
                     'cargo': empleado[3], 'telefono': empleado[4]} for empleado in empleados]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los empleados: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getEmpleadoById(self, id):

        empleadoSQL = """
        SELECT id, nombre, apellido, cargo, telefono
        FROM empleado WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(empleadoSQL, (id,))
            empleadoEncontrado = cur.fetchone()  # Obtener una sola fila
            if empleadoEncontrado:
                return {
                    "id": empleadoEncontrado[0],
                    "nombre": empleadoEncontrado[1],
                    "apellido": empleadoEncontrado[2],
                    "cargo": empleadoEncontrado[3],
                    "telefono": empleadoEncontrado[4]
                }  # Retornar los datos del empleado
            else:
                return None  # Retornar None si no se encuentra el empleado
        except Exception as e:
            app.logger.error(f"Error al obtener empleado: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarEmpleado(self, nombre, apellido, cargo, telefono):

        insertEmpleadoSQL = """
        INSERT INTO empleado(nombre, apellido, cargo, telefono) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertEmpleadoSQL, (nombre, apellido, cargo, telefono,))
            empleado_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return empleado_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar empleado: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateEmpleado(self, id, nombre, apellido, cargo, telefono):

        updateEmpleadoSQL = """
        UPDATE empleado
        SET nombre=%s, apellido=%s, cargo=%s, telefono=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateEmpleadoSQL, (nombre, apellido, cargo, telefono, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar empleado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteEmpleado(self, id):

        deleteEmpleadoSQL = """
        DELETE FROM empleado
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteEmpleadoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar empleado: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
