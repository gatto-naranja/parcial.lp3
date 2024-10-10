# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class VehiculoDao:

    def getVehiculos(self):

        vehiculoSQL = """
        SELECT id, marca, modelo, año, matricula
        FROM vehiculo
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL)
            vehiculos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': vehiculo[0], 'marca': vehiculo[1], 'modelo': vehiculo[2], 
                     'año': vehiculo[3], 'matricula': vehiculo[4]} for vehiculo in vehiculos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los vehiculos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getVehiculoById(self, id):

        vehiculoSQL = """
        SELECT id, marca, modelo, año, matricula
        FROM vehiculo WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(vehiculoSQL, (id,))
            vehiculoEncontrado = cur.fetchone()  # Obtener una sola fila
            if vehiculoEncontrado:
                return {
                    "id": vehiculoEncontrado[0],
                    "marca": vehiculoEncontrado[1],
                    "modelo": vehiculoEncontrado[2],
                    "año": vehiculoEncontrado[3],
                    "matricula": vehiculoEncontrado[4]
                }  # Retornar los datos del vehiculo
            else:
                return None  # Retornar None si no se encuentra el vehiculo
        except Exception as e:
            app.logger.error(f"Error al obtener vehiculo: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarVehiculo(self, marca, modelo, año, matricula):

        insertVehiculoSQL = """
        INSERT INTO vehiculo(marca, modelo, año, matricula) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertVehiculoSQL, (marca, modelo, año, matricula,))
            vehiculo_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return vehiculo_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar vehiculo: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateVehiculo(self, id, marca, modelo, año, matricula):

        updateVehiculoSQL = """
        UPDATE vehiculo
        SET marca=%s, modelo=%s, año=%s, matricula=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateVehiculoSQL, (marca, modelo, año, matricula, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteVehiculo(self, id):

        deleteVehiculoSQL = """
        DELETE FROM vehiculo
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteVehiculoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar vehiculo: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
