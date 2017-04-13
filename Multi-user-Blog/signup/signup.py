import os

import jinja2
import webapp2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, signup, **params):
        t = jinja_env.get_template(signup)
        return t.render(params)

    def render(self, signup, **kw):
        self.write(self.render_str(signup, **kw))

class MainPage(Handler):
    def get(self):
        self.render("sign_up.html")

    def post(self, error_username = "",
            error_password = "", error_verify = "",
            error_email = ""):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        v_username = valid_username(username)
        v_password = valid_password(password)
        v_verify = verify_password(password, verify)
        v_email = valid_email(email)

        if not (v_username and v_password and v_verify and v_email):
            if not v_username:
                error_username = "That's not a valid username."
            if not v_password:
                error_password = "That wasn't a valid password."
            if not v_verify:
                error_verify = "Your passwords didn't match."
            if not v_email:
                error_email = "That's not a valid email."
            self.render("sign_up.html", username = username, email = email,
                        error_username = error_username,
                        error_password = error_password,
                        error_verify = error_verify,
                        error_email = error_email)
        else:
            self.redirect("/welcome?username=%s" % username)




class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render("welcome.html", username=username)

app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', WelcomeHandler)
], debug = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+..[\S]+$")
def valid_username(username):
    return USER_RE.match(username)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_email(email):
    if email == "":
        return True
    elif email != "":
        return EMAIL_RE.match(email)
def verify_password(password, verify):
    if password == verify:
        return True
    else:
        return False
