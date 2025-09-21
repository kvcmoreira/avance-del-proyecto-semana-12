from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_usuario, nombre, email, password):
        self.id = id_usuario  # Flask-Login usa `id`
        self.nombre = nombre
        self.email = email
        self.password = password
