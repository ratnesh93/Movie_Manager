from flask import Flask, render_template, redirect, make_response, jsonify, flash
from flask_restful import Api, Resource, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.sql import collate
from helper import *
import os
import json
import sqlite3

app=Flask(__name__,template_folder="templates")
app.secret_key = os.urandom(24)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movies.db'
db=SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

class MovieModel(db.Model):
    name = db.Column(db.String(100),primary_key=True)
    image = db.Column(db.String(100))
    description = db.Column(db.String(500))
    dateLastEdited = db.Column(db.DateTime(),onupdate=datetime.now())

    def __repr__(self):
        return f"Movie(name = {self.name}, image= {self.image}, description= {self.description} , dataLastEdited = {self.dateLastEdited})"

db.create_all()

def database_init():
    print("-----Adding Initital Data from movies.json file-----")
    with open('movies.json') as data:
        movies = json.load(data)

    db.drop_all()
    db.create_all()

    conn = sqlite3.connect("movies.db")
    cursor =conn.cursor()
    for movie in movies:
        statement = "INSERT INTO movie_model(name,image,description) VALUES(?,?,?)"
        cursor.execute(statement,[movie['name'],movie['image'],movie['description']])
    conn.commit()

class Movie(Resource):
    @marshal_with(movie_resource_fields)
    def get(self):
        result = MovieModel.query.all()
        return result

    #@marshal_with(movie_resource_fields)
    def post(self):
        '''
            add new movie
            args sample: {
                    "name": "Movie Test Data1",
                    "image": "test url",
                    "description": "test description"
                }
        '''
        args=movie_post_args.parse_args()
        result = MovieModel.query.filter_by(name=args['name']).first()
    
        if result:
            abort(409,message="Movie already present, Cannot add Movie with same name")
        
        movie = MovieModel(name=args['name'],image=args['image'],description=args['description'],dateLastEdited=datetime.now())

        db.session.add(movie)
        db.session.commit()
        flash("Movie: '"+args['name']+"' got Added!!!")
        return redirect("/movie/all")

api.add_resource(Movie,"/movie")

database_init()

@app.route('/movie/all',methods=['GET'])
def getAll():
    '''
        return the list of all movies in the database
    '''
    result = MovieModel.query.order_by(collate(MovieModel.name,'NOCASE')).all()
    return render_template("movies.html",movies=result), 200
    
@app.route('/movie/delete',methods=['POST'])
def delete():
    '''
        delete the movie
        args:   string
    '''
    args=movie_delete_args.parse_args()
    title = args["name"]
    movie = MovieModel.query.filter(func.lower(MovieModel.name)==func.lower(title)).first()
    if movie is None:
        return render_template("error.html"), 404
    db.session.delete(movie)
    db.session.commit()
    flash("Movie: '"+title+"' got Deleted!!!")
    return redirect("/movie/all")
    
@app.route('/movie/update',methods=['POST'])
def update():
    '''
        update the movie
        args sample:{
                "oldtitle":"Movie Test Data1",
                "name": "updating Movie Test Data1",
                "image": "test url",
                "description": "test description"
            } 
    '''
    args=movie_update_args.parse_args()
    movie = MovieModel.query.filter_by(name=args['oldtitle']).first()

    if movie is None:
        return make_response(jsonify({"error": "Movie not found"}), 404)

    if args['name'] != '':
        movie.name =args['name']
    
    if args['image'] != '':
        movie.image =args['image']

    if args['description'] != '':
        movie.description =args['description']
    
    db.session.commit()
    flash("Movie: '"+args['oldtitle']+"' got Updated!!!")
    return redirect("/movie/all")

@app.route('/movie/search',methods=['POST'])
def searchAll():
    '''
        Normal search for any movie name, if the search string name is substring of any
        movie name in the database, it will show all the matching output. If no movie 
        found, it will return empty result. If search string name is empty, it will 
        return with all the result in sorted order
        
        args: string
        return: list of object in sorted order
    '''
    args=movie_get_args.parse_args()
    if args['name'] is (None or ''):
        return redirect("/movie/all")
    result = MovieModel.query.filter(MovieModel.name.contains(args['name'])).order_by(collate(MovieModel.name,'NOCASE'))
    return render_template("movies.html",movies=result)

@app.route('/movie/advanceSearchAny',methods=['POST'])
def advanceSearchAny():
    '''
        Advance search for any movie name, if the search string name is even any 
        combination of any substring of movie name in the database, it will show all 
        the matching output. If no movie found, it will return empty result. 
        If search string name is empty, it will return with all the result in sorted 
        order
        
        args: string
        return: list of object in sorted order containing any of the search string
    '''
    args=movie_get_args.parse_args()
    
    if args['name'] is (None or ''):
        return redirect("/movie/all")
    
    words=args['name'].split()

    result=MovieModel.query.filter(MovieModel.name.contains(words[0]))
    for i in range(1,len(words)):
        temp=MovieModel.query.filter(MovieModel.name.contains(words[i]))
        if(i!=len(words)-1):
            result=result.union(temp)
        else:
            result=result.union(temp).order_by(collate(MovieModel.name,'NOCASE'))

    return render_template("movies.html",movies=result) 

@app.route('/movie/advanceSearchAll',methods=['POST'])
def advanceSearchAll():
    '''
        Advance search for any movie name, if the search string name is even any 
        combination of any substring of movie name in the database, it will show all 
        the matching output which contains all of the substring. If no movie found, it will 
        return empty result. If search string name is empty, it will return with all the 
        result in sorted order
        
        args: string
        return: list of object in sorted order containing all of the search string
    '''
    args=movie_get_args.parse_args()
    
    if args['name'] is (None or ''):
        return redirect("/movie/all")
    
    words=args['name'].split()
    
    result=MovieModel.query.filter(MovieModel.name.contains(words[0]))
    for i in range(1,len(words)):
        temp=MovieModel.query.filter(MovieModel.name.contains(words[i]))
        if(i!=len(words)-1):
            result=result.intersect(temp)
        else:
            result=result.intersect(temp).order_by(collate(MovieModel.name,'NOCASE'))

    return render_template("movies.html",movies=result) 

@app.route('/movie/generatePdf',methods=['POST'])
def generatePdf():
    '''
        generates pdf of list of all movies
    '''
    document= setPdfSetting()
    page_width = document.w - 2 * document.l_margin
    th = document.font_size * 2
	
    result=MovieModel.query.order_by(collate(MovieModel.name,'NOCASE')).all()

    for row in result:
        mv="name: {}, image: {}, description: {}, dateLastEdited: {}".format(row.name,row.image,row.description,row.dateLastEdited)
        document.multi_cell(w=page_width,h=th,txt=mv,border=1)
        document.ln()

    response = make_response(document.output(dest='S').encode('latin-1'))
    response.headers.set('Content-Disposition', 'attachment', filename= 'queryResult.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response

if __name__=='__main__':
    app.run(debug=True) # remove debug, which is used for production environment
