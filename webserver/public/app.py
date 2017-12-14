import numpy as np
import pandas as pd
import pymongo
import bson
from tqdm import tqdm
from bson.objectid import ObjectId
import operator
from random import shuffle
from flask import Flask, render_template
from flask import request, redirect, url_for, abort, session
import json
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
import random as rd
from flask_pymongo import PyMongo
import hashlib
import re
import os

DB = {
    "username": "crawler",
    "password": "crawlergroup3",
    "name": "agile_data_science_group_3"
}

MONGO_DB_URI = "mongodb://{username}:{password}@ds233895.mlab.com:33895/{dbname}".format(
    username=DB['username'],
    password=DB['password'],
    dbname=DB['name']
)

class MongoServer:
    credentials = None
    conn = None
    db = None
    collections = {}

    def __init__(self, credentials, run=False, db_name="agile_data_science_group_3"):
        if run:
            if not self.connect2Mongo(credentials, db_name):
                print("Connection to server Failed.")

            if not self.connect2DataBase(db_name):
                print("Connection Data Base Failed.")

    """Rotine to connect to Mongo DB"""

    def connect2Mongo(self, credentials, db):
        try:
            # use your database name, user and password here:
            name, password, url, dbname = credentials['name'], credentials['password'], credentials['url'], credentials[
                'dbname']
            conn = pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(name, password, url, dbname))
            self.conn = conn
            return True
        except pymongo.errors.ConnectionFailure as e:
            return False

    """Routine to connect to a Data Base"""

    def connect2DataBase(self, db_name="agile_data_science_group_3"):
        try:
            self.db = self.conn[db_name]
            return True
        except:
            return False

    """Return the available collections in a data base"""

    def listOfCollections(self):
        return self.db.collection_names()

    """Donwload all the ollections from the data base"""

    def getAllCollections(self):
        collections = self.listOfCollections()
        for col in collections:
            self.getCollectionFromServer(col)
        return True

    """Routine to get one collection of the Data Base"""

    # return the collection
    def getCollectionFromServer(self, name_collection):
        if name_collection in self.db.collection_names():
            self.collections[name_collection] = self.db.get_collection(name_collection)
            print("Collection ", name_collection, " Update in Local.")
            return True
        return False

    """ Take the collection from the local copy"""

    def getCollection(self, name_collection):
        if not name_collection in self.collections:
            if not self.getCollectionFromServer(name_collection):
                return False
        return self.collections[name_collection]

    """ Gets all the items of the collection"""

    def getItems(self, name_collection, N=None):
        if not name_collection in self.collections:
            if not self.getCollectionFromServer(name_collection):
                return False
        if N != None:
            return [element for element in self.collections[name_collection].find().limit(N)]
        else:
            return [element for element in self.collections[name_collection].find()]

    """Query in one Collection"""

    def searchInCollection(self, name_collection, field, patro, N=None):
        if N == None:
            return [element for element in self.db.get_collection(name_collection).find({field: patro})]
        else:
            return [element for element in self.db.get_collection(name_collection).find({field: patro}).limit(N)]

    """Query in all the Collections"""

    def searchInDB(self, field, patro):
        query = {}
        for collection in self.db.collection_names():
            query[collection] = [element for element in self.db.get_collection(collection).find({field: patro})]
        return query

    """Find one in the collection"""

    def findOne(self, collection_name):
        return self.db.get_collection(collection_name).find_one()

    """Seach in collection with multiple querys"""

    def searchWithMultiplyConditions(self, collection_name, _query, condition='$and', N=10):
        query = []
        for item in self.db.get_collection(collection_name).find({condition: _query}).limit(N):
            query.append(item)
        return query

    """Find N elements in one collection"""

    def findNElement(self, collection_name, N):
        query = []
        for item in self.db.get_collection(collection_name).find().limit(N):
            query.append(item)
        return query

    """Insert one element into collection"""

    def insertInCollection(self, collection_name, item):
        assert type(item) == {}, "Item must be a dictionary"
        return self.db.get_collection(collection_name).insert(item)

