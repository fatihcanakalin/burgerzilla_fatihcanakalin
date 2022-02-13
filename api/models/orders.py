from ..utils.db import db
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = 'pending'
    PREPARING = 'preparing'
    ON_THE_WAY= 'on_the_way'
    DELIVERED = 'delivered'
    CANCELED_BY_RESTAURANT = 'canceled_by_restaurant'
    CANCELED_BY_CUSTOMER = 'canceled_by_customer'




class Order(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer(),primary_key=True)
    checkout_time = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer(),nullable=False)
    order_status = db.Column(db.Enum(OrderStatus),default=OrderStatus.PENDING)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))


    def __repr__(self) -> str:
        return "<Order {}>".format(self.id)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)



