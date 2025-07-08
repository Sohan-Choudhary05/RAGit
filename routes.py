from app import app,db
from flask import jsonify,request
from models import User
from werkzeug.exceptions import BadRequest,NotFound
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask_migrate import Migrate


@app.route('/v1/register',methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return {"message":"Invalid Data"},400
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not email or not username or not password:
        return {"message":"Invalid Data"},400
    user = User(email=email,username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"),201