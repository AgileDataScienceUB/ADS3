from flask import Flask, render_template
from flask import request, redirect, url_for, abort, session
import json
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from .config import MONGO_DB_URI, DB
import random as rd
from flask_pymongo import PyMongo
import hashlib
import re
import numpy as np
from .libraries.recommenderClass import Recommender, MongoServer

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_DBNAME'] = DB
app.config['MONGO_URI'] = MONGO_DB_URI
app.config['SECRET_KEY'] = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'
app.config['SESSION_PROTECTION'] = 'strong'

mongo = PyMongo(app)

@app.route('/')
def main_page():
  return render_template('main_page.html')

@app.route('/login/')
def login_page():
  return render_template('login_page.html')

@app.route('/register/')
def register_page():
  return render_template('registration_page.html')

@app.route('/recipe/<recipe_id>/')
def recipe_page(recipe_id):
  return render_template('recipe_page.html')

#
# API
#

@app.route('/api/')
@cross_origin()
def api_main_page():
  return 'API root'

@app.route('/api/ingredients/<query>/', methods=['GET'])
@cross_origin()
def get_ingredients(query):

    query = str(query).strip().lower()

    ingredients = mongo.db.ingredients.find({"Ingredient": {"$regex": "^"+query}}, {"Ingredient": 1}).limit(10)
    ingredients = [x["Ingredient"] for x in ingredients]

    return json.dumps(ingredients)

@app.route('/api/recipes/', methods=['POST'])
@cross_origin()
def get_recipes():
    """Receiving {"ingredients":[list], "count":[int]}"""

    jsonObj = json.loads(request.get_data())

    if 'ingredients' not in jsonObj.keys():
        return json.dumps({"error": "No ingredients received."}), 400

    ingredients = jsonObj['ingredients']

    if 'limit' not in jsonObj.keys():
        limit = 6
    else:
        limit = jsonObj['limit']

    if 'skip' not in jsonObj.keys():
        skip = 0
    else:
        skip = jsonObj['skip']

    if type(jsonObj['ingredients']) != list or not jsonObj['ingredients']:
        return json.dumps({"error": "Ingredients are not valid."}), 400

    # TODO: Replace correct recommender with limit and skip
    rec = Recommender()
    ids = rec.dummieRecommendation(limit)
    recipes = mongo.db.recipes.find({"_id": {"$in": ids}})
    result = []
    for recipe in recipes:
        recipe["_id"] = str(recipe["_id"])
        rating = mongo.db.ratings.find({"recipe_id": ObjectId(recipe["_id"])}, {"rating": 1, "_id": 0})
        rating = [int(x["rating"]) for x in rating]
        rating = np.mean(rating) if rating else False
        recipe["rating"] = rating
        result.append(recipe)
    return json.dumps({"recipes": result, "limit": limit})

@app.route('/api/recipes/<recipe_id>', methods=['GET'])
@cross_origin()
def get_recipe(recipe_id):

    # data = mongo.db.recipes.find().limit(50)
    # data = [str(x["_id"]) for x in data]
    # return json.dumps(data)

    if len(recipe_id) != 24:
        return json.dumps({"error": "Data structure is not correct."}), 400

    data = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}, {"_id": 0})

    if not data:
        return json.dumps({"error": "Recipe Not Found"})

    rating = mongo.db.ratings.find({"recipe_id": ObjectId(recipe_id)}, {"rating": 1, "_id": 0})
    rating = [int(x["rating"]) for x in rating]
    rating = np.mean(rating) if rating else False
    data["rating"] = rating

    if 'user_id' in session.keys():
        rating = mongo.db.ratings.find_one({"recipe_id": ObjectId(recipe_id), "user_id": ObjectId(session["user_id"])}, {"rating": 1, "_id": 0})
        data["user_rating"] = int(rating["rating"]) if rating else False
    else:
        data["user_rating"] = False

    data["_id"] = recipe_id
    return json.dumps(data)

