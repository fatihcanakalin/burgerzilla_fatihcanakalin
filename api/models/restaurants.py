from ..utils.db import db


class Restaurant(db.Model):
    __tablename__='restaurants'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(250),nullable=False)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    menus = db.relationship('Menu',backref='restaurant_name',lazy=True)

    def __repr__(self) -> str:
        return "<Restaurant {}>".format(self.name)


    def save(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)