class Recommender:
    def __init__(self, credentials):
        # connect to mongo with MongoServer object
        self.server = MongoServer(credentials, True)

    """Dummie Recommender"""

    def dummieRecommendation(self, N=10):
        listObjectIds = []
        for item in self.server.findNElement('recipes', 1000):
            listObjectIds.append(item['_id'])
        shuffle(listObjectIds)
        return listObjectIds[:N]

    """Method that check if the object is a ObjectId"""

    def isObjectId(self, _id):
        try:
            # Do a query in a specific user collection
            if not type(_id) == bson.objectid.ObjectId:
                # creation of a objectID
                if type(_id) == str:
                    idUser = bson.objectid.ObjectId(_id)
                else:
                    return None
            return _id
        except:
            return None

    """Search user by idRecepie(ObjectId)"""

    def searchRecepieWithIngredientsByIs(self, idRecepie):
        idRecepie = self.isObjectId(idRecepie)
        if idRecepie == None:
            print("idRecepie is not a ObjectId")
            return []

        # Search the recepie
        _collection = 'recipes_ingredients'
        _field = '_id'  # ObjectId
        _patro = idRecepie
        query = self.server.searchInCollection(name_collection=_collection, field=_field, patro=_patro)[0]
        # obtain the ingredients
        return query, query.values()[1]

    """Search user by idUser(ObjectId)"""

    def searchUsersById(self, idUser):
        idUser = self.isObjectId(idUser)
        if idUser == None:
            print("Id User is not a ObjectId")
            return []

        _collection = 'users'
        _field = '_id'  # ObjectId
        _patro = idUser
        query = self.server.searchInCollection(name_collection=_collection, field=_field, patro=_patro)[0]

        return query

    """Method that compute a smaller matrix for BestRated"""

    def computeRecommenderMatrixBestRated(self, idRecipe):
        # look the ingredients used in the recipe
        # look the recipe that use on of the ingridients
        # compute Recommender Matrix
        return None

    """Method that compute a smaller matrix for collaborativeFiltering"""

    def computeRecommenderMatrixCollaborativeFiltering(self, idUser, n=10):
        m_ids = []
        m_user = []

        idUser = self.isObjectId(idUser)
        if idUser == None:
            print("Id User is not a ObjectId")
            return []

        # look for the ratings of the user
        ratingsUser = self.server.searchInCollection(name_collection='ratings', field='user_id', patro=idUser, N=n)
        if ratingsUser == []:
            print("User has no ratings. Cold Start.")
            return None
        ratings = []
        m_user.append(idUser)

        # obtain ratings from the same recipes
        for rating in tqdm(ratingsUser):
            m_ids.append(rating['recipe_id'])
            # search for more ratings in the same recipe
            recipes = self.server.searchInCollection(name_collection='ratings', field='recipe_id',
                                                     patro=rating['recipe_id'])

            # acumulate the ratings
            ratings += recipes

            # look if objectId of recipe is in the list
            for recipe in recipes:
                if not recipe['recipe_id'] in m_ids:
                    m_ids.append(recipe['recipe_id'])

                if not recipe['user_id'] in m_user:
                    m_user.append(recipe['user_id'])

        # compute Recommender Matrix
        matrix = pd.DataFrame(np.full((len(m_ids), len(m_user)), np.nan), index=m_ids, columns=m_user)
        for rates in ratings:
            matrix[rates['user_id']][rates['recipe_id']] = rates['rating']

        return matrix

    """Method that donwliad the matrix from ratings and generates this one"""

    def generateRatingMatrix(self):
        m_ids = set()
        m_user = set()
        ratings = self.server.getItems('ratings')
        for item in ratings:
            m_ids.add(item["recipe_id"])
            m_user.add(item["user_id"])

        matrix = pd.DataFrame(np.full((len(m_ids), len(m_user)), np.nan), index=m_ids, columns=m_user)
        for rates in ratings:
            matrix[rates['user_id']][rates['recipe_id']] = rates['rating']

        return matrix

    def computeRecomendation(self):
        # Introduce here the distance function for each of the cases
        # maybe it is necesary to separete the funciton in two
        pass

    """Recommender of Collaborative Filtering"""

    def collaborativeFiltering(self, idUser, n=10):
        # take the ratings of the user
        # with the recipes of the user, find which recepes we can generate
        # generate the recommender matrix for user
        # call the distance function
        return self.dummieRecommendation(N)

    """ Method that search in function of the ingredients"""

    def searchRecepieByIngredients(self, listIngredients, N=10, skip=0):
        query = []
        for ingredient in listIngredients:
            query.append({'ingredients': ingredient})

        respons = self.server.searchWithMultiplyConditions('RecIng', query)

        objectsIds = []
        for recepie in respons:
            objectsIds.append(recepie['recipe_id'])

        return objectsIds

    """ Return top n recipes by maximum mean rating. In case of draw, then by minimum standard deviation rating. """

    def bestRatedWeb(self, n=10):
        data = pd.DataFrame(self.server.getItems('ratings', N=2000))
        # top rated
        data["rating"] = data["rating"].astype(float)
        recipe_rating_mean = data.groupby(['recipe_id'])['rating'].mean()
        recipe_rating_std = data.groupby(['recipe_id'])['rating'].std()
        recipe_rating = pd.concat([recipe_rating_mean, recipe_rating_std], axis=1)
        recipe_rating.columns = ["mean", "std"]
        recs = recipe_rating.sort_values(["mean", "std"], ascending=[0, 1])

        return list(map(ObjectId, list(recs.index.values)[:int(n)]))

    def distance_recipes(self, ing1, ing2):
        rec1 = set(ing1)
        rec2 = set(ing2)
        d = len(rec1.intersection(rec2)) / len(rec1)
        if d == 1.0:
            return 0
        return d

    """Recommender based on content"""

    def bestRated(self, idRecepie):
        recipes_dict = self.server.getItems('RecIng', N=2000)
        ingridents = self.server.searchInCollection('RecIng', 'recipe_id', idRecepie)[0]['ingredients']

        dis = dict()
        for rec in recipes_dict:
            dis[rec['recipe_id']] = self.distance_recipes(ingridents, rec['ingredients'])

        df_return = sorted(dis.items(), key=operator.itemgetter(1), reverse=True)[0:10]

        return [obj for obj, rat in df_return]

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
    rec = Recommender({'name': 'huang', 'password': 'chen1992', 'url': 'ds233895.mlab.com:33895', 'dbname': 'agile_data_science_group_3'})
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

@app.route('/api/random_recipe/', methods=['GET'])
@cross_origin()
def random_recipe():

    data = mongo.db.recipes.aggregate([ { "$sample": { "size": 1 } } ])
    for item in data:
        data = item
        data['_id'] = str(data["_id"])

    rating = mongo.db.ratings.find({"recipe_id": ObjectId(data["_id"])}, {"rating": 1, "_id": 0})
    rating = [int(x["rating"]) for x in rating]
    rating = np.mean(rating) if rating else False
    data["rating"] = rating

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

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)