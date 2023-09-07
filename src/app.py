from flask import Flask, jsonify, request, redirect, url_for
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

connection = MySQL(app)


@app.route('/')
def index():
    return redirect(url_for('list_books'))


@app.route('/api/books', methods=['GET'])
def list_books():
    try:
        cursor = connection.connection.cursor()
        sql = "SELECT * FROM libros"
        cursor.execute(sql)
        data = cursor.fetchall()
        books = []
        for book_info in data:
            book = {
                'id': book_info[0], 
                'title': book_info[1], 
                'synopsis': book_info[2], 
                'author': book_info[3],
                'editorial': book_info[4],
                'volume': book_info[5]
                }
            books.append(book)
        return jsonify({'books': books})
    except Exception as ex:
        return jsonify({'message': ex.message})


@app.route('/api/books/<id>', methods=['GET'])
def read_book(id):
    try:
        cursor = connection.connection.cursor()
        sql = "SELECT * FROM libros WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            book = {
                'id': data[0], 
                'title': data[1], 
                'synopsis': data[2], 
                'author': data[3],
                'editorial': data[4],
                'volume': data[5]
                }
            return jsonify({'books': book})
        else:
            return jsonify({'message': "Element not found"})
    except Exception as ex:
        return jsonify({'message': ex.message})


@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        cursor = connection.connection.cursor()
        sql = """
        INSERT INTO books 
        (id, name, synopsis, author, editorial, volume) 
        VALUES ({0}, '{1}', '{2}', '{3}', '{4}', {5})
        """.format(
            request.json['id'], 
            request.json['name'], 
            request.json['synopsis'], 
            request.json['author'], 
            request.json['editorial'], 
            request.json['volume'])
        cursor.execute(sql)
        connection.connection.commit()
       
        return jsonify({'books': request.json})
    except Exception as ex:
        return jsonify({'message': ex.message})


@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    try:
        cursor = connection.connection.cursor()
        sql = "DELETE FROM books WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        connection.connection.commit()
        return jsonify({'books': "Book deleted successfully"})
    except Exception as ex:
        return jsonify({'message': ex.message})



@app.route('/api/books/<id>', methods=['PUT'])
def update_book(id):
    try:
        cursor = connection.connection.cursor()
        sql = """UPDATE books 
        SET name = '{0}', 
        synopsis = '{1}', 
        author = '{2}', 
        editorial = '{3}', 
        volume = {4} 
        WHERE id = '{5}' 
        """.format(
            request.json['name'], 
            request.json['synopsis'], 
            request.json['author'], 
            request.json['editorial'], 
            request.json['volume'], 
            id
            )
        cursor.execute(sql)
        connection.connection.commit()
       
        return jsonify({'books': "book updated successfully"})
    except Exception as ex:
        return jsonify({'message': ex.message})




def page_not_found(error):
    return redirect(url_for('list_books')), 404

"""
MAIN
"""

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.run()