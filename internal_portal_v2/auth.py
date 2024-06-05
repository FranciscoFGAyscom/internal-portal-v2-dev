from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g, jsonify
)

# Importar modulo de seguridad de werkzeug para trabajar claves encriptadas
from werkzeug.security import generate_password_hash, check_password_hash

# Importar la tabla tbl_user definida en modelo_bd.py
from .modelo_bd import tbl_user

# Importar a la aplicación la BD
from internal_portal_v2 import db

# Importar a la aplicación el Mail
from flask_mail import Message
from internal_portal_v2 import mail

main = Blueprint('main', __name__)

# Esto crea un blueprint llamado 'auth' con un prefijo de URL de '/auth'. 
# Esto significa que todas las rutas definidas en este blueprint tendrán el prefijo de URL '/auth'
var_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Función que genera una cadena aleatoria formada por 6 digitos
import random
@var_bp.route('/generate_random_number', methods=['GET'])
def generate_random_number():
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return random_number


# Esto es lo que hace es crear esta URL: http://127.0.0.1:5000/auth/register mediante BluePrint
@var_bp.route('/register', methods = ['GET', 'POST'])
def funcion_register():  
    print("------> Se ejecuta la funcion funcion_register() en auth.py")
    if request.method == 'POST':
        print("------> Se ejecuta auth.py(POST). Se recuperan los datos del formulario")
        var_username = request.form['username']
        var_password = ""  #request.form['password']    
        print("username=" + var_username)
        print("password=" + var_password)

        # Comprobar que la cuenta usada es una @ayscom.com
        var_search_text = "@ayscom.com"
        if not var_search_text in var_username:
            flash("Solo puedes registrarte con una cuenta de correo Ayscom", "error")
            return render_template('auth/register.html')
        
        # Generar aleatoriamente una contraseña
        var_password = generate_random_number()
        print("------> var_password="+var_password)
                 

        obj_user = tbl_user(var_username, generate_password_hash(var_password))
        print("------> Se crea un objeto obj_user con los datos del formulario de registro")

        print("------> var_password(2)="+var_password)

        # Comprobamos que en la BBDD no existe un usuario con el mismo nombre. De ser asi, se registra. 
        # En caso contrario, devolvemos un error.  
        var_error_en_registro = None        
        var_existe_username = tbl_user.query.filter_by(username = var_username).first()

        print("------> filter_by=" + str(var_existe_username))        

        if var_existe_username == None:
            db.session.add(obj_user)
            db.session.commit()

            # Enviar un correo a la direcccion <var_username> con el mensaje de bienvenida y la contraseña            
            print("------> var_password(3)="+var_password)
            var_msg = Message(
                'Registro en el portal Ayscom',
                body=f'El registro en el portal Ayscom se realizao conrectamente.\nTus datos de acceso son:\n\n Usuario: {var_username}\n Contraseña:{var_password}',
                sender= var_username,
                recipients=['registro@ayscom.com']
            )
            mail.send(var_msg)            

            flash("Usuario registrado correctamente", "info")
            return redirect(url_for('auth.funcion_login'))
        else:
            var_error_en_registro = f'El usuario {var_username} ya esta registrado'

        print("------> Añadimos en flash el error=" + var_error_en_registro)
        flash(var_error_en_registro, "error")   

           
    return render_template('auth/register.html')



# Esto es lo que hace es crear esta URL: http://127.0.0.1:5000/auth/login mediante BluePrint
@var_bp.route('/login', methods = ['GET', 'POST'])
def funcion_login():  
    print("------> Se ejecuta la funcion funcion_login() en auth.py")
    if request.method == 'POST':
        print("------> Se ejecuta auth.py(POST). Se recuperan los datos del formulario")
        var_username = request.form['username']
        var_password = request.form['password']
        print("username=" + var_username)
        print("password=" + var_password)

        var_error_en_login = None
        # Recuperamos en obj_user todos los datos del registo donde el campo username = request.form['username']
        obj_user = tbl_user.query.filter_by(username = var_username).first()

        if obj_user == None:
            var_error_en_login = "Nombre de usuario o contraseña erroneos"
        elif not check_password_hash(obj_user.password, var_password):   
            var_error_en_login = "Nombre de usuario o contraseña erroneos" 

        # Si el usuario y la contraseña son correctos, iniciar sesion
        if var_error_en_login is None:
            session.clear()
            session['user_id_act'] = obj_user.user_id            
            return redirect(url_for('apli.funcion_home'))

        flash(var_error_en_login)    

    return render_template('auth/login.html')


# Recuperar usuario logado en la aplicacion
@var_bp.before_app_request
def funcion_usuario_logado():
    user_id = session.get('user_id_act')
    if user_id is None:
        g.user = None
    else:
        g.user = tbl_user.query.get_or_404(user_id)           


# Cerrar sesion
@var_bp.route('/logout')
def funcion_logout():        
    session.clear()
    return redirect(url_for('index'))       


# Comprueba si hay un usuario dado de alta en la sesion
# Si es asi, se muestran sus tareas. En caso contrario se redirecciona al login
import functools
def funcion_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.funcion_login'))
        return view(**kwargs)
    return wrapped_view


# Cambiar contraseña
@var_bp.route('/change_pass/<int:id>', methods=('GET', 'POST'))
@funcion_login_required
def funcion_cambiar_pass(id):  
    # Recuperamos en obj_user los datos para ese id
    obj_user = tbl_user.query.get_or_404(id)

    if request.method == 'POST':
        var_pass_act = request.form['password_act']
        var_pass_new = request.form['password_new']
        var_pass_new_rep = request.form['password_new_rep']
        
        print("****var_pass_act=" + str(var_pass_act))        
        print("****var_pass_new=" + str(var_pass_new))        
        print("****var_pass_new_rep=" + str(var_pass_new_rep))        
        
        var_error = None
        if not check_password_hash(obj_user.password, var_pass_act):   
            var_error = "La contraseña actual no es correcta"
        
        if not var_pass_new == var_pass_new_rep:
            var_error="La nueva contraseña no coincide"    

        if var_error is not None:
            flash(var_error)
        else:
            obj_user.password = generate_password_hash(var_pass_new)
            db.session.commit()
            flash("Contraseña modificada correctamente")
            return redirect(url_for('apli.funcion_home'))


        print("****var_error=" + str(var_error))        

     
    


    
    return render_template('auth/change_pass.html')