"""Server for parm app."""
import os
import sys
from flask import Flask, render_template
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
@app.route('/asset-grid')
def asset_grid():
    assets = crud.read.Asset.all(requesting_user_id=1, include_archived=False)
    
    # Assuming you have a theme_id variable with the ID of the UiTheme you want to retrieve
    theme_id = 2  # Replace with the actual theme ID you want to use
    
    theme_colors = crud.read.UiTheme.colors_by_id(theme_id)  # Get the theme colors

    if theme_colors is not None:
        primary_color = theme_colors['primary_color_id']
        secondary_color = theme_colors['secondary_color_id']
    else:
        primary_color = "#000000"  # Default white
        secondary_color = "#FFFFFF"  # Default black
    
    return render_template('asset_grid.html', assets=assets, primary_color=primary_color, secondary_color=secondary_color)


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)