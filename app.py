"""Flask app for Cupcakes"""
from flask import Flask, redirect, render_template, request, jsonify
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatever'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/cupcakes')
def get_cupcakes():
    all_cupcakes = Cupcake.query.all()
    serialized_cupcakes = [Cupcake.serialize_cupcake(cupcake) for cupcake in all_cupcakes]
    return jsonify(cupcakes = serialized_cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def new_cupcake():
    data = request.json
    flavor = data['flavor']
    rating = data['rating']
    size = data['size']
    image = data['image']
    print(image)

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize_cupcake()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = Cupcake.serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized_cupcake)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    serialized_cupcake = Cupcake.serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=['DELETE'])
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Cupcake deleted")

