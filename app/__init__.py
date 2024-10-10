from flask import Flask

app = Flask(__name__)

# Importar referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.cargo.cargo_routes import cargomod 
from app.rutas.referenciales.servicio.servicio_routes import serviciomod 
from app.rutas.referenciales.cliente.cliente_routes import clientemod
from app.rutas.referenciales.empleado.empleado_routes import empleadomod
from app.rutas.referenciales.proyecto.proyecto_routes import proyectomod
from app.rutas.referenciales.material.material_routes import materialmod
from app.rutas.referenciales.proveedor.proveedor_routes import proveedormod
from app.rutas.referenciales.pago.pago_routes import pagomod
from app.rutas.referenciales.equipo.equipo_routes import equipomod
from app.rutas.referenciales.vehiculo.vehiculo_routes import vehiculomod
from app.rutas.referenciales.tarea.tarea_routes import tareamod
from app.rutas.referenciales.beneficio.beneficio_routes import beneficiomod
from app.rutas.referenciales.meta.meta_routes import metamod
from app.rutas.referenciales.producto.producto_routes import productomod

# Registrar referenciales
modulo0 = '/referenciales'
app.register_blueprint(ciumod, url_prefix=f'{modulo0}/ciudad')
app.register_blueprint(cargomod, url_prefix=f'{modulo0}/cargo')  
app.register_blueprint(serviciomod, url_prefix=f'{modulo0}/servicio') 
app.register_blueprint(clientemod, url_prefix=f'{modulo0}/cliente') 
app.register_blueprint(empleadomod, url_prefix=f'{modulo0}/empleado') 
app.register_blueprint(proyectomod, url_prefix=f'{modulo0}/proyecto') 
app.register_blueprint(materialmod, url_prefix=f'{modulo0}/material') 
app.register_blueprint(proveedormod, url_prefix=f'{modulo0}/proveedor')
app.register_blueprint(pagomod, url_prefix=f'{modulo0}/pago')
app.register_blueprint(equipomod, url_prefix=f'{modulo0}/equipo')
app.register_blueprint(vehiculomod, url_prefix=f'{modulo0}/vehiculo')
app.register_blueprint(tareamod, url_prefix=f'{modulo0}/tarea')
app.register_blueprint(beneficiomod, url_prefix=f'{modulo0}/beneficio')
app.register_blueprint(metamod, url_prefix=f'{modulo0}/meta')
app.register_blueprint(productomod, url_prefix=f'{modulo0}/producto')



# APIS v1
version1 = '/api/v1'
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
from app.rutas.referenciales.cargo.cargo_api import cargoapi 
from app.rutas.referenciales.servicio.servicio_api import servicioapi 
from app.rutas.referenciales.cliente.cliente_api import clienteapi
from app.rutas.referenciales.empleado.empleado_api import empleadoapi
from app.rutas.referenciales.proyecto.proyecto_api import proyectoapi
from app.rutas.referenciales.material.material_api import materialapi
from app.rutas.referenciales.proveedor.proveedor_api import proveedorapi
from app.rutas.referenciales.pago.pago_api import pagoapi
from app.rutas.referenciales.equipo.equipo_api import equipoapi
from app.rutas.referenciales.vehiculo.vehiculo_api import vehiculoapi
from app.rutas.referenciales.tarea.tarea_api import tareaapi
from app.rutas.referenciales.beneficio.beneficio_api import beneficioapi
from app.rutas.referenciales.meta.meta_api import metaapi
from app.rutas.referenciales.producto.producto_api import productoapi



app.register_blueprint(ciuapi, url_prefix=version1)
app.register_blueprint(cargoapi, url_prefix=version1)  
app.register_blueprint(servicioapi, url_prefix=version1)  
app.register_blueprint(clienteapi, url_prefix=version1)
app.register_blueprint(empleadoapi, url_prefix=version1)
app.register_blueprint(proyectoapi, url_prefix=version1)
app.register_blueprint(materialapi, url_prefix=version1)
app.register_blueprint(proveedorapi, url_prefix=version1)
app.register_blueprint(pagoapi, url_prefix=version1)
app.register_blueprint(equipoapi, url_prefix=version1)
app.register_blueprint(vehiculoapi, url_prefix=version1)
app.register_blueprint(tareaapi, url_prefix=version1)
app.register_blueprint(beneficioapi, url_prefix=version1)
app.register_blueprint(metaapi, url_prefix=version1)
app.register_blueprint(productoapi, url_prefix=version1)