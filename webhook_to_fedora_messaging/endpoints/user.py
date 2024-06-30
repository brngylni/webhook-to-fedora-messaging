from flask import Blueprint, Flask, request, Response, Request
from ..database import db
from ..models.user import User
from sqlalchemy_helpers import get_or_create

app = Flask(__name__)
user_endpoint = Blueprint("user_endpoint", __name__)

@user_endpoint.route("/user", methods=["POST"])
def create_user():
    """
        Used for creating a new user by sending a post request to /user/ path.
    """
    
    if not validate_request(request):
        return Response("{'message': 'Bad Request'}", status=400, mimetype='application/json')
    session = db.Session()
    user, created = get_or_create(session, User, username=request.json['username'])
    if not created:
        return Response("{'message': 'User Already Exists'}", status=409, mimetype='application/json')
    else:
        return Response("{'message': 'Created', 'uuid': '%s'}" % user['id'], status=201, mimetype='application/json')
        
    
@user_endpoint.route("/user/search", methods=["GET"])
def get_user():
    
    if not validate_request(request):
        return Response("{'message': 'Bad Request'}", status=400, mimetype='application/json')
    session = db.Session()
    users = session.query(User).filter(User.username.like(request.json['username'])).all()
    if users is None or users == []:
        return Response("{'message': 'Not Found'}", status=404, mimetype='application/json')
    else:
        return Response("{'user_list': "+ users +"}", status=200, mimetype='application/json')
    
    
@user_endpoint.route("/user", methods=["GET"])
def lookup_user():
    if not validate_request(request):
        return Response("{'message': 'Bad Request'}", status=400, mimetype='application/json')
    session = db.Session()
    
    user = session.query(User).filter(User.username == request.json['username']).first()
    if user is None:
        return Response("{'message': 'Not Found'}", status=404, mimetype='application/json')
    else:
        return Response("{'uuid': "+ user.id +", 'username': '"+ user.username +"'}", status=200, mimetype='application/json')
    
    
    
    
def validate_request(request: Request):
    if request.json['username'] is None:
        return False
    return True
    
    