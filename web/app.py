from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.invoker
users = db["users"]

def UserExist(username):
  if users.find({"username":username}).count()==0:
    return False
  else:
    return True
class Register(Resource):
  def post(self):
    postedData = request.get_json()

    username = postedData["username"]
    password = postedData["password"]

    if UserExist(username):
      retJson = {
        "status": 301,
        "msg": "Invalid username"
      }
      return jsonify(retJson)

      hash_pw = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())

      users.insert({
        "username": username,
        "password": hash_pw,
        "tokens": 4
      })

      retJson = {
        "status": 200,
        "msg": "You successfully signed up for this API"
      }
      return jsonify(retJson)

