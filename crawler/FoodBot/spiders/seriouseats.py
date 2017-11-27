# -*- coding: utf-8 -*-
import scrapy
from logging import info
from scrapy import Request
from FoodBot.settings import SOURCE2, DATA_DIRECTORY
import json
from os.path import isfile, join
from os import listdir
import pandas as pd
import json
import csv

class SeriouseatsSpider(scrapy.Spider):
    name = 'seriouseats'
    allowed_domains = ['seriouseats.com']

    def __init__(self):
        # Pre compiling used Regexs
        pass

    def start_requests(self):
        # Start location fort spider
        info('Crawler initiated.')
        info('Downloading Data.')
        yield Request(url=SOURCE2['recipes'], callback=self.parse_recipes)

    def parse_recipes(self, response):
        # Extracting recipe ids for spider to follow
        data = json.loads(response.body)
        total_recipes = data['total_entries']
        data = data['entries']

        info('Processing Data ...')

        for item in data:
            id = str(item['id'])

            if self.check_recipe(id):
                info('Recipe with id {0} exists.'.format(id))
                continue
            string = json.dumps(item)
            self.save_recipe(id, string)
            info('Saved Recipe {0}.'.format(id))

    def save_recipe(self, id, jsonString):
        # Saving recipe to file
        try:
            f = open(SOURCE2['directory']+id, 'w')
            f.write(jsonString)
            f.close()
            return True
        except Exception as e:
            raise e

    def check_recipe(self, id):
        # checking if recipe exists
        if isfile(SOURCE2['directory']+id):
            return True
        return False

    def closed(self, reason):
        # Convert gathered data into a CSV file after crawler stopped crawling
        # Creating Pandas Data Frame
        info('Saving data into CSV files. Please Wait ...')

        # creating CSV writers
        recipesFile = 'Source2Recipes.csv'
        recipes = open(DATA_DIRECTORY+recipesFile, 'w')
        recipesCsv = csv.writer(recipes)
        recipesCsv.writerow(['id','title','permalink','thumbnail_625','number_serves','total_time','active_time'])

        ingredientsFile = 'Source2Ingredients.csv'
        ingredients = open(DATA_DIRECTORY + ingredientsFile, 'w')
        ingredientsCsv = csv.writer(ingredients)
        ingredientsCsv.writerow(['id', 'ingredient'])

        tagsFile = 'Source2Tags.csv'
        tags = open(DATA_DIRECTORY + tagsFile, 'w')
        tagsCsv = csv.writer(tags)
        tagsCsv.writerow(['id', 'tag'])

        # Iterating through saved recipes
        for file in self.recipe_file_names():
            # Reading file
            f = open(SOURCE2['directory']+file, 'r')
            jo = json.loads(f.read())
            f.close()

            # Extracting id
            id = jo['id']

            # Dividing ingredients
            for ing in jo['ingredients']:
                ingredientsCsv.writerow([id, ing])

            # Deviding Tags
            for tag in jo['tags']:
                tagsCsv.writerow([id, tag])

            recipesCsv.writerow([jo['id'], jo['title'], jo['permalink'], jo['thumbnail_625'], jo['number_serves'], jo['total_time'], jo['active_time']])

        recipes.close()
        ingredients.close()
        tags.close()

    def recipe_file_names(self):
        # Returns recipes fine names
        for f in listdir(SOURCE2['directory']):
            if isfile(join(SOURCE2['directory'], f)) and f != '.nothing':
                yield f