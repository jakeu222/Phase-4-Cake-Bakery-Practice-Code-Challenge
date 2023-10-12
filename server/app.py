#!/usr/bin/env python3
from models import db, Bakeries, Cakes, Cake_Bakeries
from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/bakeries')
def get_bakeries():
    response_dict = [b.to_dict(only=('id','name','address')) for b in Bakeries.query.all()]
    return make_response(response_dict, 200)

@app.get('/bakeries/<int:id>')
def get_bakeries_by_id(id):
    bake = Bakeries.query.filter_by(id=id).first()

    if not bake:
        return make_response({"error": "bakery not found"}, 404)

    return make_response(bake.to_dict(), 200)

@app.delete('/bakeries/<int:id>')
def delete_bakery(id):
    bake = Bakeries.query.filter_by(id=id).first()

    if not bake:
        return make_response({"error": "Bakery not found"}, 404)
    
    db.session.delete(bake)
    db.session.commit()

    return make_response({"message":"Deleted Bakery"}, 226)

@app.get('/cakes')
def get_cakes():
    response_dict = [c.to_dict(only=('id','name','description')) for c in Cakes.query.all()]
    return make_response(response_dict, 200)

@app.post('/cake_bakeries')
def post_cake_bakeries():
    data = request.get_json()
    try:
        new_cake_bakery = Cake_Bakeries(
            price = data['price'],
            cake_id=data['cake_id'],
            bake_id=data['bake_id']

        )
    except Exception:
        return make_response({"errors": ["validation errors"]}, 422)
    db.session.add(new_cake_bakery)
    db.session.commit()
    return make_response(new_cake_bakery.to_dict(only=("price", 'cake_id','bake_id')), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)