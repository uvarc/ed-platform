#!/bin/bash

# Run the basic operations to update a production setup after a code change.
# This script should be executed by a post_recieve git hook after completing
# a checkout.
# --------------------------------------------------------------------------

# Move the configuration file into place.
mkdir -p ./backend/instance
cp /home/ubuntu/edp_config.py ./backend/instance/config.py

# Update the database
source activate edp
export APP_CONFIG_FILE="../config/default.py"
cd backend && python manage.py clear_data
cd backend && python manage.py db upgrade
cd backend && python manage.py load_data

# Rebuild the front end.
cd frontend && ng build -dist

# Reload apache
sudo service apache2 reload
