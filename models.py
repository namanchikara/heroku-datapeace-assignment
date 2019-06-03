from app import db

class User(db.Model):

    __tablename__ = 'datapeace_users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip = db.Column(db.Integer)
    email = db.Column(db.String(255))
    web = db.Column(db.String(255))
    age = db.Column(db.Integer)

    def __init__(self, id, first_name, last_name, company_name, city, state, zip, email, web, age):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.city = city
        self.state = state
        self.zip = zip
        self.email = email
        self.web = web
        self.age = age

    def __repr__(self):
        return str({c.name: getattr(self, c.name) for c in self.__table__.columns})
