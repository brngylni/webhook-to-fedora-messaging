from flask import Blueprint, Flask, request, Response
from ..database import db
from ..models.user import User
from sqlalchemy_helpers import get_or_create

app = Flask(__name__)
user_endpoint = Blueprint("user_endpoint", __name__)

@user_endpoint.route("/user/", methods=["POST"])
def create_user():
    """
        Used for creating a new user by sending a post request to /user/ path.
    """
    
    if request.json['username'] is None:
        return Response("{'message': 'Bad Request'}", status=400, mimetype='application/json')
    
    session = db.Session()
    
    user, created = get_or_create(User, username=request.json['username'])
    if not created:
        return Response("{'message': 'User Already Exists'}", status=409, mimetype='application/json')
    else:
        return Response("{'message': 'Created', 'uuid': '%s'}" % user['id'], status=201, mimetype='application/json')
        
    
    
    