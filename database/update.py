"Update methods for DB Entities"

import model
from backend_utils import utils

from typing import Optional
from datetime import datetime




# UPDATE





def default_currency(default_currency_id, commit=True):
    """Update the default currency in the global_settings table."""
    global_settings = model.db.session.query(model.GlobalSettings).first()
    
    if global_settings:
        # Update the default_currency_id
        global_settings.default_currency_id = default_currency_id
        if commit:
            model.db.session.commit()
            utils.successMessage()
        
        # Return the updated default currency ID
        return global_settings.default_currency_id
    else:
        utils.errorMessage("Global settings entry not found.")
        return None