@app.route('/api/recipe_score/<recipe_id>/', methods=['POST'])
@cross_origin()
def update_score(recipe_id):
    """Receiving {"rating":"[score]"}"""
    jsonObj = json.loads(request.get_data())

    if len(recipe_id) != 24:
        return json.dumps({"error": "Data structure is not correct."}), 400

    if 'rating' not in jsonObj.keys():
        return json.dumps({"error": "Data structure is not correct."}), 400

    if 'user_id' not in session.keys():
        return json.dumps({"error": "No active users."})

    mongo.db.ratings.update({"recipe_id": ObjectId(recipe_id), "user_id": ObjectId(session["user_id"])},
                                   {"recipe_id": ObjectId(recipe_id), "user_id": ObjectId(session["user_id"]), "rating": jsonObj["rating"], },
                                   upsert=True)

    return redirect(url_for('get_recipe', recipe_id=recipe_id), code=302)

@app.route('/api/users/', methods=['POST','GET'])
@cross_origin()
def active_user():
    """Receiving {"user_name":"[username]", "password":"[sha1_hashed_value]", "email":"[valid_email_address]"}"""
    if request.method == 'POST':

        jsonObj = json.loads(request.get_data())
        emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.I)

        if len(set(['user_name', 'password', 'email']).intersection(set(jsonObj.keys()))) < 3:
            return json.dumps({"error": "Data structure is not correct."}), 400
        if not jsonObj['user_name'] or not jsonObj['password'] or not jsonObj['email']:
            return json.dumps({"error": "Data structure is not correct."}), 400

        email = str(jsonObj["email"]).lower()
        if not re.search(emailRegex, email):
            return json.dumps({"error": "Invalid Email."})
        username = str(jsonObj["user_name"]).lower()
        password = hashlib.sha1(str(jsonObj["password"]).encode()).hexdigest()

        if mongo.db.users.find_one({"email": email}):
            return json.dumps({"error": "Email already exists."})

        newUser = {"user_name": username, "password": password, "email": email}
        id = mongo.db.users.insert(newUser)
        return redirect(url_for('get_user_data', user_id=id), code=301)

    elif request.method == 'GET':
        if 'user_id' not in session.keys():
            return json.dumps({"error": "There is no active user."})
        if len(session["user_id"]) != 24:
            return redirect(url_for('logout_user'))
        user = mongo.db.users.find_one({"_id": ObjectId(session["user_id"])}, {"email": 1, "user_name": 1, "_id": 0})
        if not user:
            return json.dumps({"error": "User Not Found"}), 404
        user["_id"] = session["user_id"]
        return json.dumps(user)

@app.route('/api/users/<user_id>/', methods=['GET'])
@cross_origin()
def get_user_data(user_id):
    if len(user_id) != 24:
        return json.dumps({"error": "Data structure is not correct."}), 400
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"email": 1, "user_name": 1, "_id": 0})
    if not user:
        return json.dumps({"error": "User Not Found"})
    user["_id"] = user_id
    return json.dumps(user)

@app.route('/api/login/', methods=['POST'])
@cross_origin()
def login_user():
    if 'user_id' in session.keys():
        return redirect(url_for('active_user'), code=301)

    if not request.get_data():
        return json.dumps({"error": "No Data."}), 400

    jsonObj = json.loads(request.get_data())
    emailRegex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.I)

    if len(set(['password', 'email']).intersection(set(jsonObj.keys()))) < 2:
        return json.dumps({"error": "Data structure is not correct."}), 400
    if not jsonObj['email'] or not jsonObj['password']:
        return json.dumps({"error": "Data structure is not correct."}), 400

    email = str(jsonObj["email"]).lower()
    if not re.search(emailRegex, email):
        return json.dumps({"error": "Invalid Email."})
    password = hashlib.sha1(str(jsonObj["password"]).encode()).hexdigest()

    userData = mongo.db.users.find_one({"email": email, "password": password})
    if userData:
        session['user_id'] = str(userData["_id"])
        return redirect(url_for('active_user'), code=302)
    return json.dumps({"error": "User not found."})

@app.route('/api/logout/')
@cross_origin()
def logout_user():
    session.pop('user_id', None)
    return "success"
