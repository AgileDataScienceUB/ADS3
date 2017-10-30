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
    'url': 'http://www.seriouseats.com/',
    'recipes': 'http://www.seriouseats.com/topics/search?index=recipe&count=999999&only=id,tags,ingredients,title,thumbnail_1500,active_time,permalink,total_time,number_serves',
    'directory': 'recipes/source2/'
}

DATA_DIRECTORY = 'data/'

LOG_LEVEL = 'INFO'

CONCURRENT_REQUESTS = 16

