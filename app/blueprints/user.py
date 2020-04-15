from flask import Blueprint, request, make_response, jsonify
from datetime import datetime as dt
from .. import db
from ..models.user import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/test')
def test():
    return "TEST"

@user_blueprint.route('/user',methods=['GET'])
def create_user():
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        new_user = User(
            username=username,
            email=email,
            created=dt.now()
        )
        db.session.add(new_user)
        db.session.commit()
    return make_response(f"successfully created!")

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    print(users)
    return jsonify(users)
