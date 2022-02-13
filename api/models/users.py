from ..utils.db import db


class User(db.Model):
    # specify the table name
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(25),nullable=False)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(120),nullable=False,unique=True)
    password_hash = db.Column(db.String(128),nullable=False)
    is_restaurant_employee = db.Column(db.Boolean(),default=False)
    is_active = db.Column(db.Boolean(),default=True)
    restaurants = db.relationship('Restaurant',backref='staff', lazy=True)
    orders = db.relationship('Order',backref='customer',lazy=True)

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)

    # save user to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

