import scrapy
from FoodBot.settings import SOURCE1
from scrapy import Request
from FoodBot.items import Source1Recipe
import re

class AsdagoodlivingSpider(scrapy.Spider):
    name = 'asdagoodliving'
    allowed_domains = ['asdagoodliving.co.uk']

    def __init__(self):
        self.count = 0
        self.id_regex = re.compile(r'recipes/(.*)', re.IGNORECASE)

    def start_requests(self):
        yield Request(url=SOURCE1['recipes'], callback=self.parse_recipes)

    def parse_recipes(self, response):
        nextPage = response.selector.xpath('//li[@class="pagination--next"]/a/@href').extract()
        nextPage = nextPage[0] if nextPage else False

        recipes = response.selector.xpath('//div[@id="results"]//div[@class="index__item--content"]/a/@href').re(self.id_regex)
        for recipe in recipes:
            yield Request(url=SOURCE1['recipes']+recipe, callback=self.parse_recipe)

        if nextPage:
            yield Request(url=nextPage, callback=self.parse_recipes)

    def parse_recipe(self, response):
        id = re.search(self.id_regex, response.url).group(1)
        recipe = Source1Recipe(id, response.body)
        self.save_recipe(id, recipe.return_json())

    def save_recipe(self, id, jsonString):
        try:
            f = open(SOURCE1['directory']+id, 'w')
            f.write(jsonString)
            f.close()
            return True
        except Exception as e:
            raise e
