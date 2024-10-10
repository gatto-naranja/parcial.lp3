# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProductoDao:

    def getProductos(self):

        productoSQL = """
        SELECT id, nombre, descripcion, precio, stock
        FROM producto
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(productoSQL)
            productos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': producto[0], 'nombre': producto[1], 'descripcion': producto[2], 
                     'precio': producto[3], 'stock': producto[4]} for producto in productos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los productos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProductoById(self, id):

        productoSQL = """
        SELECT id, nombre, descripcion, precio, stock
        FROM producto WHERE id=%s
        """
        # objeto conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(productoSQL, (id,))
            productoEncontrado = cur.fetchone()  # Obtener una sola fila
            if productoEncontrado:
                return {
                    "id": productoEncontrado[0],
                    "nombre": productoEncontrado[1],
                    "descripcion": productoEncontrado[2],
                    "precio": productoEncontrado[3],
                    "stock": productoEncontrado[4]
                }  # Retornar los datos del producto
            else:
                return None  # Retornar None si no se encuentra el producto
        except Exception as e:
            app.logger.error(f"Error al obtener producto: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProducto(self, nombre, descripcion, precio, stock):

        insertProductoSQL = """
        INSERT INTO producto(nombre, descripcion, precio, stock) 
        VALUES(%s, %s, %s, %s) RETURNING id
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        # Ejecucion exitosa
        try:
            cur.execute(insertProductoSQL, (nombre, descripcion, precio, stock,))
            producto_id = cur.fetchone()[0]
            con.commit()  # se confirma la insercion
            return producto_id

        # Si algo fallo entra aqui
        except Exception as e:
            app.logger.error(f"Error al insertar producto: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        # Siempre se va ejecutar
        finally:
            cur.close()
            con.close()

    def updateProducto(self, id, nombre, descripcion, precio, stock):

        updateProductoSQL = """
        UPDATE producto
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProductoSQL, (nombre, descripcion, precio, stock, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar producto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProducto(self, id):

        deleteProductoSQL = """
        DELETE FROM producto
        WHERE id=%s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteProductoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar producto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
