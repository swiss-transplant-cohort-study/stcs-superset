from flask_login import UserMixin


class User(UserMixin):
    """
    Simple User class to authenticate 3LC users
    """

    def __init__(self, username, uid):
        self.username = username
        self.id = uid


class SupersetAuth:
    """
    Used to facilate the handling of db results
    """

    def __init__(
        self,
        dbid,
        token,
        username,
        consumed,
        creationDate,
        expirationDate,
        consumedDate,
        userId,
    ):
        self.id = dbid
        self.token = token
        self.username = username
        self.consumed = consumed
        self.creationDate = creationDate
        self.expirationDate = expirationDate
        self.consumedDate = consumedDate
        self.userId = userId
