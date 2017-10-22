from FoodBot.settings import SOURCE1
import json
from scrapy.selector import Selector
import re

class Source1Recipe():
    def __init__(self, ID, PageContent):
        # HTML content
        self._page_content = PageContent

        # Pre compiling used Regexs.
        self.image_address_regex = re.compile(r'(.*)\?', re.IGNORECASE)
        self.price_regex = re.compile(r"price:\s*<strong>(.*)</strong>", re.IGNORECASE | re.MULTILINE)

        # Data Dictionary
        self._data = {
            'id':ID,
            'url': SOURCE1['recipes']+ID,
            'image': None,
            'name': None,
            'time': None,
            'serves': None,
            'price': None,
            'energy': None,
            'fat': None,
            'saturated_fat': None,
            'sugar': None,
            'salt': None,
            'ingredients':None
        }
        self._process_content()

    def _process_content(self):
        # Processing HTML structure for data
        selector = Selector(text=self._page_content)
        self._data['image'] = selector.xpath('//div[@class="article--image"]//picture/source/@srcset').re(self.image_address_regex)[0]
        self._data['name'] = selector.xpath('//h1[@itemprop="name"]/text()').extract()[0]
        self._data['time'] = selector.xpath('//strong[@itemprop="totalTime"]/text()').extract()[0]
        self._data['serves'] = selector.xpath('//strong[@itemprop="recipeYield"]/text()').extract()[0]
        self._data['price'] = selector.xpath('//div[contains(@class,"article__lhs--recipe-info")]').re(self.price_regex)[0]
        nutrition_ul = selector.xpath('//div[@itemprop="nutrition"]/ul')
        self._data['energy'] = selector.xpath('//span[@itemprop="calories"]/em/text()').extract()[0]
        self._data['fat'] = selector.xpath('//meta[@itemprop="fatContent"]/@content').extract()[0]
        self._data['saturated_fat'] = selector.xpath('//meta[@itemprop="saturatedFatContent"]/@content').extract()[0]
        self._data['sugar'] = selector.xpath('//meta[@itemprop="sugarContent"]/@content').extract()[0]
        self._data['salt'] = nutrition_ul.xpath('//li[5]/span/em/text()').extract()[0]
        self._data['ingredients'] = selector.xpath('//span[@itemprop="ingredients"]/text()').extract()


    def return_json(self):
        # Returning Data in JSON format
        return json.dumps(self._data)