'''
Initial data loading from movies.json and inserting into database
'''
import json
import requests
from app import db

def database_init():
    with open('movies.json') as data:
        movies = json.load(data)

    db.drop_all()
    db.create_all()

    BASE = "http://127.0.0.1:5000/"

    for movie in movies:
        requests.post(BASE + "movie",movie)

if __name__=='__main__':
    database_init()