from ..utils.db import db

class Menu(db.Model):
    __tablename__='menus'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    restaurant_id = db.Column(db.Integer(),db.ForeignKey('restaurants.id'))
    products = db.relationship('Product', backref='menu',lazy=True)

    def __repr__(self) -> str:
        return '<Menu {}>'.format(self.name)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
