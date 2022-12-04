import pymongo
import certifi

con_srt = "mongodb+srv://elbaastidas:bastidas46@cluster0.wujncnp.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(con_srt, tlsCAFile=certifi.where())

db = client.get_database('Organika')

me = {
    'first': 'Miguel',
    'last': "Bastidas",
    'age': 35,
    'hobbies': ['music', 'movies', 'sports'],
    'address': {
        'street': 'Main St',
        'number': 345,
        'city': 'New York',
    }

}
