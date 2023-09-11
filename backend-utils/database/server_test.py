from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import crud
import model
import permissions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://server_test:password@localhost/parm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


model.db.init_app(app)

@app.route('/create_user', methods=['POST'])
def api_create_user():
    try:
        data = request.json

        password_hash = data['password_hash']
        first_name = data['first_name']
        last_name = data['last_name']
        currency_id = data['currency_id']
        created_by_user_id = data['created_by_user_id']
        
        # Optional fields with default values
        time_format_is_24h = data.get('time_format_is_24h', False)
        audit_details = data.get('audit_details', None)
        ui_theme_id = data.get('ui_theme_id', 1)
        middle_name = data.get('middle_name', None)
        nickname = data.get('nickname', None)
        nickname_preferred = data.get('nickname_preferred', None)
        last_login = data.get('last_login', None)

        user, user_audit_entry, user_settings, user_settings_audit_entry = crud.create_user(
            password_hash,
            first_name,
            last_name,
            currency_id,
            created_by_user_id,
            time_format_is_24h,
            audit_details,
            ui_theme_id,
            middle_name,
            nickname,
            nickname_preferred,
            last_login
        )

        return jsonify({
            'status': 'success',
            'user_id': user.id,
            'user_audit_entry_id': user_audit_entry.id,
            'user_settings_id': user_settings.id,
            'user_settings_audit_entry_id': user_settings_audit_entry.id
        }), 201

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(port=5000)
