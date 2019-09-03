from core import db
# import models
from models.gkeep_user import GKeepUser

db.drop_all()
db.create_all()
db.session.commit()
