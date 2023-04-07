#!/usr/bin/env python3
# 📚 Review With Students:
    # REST
    # Status codes
    # Error handling 
# Set up:
    # cd into server and run the following in the terminal
    # export FLASK_APP=app.py
    # export FLASK_RUN_PORT=5000
    # flask db init
    # flask db revision --autogenerate -m'Create tables' 
    # flask db upgrade 
    # python seed.py
from flask import Flask, request, make_response, abort
from flask_migrate import Migrate

from flask_restful import Api, Resource

# 1.✅ Import NotFound from werkzeug.exceptions for error handling
from werkzeug.exceptions import NotFound


from models import db, Production, CastMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


api = Api(app)

class Productions(Resource):
    def get(self):
        production_list = [p.to_dict() for p in Production.query.all()]
        
        response = make_response(
            production_list,
            200,
        )

        return response

    def post(self):
        request_json = request.get_json()
       
        new_production = Production(
            title=request_json['title'],
            genre=request_json['genre'],
            budget=request_json['budget'],
            image=request_json['image'],
            director=request_json['director'],
            description=request_json['description'],
            ongoing=request_json['ongoing']
        )

        db.session.add(new_production)
        db.session.commit()

        response_dict = new_production.to_dict()

        response = make_response(
            response_dict,
            201,
        )
        return response
api.add_resource(Productions, '/productions')


class ProductionByID(Resource):
    def get(self,id):
        production = Production.query.filter_by(id=id).first()
# 3.✅ If a production is not found raise the NotFound exception
        if not production:
            abort(404, "Profuction not found, sorry!")
        
        production_dict = production.to_dict()
        response = make_response(
            production_dict,
            200
        )
        
        return response

# 4.✅ Patch
    # 4.1 Create a patch method that takes self and id
    # 4.2 Query the Production from the id
    # 4.3 If the production is not found raise the NotFound exception
    # 4.4 Loop through the request.form object and update the productions attributes. Note: Be cautions of the data types to avoid errors.
    # 4.5 add and commit the updated production 
    # 4.6 Create and return the response
  
# 5.✅ Delete
    # 5.1 Create a delete method, pass it self and the id
    # 5.2 Query the Production 
    # 5.3 If the production is not found raise the NotFound exception
    # 5.4 delete the production and commit 
    # 5.5 create a response with the status of 204 and return the response 
  

   
api.add_resource(ProductionByID, '/productions/<int:id>')

# 2.✅ use the @app.errorhandler() decorator to handle Not Found
    # 2.1 Create the decorator and pass it NotFound
    # 2.2 Use make_response to create a response with a message and the status 404
    # 2.3 return t he response


# To run the file as a script
# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

#Student Exercises 
class CastMembers(Resource):
    def get(self):
        cast_members_list = [cast_member.to_dict() for cast_member in CastMember.query.all()]
    
        response = make_response(
            cast_members_list,
            200
        )
        return response

    def post(self):
        request_json = request.get_json()
        new_cast = CastMember(
            name=request_json['name'],
            role=request_json['role'],
            production_id=request_json['production_id']
        )
        db.session.add(new_cast)
        db.session.commit()

        response_dict = new_cast.to_dict()
        
        response = make_response(
            response_dict,
            201
        )
        return response

api.add_resource(CastMembers, '/cast_members')

class CastMemberByID(Resource):
    def get(self, id):
        cast_member = CastMember.query.filter_by(id=id).first()
        if not cast_member:
            abort(404, 'The cast member you are looking for was not found')
        response = make_response(
            cast_member.to_dict(),
            200
        )

        return response
api.add_resource(CastMemberByID, '/cast_members/<int:id>')

@app.errorhandler(NotFound)
def handle_not_found(e):
    response =  make_response("Not Found: Sorry the resource not found :(", 404)
    return response