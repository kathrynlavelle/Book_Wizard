# app.py

# A Flask RESTful API application, implementing simple CRUD methods within the context of a bookstore.
# Author: Kathryn Lavelle

from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)
app.json.sort_keys = False # Disable flask sorting behavior to ensure JSON fields are in desired order

# Connect to MySQL database
# TODO: replace with your database details
def get_db_connection():
    return pymysql.connect(
        host='',
        user='',
        password='',
        database=''
    )

# Utility function to return book details
def get_book_details(book_id=None):
    # Database connection
    mysql_conn = get_db_connection()
    mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

    query = """
        SELECT
            b.book_id,
            b.title,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS author,
            b.published_year,
            b.price,
            b.isbn,
            i.location,
            MAX(i.quantity) AS inventory
        FROM books b
        LEFT JOIN inventory i ON b.book_id = i.book_id
        LEFT JOIN book_author ba ON b.book_id = ba.book_id
        LEFT JOIN authors a ON ba.author_id = a.author_id
    """
    
    # If book_id is provided, only show details for that book
    if book_id:
        query += " WHERE b.book_id = %s"
        query += " GROUP BY b.book_id, b.title, b.published_year, b.price, b.isbn, i.location" # aggregate author rows for each book_id
        mysql_cursor.execute(query, (book_id,))
    else:
        query += " GROUP BY b.book_id, b.title, b.published_year, b.price, b.isbn, i.location"  # aggregate author rows for each book_id
        mysql_cursor.execute(query)

    books = mysql_cursor.fetchall()
    
    # Close connection
    mysql_cursor.close()
    mysql_conn.close()

    # If no book_id, return the full list of books
    if not book_id:
        return books
    else:
        if books:
            return books
        else: # Else no book is found
            return None

# Utility function to split author name
def split_author_name(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        raise ValueError("Author name must contain at least a first and last name")
    first_name = " ".join(parts[:-1])
    last_name = parts[-1] # assume the last word is the last name
    return first_name, last_name

# Route to home
@app.route("/")
def home():
    return render_template('index.html')

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = get_book_details()
    return jsonify(books)

# Route to get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_details(book_id)
    if book:
        return jsonify(book[0])
    return jsonify({"message": "Book not found"}), 404

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    required_fields = ['title', 'author', 'published_year', 'price', 'inventory']

    if not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    # Get values for the required fields
    title = data['title']
    author_full = data['author']
    published_year = data['published_year']
    price = data['price']
    quantity = data['inventory']

    # Check if the request contains values for the optional fields
    # If not, set a default value
    isbn = data.get('isbn', None)
    publisher_id = data.get('publisher_id', 1)
    location = data.get('location', 'Warehouse A')
    bio = f"Author of '{title}'"

    # Split author into first and last name using utility function
    try:
        first_name, last_name = split_author_name(author_full)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    # Database connection
    mysql_conn = get_db_connection()
    mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Insert book
        mysql_cursor.execute("""
            INSERT INTO books (title, isbn, published_year, price, publisher_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, isbn, published_year, price, publisher_id))
        book_id = mysql_cursor.lastrowid # save the last inserted book_id

        # Insert inventory
        mysql_cursor.execute("""
            INSERT INTO inventory (book_id, quantity, location)
            VALUES (%s, %s, %s)
        """, (book_id, quantity, location))

        # Check if author exists
        mysql_cursor.execute("""
            SELECT author_id FROM authors
            WHERE first_name = %s AND last_name = %s
        """, (first_name, last_name))
        author = mysql_cursor.fetchone()

        # If author already exists, get existing author_id
        if author:
            author_id = author['author_id']
        # Else insert and get the new author_id
        else:
            mysql_cursor.execute("""
                INSERT INTO authors (first_name, last_name, bio)
                VALUES (%s, %s, %s)
            """, (first_name, last_name, bio))
            author_id = mysql_cursor.lastrowid

        # Add author and book bridge
        mysql_cursor.execute("""
            INSERT INTO book_author (book_id, author_id)
            VALUES (%s, %s)
        """, (book_id, author_id))

        mysql_conn.commit()

        # Return the new book details
        new_book = get_book_details(book_id=book_id)
        if new_book:
            return jsonify({
                "message": "Book added successfully",
                "book": new_book[0]
            }), 201
        else:
            return jsonify({
                "message": "Book was added, but could not retrieve the details."
            }), 201

    except Exception as e:
        mysql_conn.rollback() # rollback insertions if there was an error
        return jsonify({"error": str(e)}), 500

    finally:
        mysql_cursor.close()
        mysql_conn.close()

# Route to update a book by ID
@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.json
    if not data:
        return jsonify({"message": "No request data provided"}), 400

    # Database connection
    mysql_conn = get_db_connection()
    mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Check if book exists
        mysql_cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        if not mysql_cursor.fetchone():
            return jsonify({"message": "Book not found"}), 404

        fields = []
        values = []

        # Get book fields to update
        for field in ['title', 'isbn', 'published_year', 'price', 'publisher_id']:
            if field in data:
                fields.append(f"{field} = %s")
                values.append(data[field])

        # Update book fields if provided
        if fields:
            values.append(book_id)
            update_query = f"UPDATE books SET {', '.join(fields)} WHERE book_id = %s"
            mysql_cursor.execute(update_query, tuple(values))

        # Update inventory fields if provided
        inventory_fields = []
        inventory_values = []

        if 'inventory' in data:
            inventory_fields.append("quantity = %s")
            inventory_values.append(data['inventory'])

        if 'location' in data:
            inventory_fields.append("location = %s")
            inventory_values.append(data['location'])

        if inventory_fields:
            inventory_values.append(book_id)
            mysql_cursor.execute(
                f"UPDATE inventory SET {', '.join(inventory_fields)} WHERE book_id = %s",
                tuple(inventory_values)
            )

        mysql_conn.commit()

        # Get the updated book
        updated_book = get_book_details(book_id)
        if not updated_book:
            return jsonify({"error": "Book updated but details could not be retrieved"}), 500

        return jsonify({
            "message": "Book updated successfully",
            "book": updated_book[0]
        }), 200

    except Exception as e:
        mysql_conn.rollback() # rollback any updates if there was an error
        return jsonify({"error": str(e)}), 500

    finally:
        mysql_cursor.close()
        mysql_conn.close()


# Route to delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Database connection
    mysql_conn = get_db_connection()
    mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)

    try:
        # Check if the book exists
        mysql_cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        if not mysql_cursor.fetchone():
            return jsonify({"message": "Book not found"}), 404

        # Delete related records first to ensure referential integrity
        mysql_cursor.execute("DELETE FROM book_author WHERE book_id = %s", (book_id,))
        mysql_cursor.execute("DELETE FROM book_genre WHERE book_id = %s", (book_id,))
        mysql_cursor.execute("DELETE FROM inventory WHERE book_id = %s", (book_id,))
        mysql_cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))

        mysql_conn.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

    except Exception as e:
        mysql_conn.rollback() # rollback deletions if there was an error
        return jsonify({"error": str(e)}), 500

    finally:
        mysql_cursor.close()
        mysql_conn.close()
    


if __name__ == "__main__":
        app.run(debug=True)