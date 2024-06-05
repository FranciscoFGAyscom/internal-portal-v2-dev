# Importamos la aplicación
from internal_portal_v2 import crear_aplicacion_internal_portal

# if verificar si el script se está ejecutando como el programa principal o si ha sido importado como un módulo en otro script.
# La función app se ejecutará solo si el script se ejecuta como programa principal.
if __name__ == '__main__':
    app = crear_aplicacion_internal_portal()
    app.run('0.0.0.0', 8080)
    