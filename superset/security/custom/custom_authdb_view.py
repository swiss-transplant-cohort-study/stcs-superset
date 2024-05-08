import logging
import os

from flask import flash, g, redirect, request
from flask_appbuilder.security.views import AuthDBView, expose
from flask_login import login_user
from sqlalchemy import create_engine
from superset.security.custom.utils import SupersetAuth, User

class CustomAuthDBView(AuthDBView):
    """
    Custom auth view to handle 3LC login into Superset
    """
    login_template = "appbuilder/general/security/login_db.html"
    superset_postgres_password = os.getenv("SUPERSET_POSTGRES_PASSWORD")
    superset_postgres_host = os.getenv("SUPERSET_POSTGRES_HOST", "postgres-superset")
    superset_postgres_port = os.getenv("SUPERSET_POSTGRES_PORT", "5432")

    def create_connection(self):
        """
        Creating connection to Superset DB
        """

        engine = create_engine(
            f"postgresql+psycopg2://postgres:{self.superset_postgres_password}@{self.superset_postgres_host}:{self.superset_postgres_port}"
        )
        connection = engine.connect()
        return connection

    def execute_query(self, connection, query):
        """
        This method will create the connection between 3LC and the Superset DB
        and execute the provided query
        """
        results = connection.execute(query)
        return results

    @expose("/login/", methods=["GET", "POST"])
    def login(self):
        """
        Overriding login view
        """
        authsuccess = False
        username = ""
        uid = 0
        token = ""
        redirect_url = self.appbuilder.get_url_for_index

        if request.args.get("redirect") is not None:
            redirect_url = request.args.get("redirect")
        if request.args.get("username") is not None:
            username = request.args.get("username")
        if request.args.get("token") is not None:
            token = request.args.get("token")
        if request.args.get("user_id") is not None:
            uid = request.args.get("user_id")

        if username != "":
            connection = self.create_connection()
            results = self.execute_query(
                connection, f"SELECT * FROM users_3lc WHERE token='{token}'"
            ).fetchall()

            if results:
                tokens = [SupersetAuth(*result) for result in results]
                if all(token.consumed is True for token in tokens):
                    flash("InvalidToken", "warning")
                    return super().login()

                authsuccess = True
        if g.user is not None and g.user.is_authenticated and not authsuccess:
            logging.info("Failed here")

        if authsuccess:
            login_user(User(username, uid), remember=False)
            return redirect(redirect_url)

        flash("Auto Login Failed", "warning")
        return super().login()

