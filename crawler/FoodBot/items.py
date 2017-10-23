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
        image = selector.xpath('//div[@class="article--image"]//picture/source/@srcset').re(self.image_address_regex)
        self._data['image'] = image[0].strip() if image else ''
        name = selector.xpath('//h1[@itemprop="name"]/text()').extract()
        self._data['name'] = name[0].strip() if name else ''
        time = selector.xpath('//strong[@itemprop="totalTime"]/text()').extract()
        self._data['time'] = time[0].strip() if time else ''
        serves = selector.xpath('//strong[@itemprop="recipeYield"]/text()').extract()
        self._data['serves'] = serves[0].strip() if serves else ''
        price = selector.xpath('//div[contains(@class,"article__lhs--recipe-info")]').re(self.price_regex)
        self._data['price'] = price[0].strip() if price else ''
        nutrition_ul = selector.xpath('//div[@itemprop="nutrition"]/ul').strip()
        energy = selector.xpath('//span[@itemprop="calories"]/em/text()').extract()
        self._data['energy'] = energy[0].strip() if energy else ''
        fat = selector.xpath('//meta[@itemprop="fatContent"]/@content').extract()
        self._data['fat'] = fat[0].strip() if fat else ''
        saturated_fat = selector.xpath('//meta[@itemprop="saturatedFatContent"]/@content').extract()
        self._data['saturated_fat'] = saturated_fat[0].strip()
        sugar = selector.xpath('//meta[@itemprop="sugarContent"]/@content').extract()
        self._data['sugar'] = sugar[0].strip() if sugar else ''
        salt = nutrition_ul.xpath('//li[5]/span/em/text()').extract()
        self._data['salt'] = salt[0].strip() if salt else ''
        self._data['ingredients'] = selector.xpath('//span[@itemprop="ingredients"]/text()').extract()

    def return_json(self):
        # Returning Data in JSON format
        return json.dumps(self._data)