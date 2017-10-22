BOT_NAME = 'FoodBot'

SPIDER_MODULES = ['FoodBot.spiders']
NEWSPIDER_MODULE = 'FoodBot.spiders'

USER_AGENT = 'FoodBot'

ROBOTSTXT_OBEY = True

SOURCE = 'https://www.asdagoodliving.co.uk/'

# {number} starts from 0 to and grows by a factor of 12
# i.e. 0 - 12 - 24 - 36 - etc.
RECIPES = SOURCE+'food/recipes/'

CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

