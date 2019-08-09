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
  if users.find({"username":username}).count() == 0:
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

    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    users.insert({
      "username": username,
      "password": hashed_pw,
      "tokens": 4
    })

    retJson = {
      "status": 200,
      "msg": "You successfully signed up for this API"
    }
    return jsonify(retJson)

def verifyPw(username, password):
  if not UserExist(username):
    return False

  hashed_pw = users.find({
    "username":username
  })[0]["password"]

  if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
    return True
  else:
    return False

def generateReturnDictionary(status, msg):
  retJson = {
    "status": status,
    "msg": msg
  }
  return retJson

def verifyCredentials(username, password):
  if not UserExist(username):
    return generateReturnDictionary(301, "Invalid username"), True

  correct_pw = verifyPw(username, password)

  if not correct_pw:
    return generateReturnDictionary(302, "Invalid password"), True

  return None, False

class Classify(Resource):
  def post(self):
    postedData = request.get_json()

    username = postedData["username"]
    password = postedData["password"]
    url = postedData["url"]

    retJson, error = verifyCredentials(username, password)
    if error:
      return jsonify(retJson)

    tokens = users.find({
      "username":username
    })[0]["tokens"]

    if tokens <=0:
      return jsonify(generateReturnDictionary(303, "Not Enough Tokens"))

    r = requests.get(url)
    retJson = {}
    with open("temp.jpg", "wb") as f:
      f.write(r.content)
      proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=temp.jpg', shell=True)
      proc.communicate()[0]
      proc.wait()
      with open("text.txt") as g:
        retJson = json.load(g)

      users.update({
        "username": username
      }, {
        "$set":{
          "tokens": tokens-1
        }
      })
    return retJson

class Refill(Resource):
  def post(self):
    postedData = request.get_json()

    username = postedData["username"]
    password = postedData["admin_pw"]
    amount = postedData["amount"]

    if not UserExist(username):
      return jsonify( generateReturnDictionary(301, "Invalid username"))

    correct_pw = "bambang"

    if not password == correct_pw:
      return jsonify( generateReturnDictionary(304, "Invalid administrator password"))

    users.update({
      "username": username
    },{
      "$set":{
        "tokens": amount
      }
    })

    return jsonify( generateReturnDictionary(200, "Refilled successfully"))

api.add_resource(Register, "/register")
api.add_resource(Classify, "/classify")
api.add_resource(Refill, "/refill")

if __name__ == "__main__":
  app.run(host="0.0.0.0")