from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g, send_from_directory
)

# Esta función se utiliza para generar n bytes de datos aleatorios seguros. Es útil para generar claves criptográficas, tokens de sesión, etc.
from os import urandom

# Estas funciones se utilizan para trabajar con rutas de archivos de una manera compatible con diferentes sistemas operativos
from os.path import join, abspath, dirname, basename

# Codifica los datos binarios en una representación de cadena en Base64. Es útil para la transferencia segura de datos binarios 
# en texto (por ejemplo, en correos electrónicos, almacenamiento en JSON, etc.).
from base64 import b64encode

# Este módulo proporciona una forma de codificar y decodificar datos en formato JSON (JavaScript Object Notation)
import json

# Importar la tabla tbl_user definida en modelo_bd.py
from .modelo_bd import tbl_user

# Importar a la aplicación la BD
from internal_portal_v2 import db

# Importar la variable var_root_path
from internal_portal_v2 import var_root_path

# Esto crea un blueprint llamado 'apli' con un prefijo de URL de '/aplicacion'. 
# Esto significa que todas las rutas definidas en este blueprint tendrán el prefijo de URL '/aplicacion'
var_bp = Blueprint('apli', __name__, url_prefix='/')

# Para poder acceder a la aplicación se requiere un usuario logado.
from internal_portal_v2.auth import funcion_login_required

# Esto es lo que hace es crear esta URL: http://127.0.0.1:8080/home mediante BluePrint
@var_bp.route('/home')
@funcion_login_required
def funcion_home():  
    with open(join(var_root_path, 'sites_config.json'), 'r') as f:
        obj_config = json.load(f)    
    return render_template('apli/home.html', param_config=obj_config)

    

