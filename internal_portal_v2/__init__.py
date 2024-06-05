# Configuraciones básicas de la aplicacion

# Importar Flask
from flask import Flask, render_template, send_from_directory

# Importar SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Importar flask_mail
from flask_mail import Mail

# Esta función se utiliza para generar n bytes de datos aleatorios seguros. Es útil para generar claves criptográficas, tokens de sesión, etc.
from os import urandom

# Estas funciones se utilizan para trabajar con rutas de archivos de una manera compatible con diferentes sistemas operativos
from os.path import join, abspath, dirname, basename

# Codifica los datos binarios en una representación de cadena en Base64. Es útil para la transferencia segura de datos binarios 
# en texto (por ejemplo, en correos electrónicos, almacenamiento en JSON, etc.).
from base64 import b64encode

# Este módulo proporciona una forma de codificar y decodificar datos en formato JSON (JavaScript Object Notation)
import json

import os
# Definimos la variable var_root_path que se puede usar en otros py usando "from internal_portal_v2 import root_path"
var_root_path = os.path.dirname(os.path.abspath(__file__))

# Crear la extensión SQLAlchemy
db = SQLAlchemy()
POSTGRESQL = "postgresql+psycopg2://postgres:qa@localhost:5432/internal_portal_db"

# Crear la extensión mail
mail = Mail()

# Definición de la aplicacion internal portal -----------------------------------------------------------------
def crear_aplicacion_internal_portal():
    app = Flask(__name__)  

    # Configuración de la aplicacion
        # Modo DEBUG activado
        # Clave secreta aplicacion
        # BBDD que usa la aplicacion
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY =b64encode(urandom(125)),  
        SESSION_COOKIE_SAMESITE = "Strict",     
        SQLALCHEMY_DATABASE_URI = POSTGRESQL,     
        MAIL_SERVER='sandbox.smtp.mailtrap.io',
        MAIL_PORT = 2525,
        MAIL_USERNAME = '2079c58274dea6',
        MAIL_PASSWORD = '25a2fe11a34eba',
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False
    )

    # Inicializar la aplicación con la extensión SQLAlchemy    
    db.init_app(app)
        
    # Inicializar la aplicación de correo    
    mail.init_app(app)

    # Configurar idioma local
    import locale
    locale.setlocale(locale.LC_ALL, 'es_ES')

    # Registrar Blueprint llamado 'apli' definido en el fichero apli.py
    from . import apli
    app.register_blueprint(apli.var_bp)

    # Registrar Blueprint llamado 'auth' definido en el fichero auth.py
    from . import auth
    app.register_blueprint(auth.var_bp)

    # Definimos la ruta y la funcion principal
    @app.route('/')    
    def index():        
        return render_template('index.html')
    
    @app.route('/favicon.ico', methods=['GET'])
    def favicon():
        print("----->"+app.root_path)
        return send_from_directory(join(var_root_path, 'static', 'img'), 'favicon.png', mimetype='image/vnd.microsoft.icon')
        
    # Migra los modelos de datos de la aplicacion a la BBDD
    # Esto lo que hace es traducir a la BBDD los modelos de objetos de BBDD que se definen en modelo_db.py
    print("------>  Sincronizamos ORM con BBDD")
    with app.app_context():
        db.create_all()                

    return app
 