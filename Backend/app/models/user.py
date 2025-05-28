from app.extensions import db
from flask_security import UserMixin, RoleMixin
import uuid

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


# Define the Order model
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    days_for_shipping_real = db.Column(db.Integer)
    days_for_shipment_scheduled = db.Column(db.Integer)
    benefit_per_order = db.Column(db.Float)
    sales_per_customer = db.Column(db.Float)
    delivery_status = db.Column(db.String(50))
    late_delivery_risk = db.Column(db.Integer)
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String(100))
    customer_city = db.Column(db.String(100))
    customer_country = db.Column(db.String(100))
    customer_email = db.Column(db.String(100))
    customer_fname = db.Column(db.String(100))
    customer_id = db.Column(db.Integer)
    customer_lname = db.Column(db.String(100))
    customer_password = db.Column(db.String(100))
    customer_segment = db.Column(db.String(50))
    customer_state = db.Column(db.String(100))
    customer_street = db.Column(db.String(200))
    customer_zipcode = db.Column(db.Float, nullable=True)
    department_id = db.Column(db.Integer)
    department_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    market = db.Column(db.String(100))
    order_city = db.Column(db.String(100))
    order_country = db.Column(db.String(100))
    order_customer_id = db.Column(db.Integer)
    order_date = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, unique=True)
    order_item_cardprod_id = db.Column(db.Integer)
    order_item_discount = db.Column(db.Float)
    order_item_discount_rate = db.Column(db.Float)
    order_item_id = db.Column(db.Integer, unique=True)
    order_item_product_price = db.Column(db.Float)
    order_item_profit_ratio = db.Column(db.Float)
    order_item_quantity = db.Column(db.Integer)
    sales = db.Column(db.Float)
    order_item_total = db.Column(db.Float)
    order_profit_per_order = db.Column(db.Float)
    order_region = db.Column(db.String(100))
    order_state = db.Column(db.String(100))
    order_status = db.Column(db.String(50))
    order_zipcode = db.Column(db.Float, nullable=True)
    product_card_id = db.Column(db.Integer)
    product_category_id = db.Column(db.Integer)
    product_description = db.Column(db.Text, nullable=True)
    product_image = db.Column(db.String(200))
    product_name = db.Column(db.String(200))
    product_price = db.Column(db.Float)
    product_status = db.Column(db.Integer)
    shipping_date = db.Column(db.DateTime)
    shipping_mode = db.Column(db.String(50))

    def __repr__(self):
        return f"<Order {self.order_id}>"


# # Define SQLAlchemy Models (Normalized Schema)
# class Customer(db.Model):
#     __tablename__ = 'customers'
#     customer_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(100), nullable=False)
#     customer_segment = db.Column(db.String(50), nullable=False)
#     location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)

# class Location(db.Model):
#     __tablename__ = 'locations'
#     location_id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(100), nullable=False)
#     country = db.Column(db.String(100), nullable=False)
#     state = db.Column(db.String(100), nullable=True)
#     street = db.Column(db.String(200), nullable=True)
#     zipcode = db.Column(db.Float, nullable=True)
#     latitude = db.Column(db.Float, nullable=True)
#     longitude = db.Column(db.Float, nullable=True)

# class Department(db.Model):
#     __tablename__ = 'departments'
#     department_id = db.Column(db.Integer, primary_key=True)
#     department_name = db.Column(db.String(100), nullable=False)

# class Category(db.Model):
#     __tablename__ = 'categories'
#     category_id = db.Column(db.Integer, primary_key=True)
#     category_name = db.Column(db.String(100), nullable=False)
#     department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)

# class Product(db.Model):
#     __tablename__ = 'products'
#     product_id = db.Column(db.Integer, primary_key=True)
#     product_name = db.Column(db.String(200), nullable=False)
#     product_price = db.Column(db.Float, nullable=False)
#     product_status = db.Column(db.Integer, nullable=False)
#     product_image = db.Column(db.String(500), nullable=True)
#     category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)

# class Order(db.Model):
#     __tablename__ = 'orders'
#     order_id = db.Column(db.Integer, primary_key=True)
#     customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
#     order_date = db.Column(db.DateTime, nullable=False)
#     order_status = db.Column(db.String(50), nullable=False)
#     order_city = db.Column(db.String(100), nullable=False)
#     order_country = db.Column(db.String(100), nullable=False)
#     order_state = db.Column(db.String(100), nullable=True)
#     order_region = db.Column(db.String(100), nullable=True)
#     order_zipcode = db.Column(db.Float, nullable=True)
#     market = db.Column(db.String(100), nullable=False)

# class OrderItem(db.Model):
#     __tablename__ = 'order_items'
#     order_item_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     discount = db.Column(db.Float, nullable=False)
#     discount_rate = db.Column(db.Float, nullable=False)
#     total = db.Column(db.Float, nullable=False)
#     profit_ratio = db.Column(db.Float, nullable=False)
#     profit_per_order = db.Column(db.Float, nullable=False)

# class ShippingDetail(db.Model):
#     __tablename__ = 'shipping_details'
#     shipping_id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
#     days_real = db.Column(db.Integer, nullable=False)
#     days_scheduled = db.Column(db.Integer, nullable=False)
#     delivery_status = db.Column(db.String(50), nullable=False)
#     late_delivery_risk = db.Column(db.Integer, nullable=False)
#     shipping_mode = db.Column(db.String(50), nullable=False)
#     shipping_date = db.Column(db.DateTime, nullable=False)

from flask_security import SQLAlchemyUserDatastore
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
