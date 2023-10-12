# P.A.R.M. - Production Asset Reservation Management 🎥💼

## Overview 🌐

P.A.R.M. is a web application designed to track and manage large sets of production assets. Ideal for teams, it offers features for flagging problematic assets, and reserving assets. It's built using Flask, Jinja templates, and React.

## Features 🛠️

- **Asset Reservation**: Reserve assets in advance. Once reserved, assets are locked to prevent double-booking.
- **Asset History Tracking**: Pull up the reservation history of an asset and see who has reserved it in the past.
- **Flagging Assets**: Flag assets that have issues, making it easier to track and resolve.

## Tech Stack 🖥️

- Flask
- Jinja Templates
- React

## How to Run 🚀

1. Clone the repository
```bash
git clone https://github.com/yourusername/PARM.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Popluate Database
```
python3 -m database.seed_database
```
from "~/src/PARM-Production_Asset_Reservation_Manager/backend$"

4. Run the Flask server in `/backend`
```bash
python server.py
```