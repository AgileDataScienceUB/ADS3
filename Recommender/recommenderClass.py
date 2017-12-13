import numpy as np
import pandas as pd
import pymongo
import bson
from tqdm import tqdm
from bson.objectid import ObjectId
import operator

class MongoServer():
    credentials = None
    conn = None
    db = None
    collections = {}
    def __init__(self, run = False, credentials = "credentials.txt", db_name = "agile_data_science_group_3"):
        if run:
            if not self.connect2Mongo(credentials):
                print("Connection to server Failed.")
            
            if not self.connect2DataBase(db_name):
                print("Connection Data Base Failed.")
    """Rotine to connect to Mongo DB"""    
    def connect2Mongo(self, credentials = "credentials.txt"):
        try:
            #use your database name, user and password here:
            with open(credentials, 'r', encoding='utf-8') as f:
                [name,password,url,dbname]=f.read().splitlines()
            conn=pymongo.MongoClient("mongodb://{}:{}@{}/{}".format(name,password,url,dbname))
            self.conn = conn
            return True
        except pymongo.errors.ConnectionFailure as e:
            return False
    
    """Routine to connect to a Data Base"""
    def connect2DataBase(self, db_name = "agile_data_science_group_3"):
        try:
            self.db = self.conn[db_name]
            return True
        except:
            return False
    
    """Return the available collections in a data base"""
    def listOfCollections (self):
        return self.db.collection_names()
    
    """Donwload all the ollections from the data base"""
    def getAllCollections (self):
        collections = self.listOfCollections()
        for col in collections:
            self.getCollectionFromServer(col)
        return True
    
    
    """Routine to get one collection of the Data Base"""
    # return the collection
    def getCollectionFromServer (self, name_collection):
        if name_collection in self.db.collection_names():
            self.collections[name_collection] = self.db.get_collection(name_collection)
            print ("Collection ",name_collection," Update in Local.")
            return True
        return False
    
    """ Take the collection from the local copy"""
    def getCollection(self, name_collection):
        if not name_collection in self.collections:
            if not self.getCollectionFromServer(name_collection):
                return False
        return self.collections[name_collection]
    
    """ Gets all the items of the collection"""
    def getItems(self, name_collection, N = None):
        if not name_collection in self.collections:
            if not self.getCollectionFromServer(name_collection):
                return False
        if N != None:
            return [element for element in self.collections[name_collection].find().limit(N)]
        else:
            return [element for element in self.collections[name_collection].find()]
    
    """Query in one Collection"""
    def searchInCollection(self, name_collection, field, patro, N = None):
        if N == None:
            return [element for element in self.db.get_collection(name_collection).find({field:patro})]
        else:
            return [element for element in self.db.get_collection(name_collection).find({field:patro}).limit(N)]
    
    """Query in all the Collections"""
    def searchInDB (self, field, patro):
        query = {}
        for collection in self.db.collection_names():
            query[collection] = [element for element in self.db.get_collection(collection).find({field:patro})]
        return query
    
    """Find one in the collection"""
    def findOne(self, collection_name):
        return self.db.get_collection(collection_name).find_one()
    
    """Seach in collection with multiple querys"""
    def searchWithMultiplyConditions(self, collection_name, _query, condition ='$and', N = 10):
        query = []
        for item in self.db.get_collection(collection_name).find({condition:_query}).limit( N ):
            query.append(item)
        return query
             
    """Find N elements in one collection"""
    def findNElement(self, collection_name, N):
        query = []
        for item in self.db.get_collection(collection_name).find().limit( N ):
            query.append(item)
        return query
    
    """Insert one element into collection"""
    def insertInCollection (self, collection_name,  item):
        assert type(item) == {}, "Item must be a dictionary"
        return self.db.get_collection(collection_name).insert(item)
     
        
