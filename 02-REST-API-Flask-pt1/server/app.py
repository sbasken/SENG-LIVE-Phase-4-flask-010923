#!/usr/bin/env python3

# 📚 Review With Students:
    # API Fundamentals
    # MVC Architecture and Patterns / Best Practices
    # RESTful Routing
    # Serialization
    # Postman

# Set Up:
    # In Terminal, `cd` into `server` and run the following:
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5000
        # flask db init
        # flask db revision --autogenerate -m 'Create tables' 
        # flask db upgrade 
        # python seed.py

# Restful

# | HTTP Verb 	|       Path       	| Description        	|
# |-----------	|:----------------:	|--------------------	|
# | GET       	|   /productions   	| READ all resources 	|
# | GET       	| /productions/:id 	| READ one resource   	|
# | POST      	|   /productions   	| CREATE one resource 	|
# | PATCH/PUT 	| /productions/:id 	| UPDATE one resource	|
# | DELETE    	| /productions/:id 	| DESTROY one resource 	|



from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

# 1. ✅ Import `Api` and `Resource` from `flask_restful`
    # ❓ What do these two classes do at a higher level? 

from flask_restful import Api, Resource 

from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Note: `app.json.compact = False` configures JSON responses to print on indented lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# 2. ✅ Initialize the Api
api = Api(app)

# 3. ✅ Create a Production class that inherits from Resource
class Productions(Resource):
    def get(self):

        production_list = [ production.to_dict() for production in Production.query.all() ]

        return make_response(production_list, 200)
    
    def post(self):
        data = request.get_json()
        new_production = Production(
            title = data['title'],
            genre = data['genre'],
            budget = data['budget'],
            image = data['image'],
            director = data['director'],
            description = data['description'],
            ongoing = data['ongoing'],
        )
        db.session.add(new_production)
        db.session.commit()

        return make_response(new_production.to_dict(), 201)
    
    
api.add_resource(Productions, '/productions')

class CastMembers(Resource):
    def get(self):
        cast_members_list = [ cast_member.to_dict() for cast_member in CastMember.query.all()]
        return make_response(cast_members_list, 200)
    
    def post(self):
        data = request.get_json()
        new_cast = Production(
            name = data['name'],
            role = data['role'],
            production_id = data['production_id']
        )
        db.session.add(new_cast)
        db.session.commit()

        return make_response(new_cast.to_dict(), 201)
    
    
api.add_resource(CastMembers, '/cast_members')

class ProductionByID(Resource):
    def get(self,id):
        production_list = Production.query.filter_by(id=id).first().to_dict()
        return make_response(production_list, 200)

api.add_resource(ProductionByID, '/productions/<int:id>')

# 4. ✅ Create a GET (All) Route

# 5. ✅ Serialization
    # This is great, but there's a cleaner way to do this! Serialization will allow us to easily add our 
    # associations as well.
    # Navigate to `models.py` for Steps 6 - 9.

# 10. ✅ Use our serializer to format our response to be cleaner
   
# 11. ✅ Create a POST Route
   
# 12. ✅ Add the new route to our api with `api.add_resource`

# 13. ✅ Create a GET (One) route
    # 13.1 Build a class called `ProductionByID` that inherits from `Resource`.
    # 13.2 Create a `get` method and pass it the id along with `self`. (This is how we will gain access to 
    # the id from our request)
    # 13.3 Make a query for our production by the `id` and build a `response` to send to the browser.


# 14. ✅ Add the new route to our api with `api.add_resource`