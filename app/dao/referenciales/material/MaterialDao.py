# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MaterialDao:

    def getMateriales(self):

        materialSQL = """
        SELECT id, nombre, descripcion, costo
        FROM material
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materialSQL)
            materiales = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': material[0], 'nombre': material[1], 'descripcion': material[2], 
                     'costo': material[3]} for material in materiales]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los materiales: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getMaterialById(self, id):

        materialSQL = """
        SELECT id, nombre, descripcion, costo
        FROM material WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(materialSQL, (id,))
            materialEncontrado = cur.fetchone()  # Obtener una sola fila
            if materialEncontrado:
                return {
                    "id": materialEncontrado[0],
                    "nombre": materialEncontrado[1],
                    "descripcion": materialEncontrado[2],
                    "costo": materialEncontrado[3]
                }  # Retornar los datos del material
            else:
                return None  # Retornar None si no se encuentra el material
        except Exception as e:
            app.logger.error(f"Error al obtener material: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarMaterial(self, nombre, descripcion, costo):

        insertMaterialSQL = """
        INSERT INTO material(nombre, descripcion, costo) 
        VALUES(%s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertMaterialSQL, (nombre, descripcion, costo,))
            material_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return material_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar material: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateMaterial(self, id, nombre, descripcion, costo):

        updateMaterialSQL = """
        UPDATE material
        SET nombre=%s, descripcion=%s, costo=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateMaterialSQL, (nombre, descripcion, costo, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar material: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteMaterial(self, id):

        deleteMaterialSQL = """
        DELETE FROM material
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteMaterialSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar material: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
