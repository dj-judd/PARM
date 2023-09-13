"""CRUD operations."""
import model

import create
import read
import update
import delete
import archive



if __name__ == '__main__':
    from server import app
    model.connect_to_db(app)