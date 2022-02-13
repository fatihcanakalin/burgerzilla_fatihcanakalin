from ..utils.db import db

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    description = db.Column(db.String(120),nullable=False)
    menu_id = db.Column(db.Integer(),db.ForeignKey('menus.id'))
    orders = db.relationship('Order',backref='product',lazy=True)


    def __repr__(self) -> str:
        return "<Product {}>".format(self.name)


    # save to database
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


