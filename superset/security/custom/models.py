from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer

class CustomSupersetUser(User):
    """
    Overriding the default flask user model, to add our stcs 3lc id column
    """
    __tablename__ = 'ab_user'
    stcs_3lc_id = Column(Integer)