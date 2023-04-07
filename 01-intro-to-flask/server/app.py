#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from models import db, Production

# 3. ✅ Initialize the App

app = Flask(__name__)
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///app.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` 
    
 # 4. ✅ Migrate

# 5. ✅ Navigate to `seed.rb`

@app.before_request
def runs_before():
    current_user = {"user.id": 1, "username": "rose"}
    print(current_user)

# 6. ✅ Routes
@app.route( '/' )
def index():
    return '<h1>Hello World</h1>'

@app.route( '/image' )
def image():
    return '<img src=https://images.unsplash.com/photo-1618826411640-d6df44dd3f7a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Nnx8Y2F0fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=700&q=60 />'

# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route
# 9.✅ Update the route to find a `production` by its `title` and send it to our browser

@app.route('/productions/<string:title>')
def production(title):
    production = Production.query.filter(Production.title == title).first()
    response = {
        'title': production.title,
        'genre': production.genre,
        'image': production.image,
        'director': production.director,
        'description': production.description,
        'budget': production.budget,
        'ongoing': production.ongoing,
    }

    return make_response(jsonify(response), 200)

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
