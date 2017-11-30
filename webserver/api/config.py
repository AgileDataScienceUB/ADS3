DB = {
    "username": "crawler",
    "password": "crawlergroup3",
    "name": "agile_data_science_group_3"
}

MONGO_DB_URI = "mongodb://{username}:{password}@ds233895.mlab.com:33895/{dbname}".format(
    username=DB['username'],
    password=DB['password'],
    dbname=DB['name']
)