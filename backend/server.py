"""Server for parm app."""
import os
import sys
from flask import Flask, render_template, jsonify, send_from_directory, redirect, url_for, request
from dotenv import load_dotenv

from database import crud, model, permissions
from tools import utils



load_dotenv()

db_password = os.getenv("DATABASE_PASSWORD")

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://parm_server:{db_password}@localhost/parm'

model.db.init_app(app)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Replace this with routes and view functions!





@app.route('/custom_static/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend/static', filename)

@app.route('/components/<path:filename>')
def serve_components(filename):
    return send_from_directory('../frontend/components', filename)

@app.route('/file_attachments/<path:filename>', methods=['GET'])
def serve_attachment(filename):
    return send_from_directory('../backend/database/data/file_attachments', filename)


@app.route('/')
def landing():
    return render_template('landing.html')


#OLD METHOD (BUT WASN"T ABLE TO DO A SERVER SIDE REDIRECT)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email_address = request.form.get('email_address')
#         user = crud.read.User.by_email(email_address)
#         password = user.password_hash
        
#         if user:
#             # User authenticated successfully
#             # Set session or token here
#             return redirect(url_for('serve_app'))
#         else:
#             # Authentication failed
#             return "Invalid credentials", 401

#     return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        user = crud.read.User.by_email(email_address)
        
        if user:
            # User authenticated successfully
            # Set session or token here
            return jsonify({"status": "success"}), 200
        else:
            # Authentication failed
            return jsonify({"status": "failure", "message": "Invalid credentials"}), 401

    return render_template('login.html')

# @app.route('/')
# def index():
#     return redirect(url_for('asset_grid'))

@app.route('/asset_grid')
def asset_grid():
    assets = crud.read.Asset.all(requesting_user_id=1, include_archived=False)
    

    # primary_color = "#000000"  # Default white
    # secondary_color = "#FFFFFF"  # Default black

    primary_color = "#FFFFFF"  # Default white
    secondary_color = "#000000"  # Default black

    categories = crud.read.Category.all_ordered()
    return render_template('app.html', assets=assets, primary_color=primary_color, secondary_color=secondary_color, categories=categories)


@app.route('/app', defaults={'path': ''})
@app.route('/app/<path:path>')
def serve_app(path):
    email_cookie = request.cookies.get('email')
    password_cookie = request.cookies.get('password')

    if email_cookie and password_cookie:
        return render_template('app.html')  # Your React app will take it from here.
    else:
        return redirect('/login')


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)