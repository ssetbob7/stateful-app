from aciapps import db

class Login_User(db.Model):
    user = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self,user,password,email):
        self.user = user
        self.password = password
        self.email = email
