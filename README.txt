# README

# BookWizard: A Flask RESTful API application, implementing simple CRUD methods within the context of a bookstore.
# Author: Kathryn Lavelle

# The app connects to an existing database and exposes the following endpoints:
    - Retrieve all books: GET /books
    - Retrieve a book by ID: GET /books/<id>
    - Add a new book: POST /books
    - Update a book's details: PATCH /books/<id>
    - Delete a book: DELETE /books/<id>


# Instructions to run BookWizard app:
1. Open your terminal and navigate to your project directory.

2. Create / Activate the virtual environment.
    bash (create venv): python -m venv venv

    The command depends on your operating system and the name of your venv folder (commonly named venv or .venv).
        bash (activate venv): venv\Scripts\activate

    Once activated, your command prompt will show the environment name in parentheses, like (venv)

3. Install Flask.
    Make sure Flask is installed within this specific environment:
        bash (install Flask): pip install flask

    If you have a requirements.txt file, you can install all dependencies at once:
        bash (install requirements): pip install -r requirements.txt

4. Run the Flask application.
    Use the flask run command to start the development server:
        bash (run app): flask run

5. When finished, deactivate the virtual environment.
    bash (deactivate venv): deactivate