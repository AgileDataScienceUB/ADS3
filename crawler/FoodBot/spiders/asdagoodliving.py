import scrapy
from FoodBot.settings import SOURCE1, DATA_DIRECTORY
from scrapy import Request
from FoodBot.items import Source1Recipe
import re
from os import listdir
from os.path import isfile, join
import pandas as pd
import json
from logging import info, debug

class AsdagoodlivingSpider(scrapy.Spider):
    name = 'asdagoodliving'
    allowed_domains = ['asdagoodliving.co.uk']

    def __init__(self):
        # Pre compiling used Regexs
        self.id_regex = re.compile(r'recipes/(.*)', re.IGNORECASE)

    def start_requests(self):
        # Start location fort spider
        info('Crawler initiated.')
        yield Request(url=SOURCE1['recipes'], callback=self.parse_recipes)

    def parse_recipes(self, response):
        # Extracting recipe links for spider to follow
        recipes = response.selector.xpath('//div[@id="results"]//div[@class="index__item--content"]/a/@href').re(self.id_regex)
        for recipe in recipes:
            # Only follow links which are not extracted
            if not self.check_recipe(recipe):
                yield Request(url=SOURCE1['recipes']+recipe, callback=self.parse_recipe)

        # Extracting the link for spider to follow
        nextPage = response.selector.xpath('//li[@class="pagination--next"]/a/@href').extract()
        nextPage = nextPage[0] if nextPage else False
        if nextPage:
            yield Request(url=nextPage, callback=self.parse_recipes)

    def parse_recipe(self, response):
        # Extract unique id from url
        id = re.search(self.id_regex, response.url).group(1)

        # Creating recipe object
        recipe = Source1Recipe(id, response.body)

        # saving recipe to file
        if not self.check_recipe(id):
            info('Saving recipe: "{id}"'.format(id=id))
            self.save_recipe(id, recipe.return_json())
        else:
            debug('Recipe already exists: "{id}"'.format(id=id))

    def save_recipe(self, id, jsonString):
        # Saving recipe to file
        try:
            f = open(SOURCE1['directory']+id, 'w')
            f.write(jsonString)
            f.close()
            return True
        except Exception as e:
            raise e

    def check_recipe(self, id):
        # checking if recipe exists
        if isfile(SOURCE1['directory']+id):
            return True
        return False

    def closed(self, reason):
        # Convert gathered data into a CSV file after crawler stopped crawling
        # Creating Pandas Data Frame
        info('Saving data into CSV files. Please Wait ...')
        recipes_columns = ['id', 'url', 'image', 'name', 'time', 'serves', 'price', 'energy', 'fat', 'saturated_fat', 'sugar', 'salt']
        recipes = pd.DataFrame(columns=recipes_columns)
        ingredients_columns = ['id', 'ingredient']
        ingredients = pd.DataFrame(columns=ingredients_columns)

        # Iterating through saved recipes
        for file in self.recipe_file_names():
            # Reading file
            f = open(SOURCE1['directory']+file, 'r')
            jo = json.loads(f.read())
            f.close()

            recipe = [jo['id'], jo['url'], jo['image'], jo['name'], jo['time'], jo['serves'], jo['price'], jo['energy'], jo['fat'], jo['saturated_fat'], jo['sugar'], jo['salt']]
            recipes.loc[recipes.shape[0]+1] = recipe

            for ing in jo['ingredients']:
                ingredients.loc[ingredients.shape[0]+1] = [jo['id'], ing]

        # Saving into CSV file
        try:
            recipes.to_csv(DATA_DIRECTORY+'Source1Recipes.csv', index=False)
            ingredients.to_csv(DATA_DIRECTORY+'Source1Ingredients.csv', index=False)
        except Exception as e:
            raise e
        info('Saving Successful! Access data in data directory.')

    def recipe_file_names(self):
        # Returns recipes fine names
        for f in listdir(SOURCE1['directory']):
            if isfile(join(SOURCE1['directory'], f)) and f != '.nothing':
                yield f
