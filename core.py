import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

if application.config.get('FQDN') is None:
    with open('private/config.json') as private_config:
        config_dict = json.load(private_config)
    application.config['FQDN'] = config_dict['fqdn']
    application.config['CERT'] = config_dict['cert']
    application.config['PORT'] = config_dict['port']
    application.config['TOKEN'] = config_dict['token']
    application.config['API_URL'] = 'https://api.telegram.org/bot' + \
        application.config['TOKEN']

# SQLAlchemy setup
with open('private/config.json') as private_config:
    config_dict = json.load(private_config)
DB_URL = 'postgresql://{user}:{pass}@{host}/{database}'.format_map(
    config_dict['db'])
application.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)