class Recommender:
    
    def __init__(self):
        # connect to mongo with MongoServer object
        self.server = MongoServer(True)
        
    """Dummie Recommender"""
    def dummieRecommendation(self, N = 10):
        listObjectIds = []
        for item in self.server.findNElement('recipes', N):
            listObjectIds.append(item['_id'])
        return listObjectIds
        
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
            print ("idRecepie is not a ObjectId")
            return []
        
        # Search the recepie    
        _collection = 'recipes_ingredients'
        _field = '_id' # ObjectId
        _patro = idRecepie
        query = self.server.searchInCollection(name_collection = _collection, field = _field, patro = _patro)[0]    
        # obtain the ingredients
        return query, query.values()[1]
    

    """Search user by idUser(ObjectId)"""
    def searchUsersById(self, idUser):
        idUser = self.isObjectId(idUser)
        if idUser == None:
            print ("Id User is not a ObjectId")
            return []
        
        _collection = 'users'
        _field = '_id' # ObjectId
        _patro = idUser
        query = self.server.searchInCollection(name_collection = _collection, field = _field, patro = _patro)[0]
        
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
            print ("Id User is not a ObjectId")
            return []
        
        # look for the ratings of the user
        ratingsUser = self.server.searchInCollection(name_collection='ratings', field='user_id', patro=idUser, N=n) 
        if ratingsUser == []:
            print ("User has no ratings. Cold Start.")
            return None
        ratings = []
        m_user.append(idUser) 
        
        # obtain ratings from the same recipes
        for rating in tqdm(ratingsUser):
            m_ids.append(rating['recipe_id'])
            # search for more ratings in the same recipe
            recipes = self.server.searchInCollection(name_collection='ratings', field='recipe_id', patro=rating['recipe_id'])
            
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
    def collaborativeFiltering(self, idUser, n = 10):
        # take the ratings of the user
        # with the recipes of the user, find which recepes we can generate
        # generate the recommender matrix for user
        # call the distance function
        return self.dummieRecommendation(N)
    
    """ Method that search in function of the ingredients"""
    def searchRecepieByIngredients(self, listIngredients, N = 10):
        query = []
        for ingredient in listIngredients:
            query.append({'ingredients':ingredient})
        
        respons = self.server.searchWithMultiplyConditions('RecIng', query)
        
        objectsIds = []
        for recepie in respons:
            objectsIds.append(recepie['_id'])
            
        return objectsIds
    
    """ Return top n recipes by maximum mean rating. In case of draw, then by minimum standard deviation rating. """
    def bestRatedWeb(self, n=10):
        data = pd.DataFrame(self.server.getItems('ratings', N = 16000))
        # top rated
        data["rating"] = data["rating"].astype(float)
        recipe_rating_mean = data.groupby(['recipe_id'])['rating'].mean()
        recipe_rating_std = data.groupby(['recipe_id'])['rating'].std()
        recipe_rating = pd.concat([recipe_rating_mean, recipe_rating_std], axis=1)
        recipe_rating.columns=["mean", "std"]
        recs = recipe_rating.sort_values(["mean", "std"], ascending=[0,1])
        
        return list(map(ObjectId, list(recs.index.values)[:int(n)]))
    
    def distance_recipes(self, ing1, ing2):
        rec1 = set(ing1)
        rec2 = set(ing2)
        d = len(rec1.intersection(rec2))/len(rec1)
        if d == 1.0:
            return 0
        return d

    """Recommender based on content"""
    def bestRated(self, idRecepie):
        recipes_dict = self.server.getItems('RecIng', N = 10)
        ingridents = self.server.searchInCollection('RecIng', 'recipe_id', idRecepie)[0]['ingredients']

        dis = dict()
        for rec in recipes_dict:
            dis[rec['_id']] = self.distance_recipes(ingridents, rec['ingredients'])

        df_return = sorted(dis.items(),key=operator.itemgetter(1),reverse=True)[0:10]

        return [obj for obj, rat in df_return]
    
