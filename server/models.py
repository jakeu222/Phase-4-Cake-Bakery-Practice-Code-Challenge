from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Bakeries(db.Model, SerializerMixin):
    __tablename__ = "bakeries_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String,nullable=False)

    cake_bake_bakeries=db.relationship('Cake_Bakeries', back_populates='bakeries_feild')

class Cakes(db.Model, SerializerMixin):
    __tablename__ = "cakes_table"

    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    cake_bake_cakes = db.relationship('Cake_Bakeries', back_populates='cakes_feild')

class Cake_Bakeries(db.Model, SerializerMixin):
    __tablename__ = "cake_bakeries_table"

    id = db.Column(db.Integer,  primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    @validates('price')
    def validate_price(self, key, price):
        if 1 <= price <= 1000:
            return price
        else:
            raise ValueError("Not a valid price!")


    created_at = db.Column(db.DateTime, nullable=False)

    updated_at = db.Column(db.DateTime, nullable=False)

    bake_id = db.Column(db.Integer, db.ForeignKey('bakeries_table.id'), nullable=False)
    bakeries_feild=db.relationship('Bakeries', back_populates='cake_bake_bakeries')

    cake_id = db.Column(db.Integer, db.ForeignKey('cakes_table.id'), nullable=False)
    cakes_feild=db.relationship('Cakes', back_populates='cake_bake_cakes')

    serialize_rules=('-bakeries_feild', '-cakes_feild.cake_bake_cakes')
      