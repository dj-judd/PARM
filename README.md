# P.A.R.M. - Production Asset Reservation Management 🎥💼

## Overview 🌐

P.A.R.M. is a web application designed to track and manage large sets of production assets. Ideal for teams, it offers features for flagging problematic assets, reserving assets, and tracking their financial metrics. It's built using Flask, Jinja templates, and React.

## Features 🛠️

- **Asset Reservation**: Reserve assets in advance. Once reserved, assets are locked to prevent double-booking.
- **Flagging Assets**: Flag assets that have issues, making it easier to track and resolve.
- **Financial Tracking**: Run reports on asset depreciation and other financial metrics.

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

## Reporting 📊

To run financial reports, navigate to the `Reports` section in the application. 

## Contribution 🤝

If you'd like to contribute, please fork the repository and create a pull request.

## License 📝

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For any additional questions or feedback, please contact the development team.
