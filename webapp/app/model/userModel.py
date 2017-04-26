from app.dao import daoPool

db = daoPool.sqlDAO

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    access_token = db.Column(db.String(120), nullable=True)
    refresh_token = db.Column(db.String(120), nullable=True)

    def __init__(self, userame, email, access_token, refresh_token):
            self.username = userame
            self.email = email
            self.access_token = access_token
            self.refresh_token = refresh_token

    def __repr__(self):
        return '<User %r>' % self.username

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}



