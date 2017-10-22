import scrapy
from FoodBot.settings import SOURCE1
from scrapy import Request
from FoodBot.items import Source1Recipe
import re
import os.path as osp

class AsdagoodlivingSpider(scrapy.Spider):
    name = 'asdagoodliving'
    allowed_domains = ['asdagoodliving.co.uk']

    def __init__(self):
        # Pre compiling used Regexs
        self.id_regex = re.compile(r'recipes/(.*)', re.IGNORECASE)

    def start_requests(self):
        # Start location fort spider
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
            self.save_recipe(id, recipe.return_json())

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
        if osp.isfile(SOURCE1['directory']+id):
            return True
        return False
