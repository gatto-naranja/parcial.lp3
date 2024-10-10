# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PagoDao:

    def getPagos(self):

        pagoSQL = """
        SELECT id, descripcion, monto_pagado, fecha_pago, metodo_pago
        FROM pago
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pagoSQL)
            pagos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': pago[0], 'descripcion': pago[1], 'monto_pagado': pago[2], 
                     'fecha_pago': pago[3], 'metodo_pago': pago[4]} for pago in pagos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los pagos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getPagoById(self, id):

        pagoSQL = """
        SELECT id, descripcion, monto_pagado, fecha_pago, metodo_pago
        FROM pago WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(pagoSQL, (id,))
            pagoEncontrado = cur.fetchone()  # Obtener una sola fila
            if pagoEncontrado:
                return {
                    "id": pagoEncontrado[0],
                    "descripcion": pagoEncontrado[1],
                    "monto_pagado": pagoEncontrado[2],
                    "fecha_pago": pagoEncontrado[3],
                    "metodo_pago": pagoEncontrado[4]
                }  # Retornar los datos del pago
            else:
                return None  # Retornar None si no se encuentra el pago
        except Exception as e:
            app.logger.error(f"Error al obtener pago: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarPago(self, descripcion, monto_pagado, fecha_pago, metodo_pago):

        insertPagoSQL = """
        INSERT INTO pago(descripcion, monto_pagado, fecha_pago, metodo_pago) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertPagoSQL, (descripcion, monto_pagado, fecha_pago, metodo_pago,))
            pago_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return pago_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar pago: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updatePago(self, id, descripcion, monto_pagado, fecha_pago, metodo_pago):

        updatePagoSQL = """
        UPDATE pago
        SET descripcion=%s, monto_pagado=%s, fecha_pago=%s, metodo_pago=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updatePagoSQL, (descripcion, monto_pagado, fecha_pago, metodo_pago, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar pago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deletePago(self, id):

        deletePagoSQL = """
        DELETE FROM pago
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deletePagoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar pago: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
