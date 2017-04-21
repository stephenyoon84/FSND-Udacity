import os

import jinja2
import webapp2
from signup_back import *
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u



def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, signup, **params):
        params['user'] = self.user
        return render_str(signup, **params)

    def render(self, signup, **kw):
        self.write(self.render_str(signup, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

class MainPage(Handler):
    # render mainpage.html
    def get(self):
        self.render("mainpage.html")

class Signup(Handler):
    def get(self):
        self.render("sign_up.html")

    def post(self, error_username = "",
            error_password = "", error_verify = "",
            error_email = ""):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify = self.request.get("verify")
        self.email = self.request.get("email")

        params = dict(username = self.username,
                      email = self.email)

        v_username = valid_username(self.username)
        v_password = valid_password(self.password)
        v_verify = verify_password(self.password, self.verify)
        v_email = valid_email(self.email)

        if not (v_username and v_password and v_verify and v_email):
            if not v_username:
                error_username = "That's not a valid username."
            if not v_password:
                error_password = "That wasn't a valid password."
            if not v_verify:
                error_verify = "Your passwords didn't match."
            if not v_email:
                error_email = "That's not a valid email."
            self.render("sign_up.html", username = self.username, email = self.email,
                        error_username = error_username,
                        error_password = error_password,
                        error_verify = error_verify,
                        error_email = error_email)
        else:
            # user_id = db.GqlQuery("SELECT * FROM User_Info WHERE user_id = '%s'" % username)
            # if username in user_id:
            #     error_username = "That user already exists"
            #     self.render("sign_up.html", username = username, email = email,
            #                 error_username = error_username)
            # else:
            #     user_db = User_Info(parent = blog_key(), user_id=username,
            #                         user_pw_hash=password, user_email=email,
            #                         visited_time = 1)
            #     user_db.put()
            #     self.redirect("/welcome")
            self.done()

        def done(self, *a, **kw):
            raise NotImplementedError

class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('sign_up.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.set_secure_cookie('user_id', str(u.key().id()))
            self.redirect('/welcome')

class WelcomeHandler(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('signup')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/welcome', WelcomeHandler),
                               ('/signup', Register),
                              ], debug = True)
