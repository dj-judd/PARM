"""Server for parm app."""
import os
import sys
from flask import Flask
from dotenv import load_dotenv

from database import crud, model, permissions
from backend_tools import utils



load_dotenv()

db_password = os.getenv("DATABASE_PASSWORD")

app = Flask(__name__)

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://parm_server:{db_password}@localhost/parm'

model.db.init_app(app)


# Replace this with routes and view functions!


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)