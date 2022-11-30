from dash_auth.auth import Auth
import base64
import flask
import login

class LdapAuth(Auth):

    def __init__(self, app):
        Auth.__init__(self, app)
        self.username = None
        self.password = None

    def is_authorized(self):
        header = flask.request.headers.get("Authorization", None)
        if not header:
            return False

        username_password = base64.b64decode(header.split("Basic ")[1])
        username_password_utf8 = username_password.decode("utf-8")
        username, password = username_password_utf8.split(":", 1)

        if self.username == username and self.password == password:
            return True

        authorized = login.login_user(username, password)

        if authorized:
            self.username = username
            self.password = password

        return authorized

    def login_request(self):
        return flask.Response(
            "LDAP Login Required",
            headers={"WWW-Authenticate": 'Basic realm="User Visible Realm"'},
            status=401
        )

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()
        return wrap
