from flask import Flask
from flask_restplus import Resource, Api, fields

app=Flask(__name__) #instantiate flsk app
api=Api(app, title="Library",description="Welcome to our Simple Library",) # instantiate api

ns = api.namespace('library', description='Operations')

model=api.model('Book',{
	'book_name': fields.String(required=True, description='Details of the book'),
	"book_id": fields.Integer(readOnly=True, description='Unique identifier of a book')
	})

class lib(object):
	def __init__(self):
		self.books = [{"book_name":"Angels of IIITK","book_id":21}]
	def get(self, id):
		for book in self.books:
			if book['book_id'] == id:
				return book
		api.abort(404, "Book_id {} doesn't exist".format(id))

	def create(self, book):
		numb=book["book_id"]
		for i in self.books:
			if i["book_id"]==numb:
				api.abort(404, "Book_id {} already exist!!....... Give an other ID".format(numb))
			else:
				self.books.append(book)
				return book
	def delete(self, id):
		book = self.get(id)
		self.books.remove(book)

obj=lib()
obj.create({"book_name":"Honesty","book_id":31})
obj.create({"book_name":"Best Memories","book_id":41})

@ns.route('/')
class methods(Resource):
    @ns.doc('list_Books')
    @ns.marshal_list_with(model)
    def get(self):
        return obj.books

    @ns.doc('add_Book')
    @ns.expect(model)
    @ns.marshal_with(model, code=201)
    def post(self):
        return obj.create(api.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Book not found')
@ns.param('id', 'The Book identifier')
class methods(Resource):
    @ns.doc('delete_book')
    @ns.response(204, 'book deleted')
    def delete(self, id):
        obj.delete(id)
        return '', 204

if __name__ =='__main__':
	app.run(debug=True)
