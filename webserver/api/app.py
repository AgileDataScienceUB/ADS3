from flask import Flask
from flask import request, redirect, url_for, abort
import json
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from .config import MONGO_DB_URI, DB
import random as rd
from flask_pymongo import PyMongo
import hashlib
import re

app = Flask(__name__)
cors = CORS(app)

app.config['MONGO_DBNAME'] = DB
app.config['MONGO_URI'] = MONGO_DB_URI

mongo = PyMongo(app)

@app.route('/')
@cross_origin()
def main_page():
  return 'Initial API root'

@app.route('/ingredients/', methods=['POST'])
@cross_origin()
def get_ingredients():
    """Receiving {"query":"[characters]"}"""
    jsonObj = json.loads(request.get_data())

    if 'query' not in jsonObj.keys():
        return json.dumps({"error": "No Queries received."}), 400
    if not jsonObj['query']:
        return json.dumps({"error": "Query is not valid."}), 400

    query = str(jsonObj['query']).strip().lower()

    ingredients = ['Eggs1', 'Eggs3', 'Eggs2', 'Flour', 'Oil', 'Banana', 'Apple', 'Sugar', 'Bread', 'Oranges'] # TODO: Load complete list of ingredient
    ingredients = [x for x in ingredients if str(x).lower().find(query) > -1]

    return json.dumps({"ingredients": ingredients})

@app.route('/recipes/', methods=['post'])
@cross_origin()
def get_recipes():
    """Receiving {"ingredients":[list], "count":[int]}"""

    jsonObj = json.loads(request.get_data())

    if 'ingredients' not in jsonObj.keys():
        return json.dumps({"error": "No ingredients received."}), 400

    ingredients = jsonObj['ingredients']

    if 'count' not in jsonObj.keys():
        count = 5
    else:
        count = jsonObj['count']

    if type(jsonObj['ingredients']) != list or not jsonObj['ingredients']:
        return json.dumps({"error": "Ingredients are not valid."}), 400


    #
    #   Dummy Recipes
    #
    recipes = [
        {
            "id": "1",
            "title": "Grilled Cubanos",
            "image": "http://www.seriouseats.com/recipes/assets_c/2010/06/20100603-cubano-large-thumb-625xauto-93006.jpg"
        },
        {
            "id": "2",
            "title": "Cornish Pasty",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/01/01212012-188504-sunday-brunch-cornish-pasty-primary-thumb-625xauto-213242.jpg"
        },
        {
            "id": "3",
            "title": "Tomato Avgolemono Soup",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/02/20120214-seriousentertaining-soupson-tomatoavegolemenosoup-thumb-625xauto-219164.jpg"
        },
        {
            "id": "4",
            "title": "Cioppino",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/02/02182012-193155-sunday-supper-cioppino-primary-thumb-625xauto-219621.jpg"
        },
        {
            "id": "5",
            "title": "Steak Taco Salad",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/02/20120216-193359-dinner-tonight-steak-taco-salad-primary-thumb-625xauto-219875.jpg"
        },
        {
            "id": "6",
            "title": "Oyakodon",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/02/20120219oyakodonlow610-thumb-625xauto-220819.jpg"
        },
        {
            "id": "7",
            "title": "Oyakodon",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/02/20120219oyakodonlow610-thumb-625xauto-220819.jpg"
        },
        {
            "id": "8",
            "title": "Raspberry Limeade",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/06/20120618-lemonade-variations-03-thumb-625xauto-250111.jpg"
        },
        {
            "id": "9",
            "title": "Campari Flamingo",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/06/20120621-campari-flamingo-cocktail-primary-thumb-625xauto-251384.jpg"
        },
        {
            "id": "10",
            "title": "Watermelon Cake",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/07/20120709-213358-watermeloncake-thumb-625xauto-254470.jpg"
        },
        {
            "id": "11",
            "title": "Philly Smash",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/07/201206-213781-seasonalcocktail-phillysmash-thumb-625xauto-255242.jpg"
        },
        {
            "id": "12",
            "title": "Kir Royale Sangria",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/07/20120710KirRoyaleSangria-thumb-625xauto-255831.jpg"
        },
        {
            "id": "13",
            "title": "Braided Bread",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/07/20120717-214279-bread-baking-braided-bread-thumb-625xauto-256207.jpg"
        },
        {
            "id": "14",
            "title": "Cuban Picadillo",
            "image": "http://www.seriouseats.com/recipes/assets_c/2012/07/20120719-127677-LatAmCuisine-Picadillo-610x458-thumb-625xauto-257804.jpeg"
        }
    ]
    rand = rd.sample(range(1, 15), 5)
    return json.dumps({"recipes": [x for x in recipes if int(x['id']) in rand], "count": count})

@app.route('/users/', methods=['post','get'])
@cross_origin()
def users_route():
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
            return json.dumps({"error": "Invalid Email."}), 400
        username = str(jsonObj["user_name"]).lower()
        password = hashlib.sha1(str(jsonObj["password"]).encode()).hexdigest()

        if mongo.db.users.find_one({"email": email}):
            return json.dumps({"error": "Email already exists."}), 400

        newUser = {"user_name": username, "password": password, "email": email}
        id = mongo.db.users.insert(newUser)
        return redirect(url_for('get_user_data', user_id=id), code=301)

    elif request.method == 'GET':
        return 'get'

@app.route('/users/<user_id>/', methods=['GET'])
@cross_origin()
def get_user_data(user_id):
    if len(user_id) != 24:
        return json.dumps({"error": "Data structure is not correct."}), 400
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)}, {"email": 1, "user_name": 1, "_id": 0})
    if not user:
        return json.dumps({"error": "User Not Found"}), 404
    user["_id"] = user_id
    return json.dumps(user)
