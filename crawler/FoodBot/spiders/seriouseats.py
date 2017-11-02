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
        # recipes_columns = ['id', 'url', 'image', 'name', 'active_time', 'total_time', 'serves']
        # recipes = pd.DataFrame(columns=recipes_columns)
        # ingredients_columns = ['id', 'ingredient']
        # ingredients = pd.DataFrame(columns=ingredients_columns)
        # tags_columns = ['id', 'tags']
        # tags = pd.DataFrame(columns=tags_columns)

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
