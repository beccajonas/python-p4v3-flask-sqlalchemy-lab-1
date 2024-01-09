# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    '''
    This line queries a database model named 'Earthquake' to retrieve a specific earthquake 
    record based on the provided 'id'. It uses the SQLAlchemy query API to filter earthquakes 
    by their ID and retrieves the first result.'''

    if earthquake:
        body = earthquake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    
    return make_response(body, status)
    '''
    This line creates an HTTP response using the Flask make_response function. 
    It includes the 'body' (response content) and 'status' (HTTP status code) variables 
    determined in the previous lines. The resulting response is then sent back to the 
    client that made the request.
    '''

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    quakes = [] #array to store dictionary for each quake
    for quake in Earthquake.query.filter(Earthquake.magnitude>=magnitude).all():
        quakes.append(quake.to_dict())
    body = {'count': len(quakes), 'quakes': quakes}
    return make_response(body, 200)
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)
