""" This module is the entry point for the Flask application.
    It initializes the app, sets up the database, and runs the server.
"""

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # app.run(debug=True, host='', port=80)
    app.run(debug=True)
