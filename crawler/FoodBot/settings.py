BOT_NAME = 'FoodBot'

SPIDER_MODULES = ['FoodBot.spiders']
NEWSPIDER_MODULE = 'FoodBot.spiders'

USER_AGENT = 'FoodBot'

ROBOTSTXT_OBEY = True

SOURCE1 = {
    'url': 'https://www.asdagoodliving.co.uk/',
    'recipes': 'https://www.asdagoodliving.co.uk/food/recipes/',
    'directory': 'recipes/source1/'
}

SOURCE2 = {
    'url': 'http://allrecipes.com/',
    'recipes': ['http://allrecipes.com/recipedetail.xml.gz', 'http://allrecipes.com/recipedetail1.xml.gz', 'http://allrecipes.com/recipedetail2.xml.gz'],
    'directory': 'recipes/source2/'
}

DATA_DIRECTORY = 'data/'

LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 16

