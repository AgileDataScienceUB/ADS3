from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/')
def main_page():
  return 'Initial API root'

@app.route('/ingredients', methods=['POST'])
def get_ingredients():
    """Receiving {"query":"[characters]"}"""
    jsonObj = json.loads(request.get_data())

    if 'query' not in jsonObj.keys():
        return json.dumps({"error":"No Queries Recieved."})

    if not jsonObj['query']:
        return json.dumps({"error":"Query is not valid."})

    query = str(jsonObj['query']).strip().lower()

    ingredients = ['Eggs1', 'Eggs3', 'Eggs2', 'Flour', 'Oil', 'Banana', 'Apple', 'Sugar', 'Bread', 'Oranges'] # TODO: Load complete list of ingredient
    ingredients = [x for x in ingredients if str(x).lower().find(query) > -1]

    return json.dumps({"ingredienrts": ingredients})
