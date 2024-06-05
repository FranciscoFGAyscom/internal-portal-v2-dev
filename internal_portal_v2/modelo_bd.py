from internal_portal_v2 import db

class tbl_user(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__ (self, username, password):        
        print ("creamos un objeto de la clase user con los datos username=" + username)
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
    