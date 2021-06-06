from flask_restful import reqparse,fields
from fpdf import FPDF

#function to set Pdf setting
def setPdfSetting():
    document = FPDF()
    document.add_page()
    document.set_font('Times','B',14.0)
    page_width = document.w - 2 * document.l_margin
    document.cell(page_width, 0.0, 'Movie Data', align='C') 
    document.set_font('Courier', '', 12)
    document.ln(10)
    return document

#delete request parser
movie_get_args = reqparse.RequestParser()
movie_get_args.add_argument("name",type=str,help="Name of the movie",required=True)

#post request parser
movie_post_args = reqparse.RequestParser()
movie_post_args.add_argument("name",type=str,help="Name of the movie",required=True)
movie_post_args.add_argument("image",type=str,help="url of the movie image")
movie_post_args.add_argument("description",type=str,help="Description of the movie")

#delete request parser
movie_delete_args = reqparse.RequestParser()
movie_delete_args.add_argument("name",type=str,help="Name of the movie",required=True)

#update request parser
movie_update_args = reqparse.RequestParser()
movie_update_args.add_argument("oldtitle",type=str,required=True)
movie_update_args.add_argument("name",type=str,help="Name of the movie")
movie_update_args.add_argument("image",type=str,help="url of the movie image")
movie_update_args.add_argument("description",type=str,help="Description of the movie")

#response formatting
movie_resource_fields={
    'name':fields.String,
    'image':fields.String,
    'description':fields.String,
    'dateLastEdited':fields.DateTime
}