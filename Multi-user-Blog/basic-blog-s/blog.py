import os
import webapp2
import jinja2

from back_etc import *
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        # set cookie for user
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        # request cookie from user
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


class MainPage(BlogHandler):
    # render mainpage.html
    def get(self):
        self.render("mainpage.html")


def users_key(group='default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    # user database - contain user's name, pw hash, and email
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        # create pw_hash
        pw_hash = make_pw_hash(name, pw)
        return User(parent=users_key(), name=name,
                    pw_hash=pw_hash, email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


def blog_key(name='default'):
    return db.Key.from_path('posts', name)


class Post(db.Model):
    # post database - contain subject content and
    # created datetime last modified datetime
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)


class BlogPosts(BlogHandler):
    def get(self):
        # posts = Post.all().order('-created')
        posts = db.GqlQuery("select * from Post\
        order by created desc")  # - using GqlQuery example
        self.render('blogpost.html', posts=posts)


class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post)


class NewPost(BlogHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content)
            p.put()
            self.redirect("/blog/%s" % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject,
                        content=content, error=error)


class SignUpPage(BlogHandler):
    def get(self):
        self.render("sign_up.html")

    def post(self):
        have_error = False
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
            self.render("sign_up.html", username=username, email=email,
                        error_username=error_username,
                        error_password=error_password,
                        error_verify=error_verify,
                        error_email=error_email)
        else:
            u = User.by_name(username)
            if u:
                msg = "That user already exists."
                self.render('sign_up.html', error_username=msg)
            else:
                u = User.register(username, password, email)
                u.put()

                self.login(u)
                self.redirect('/welcome')


class WelcomeHandler(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')


class Login(BlogHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = "Invalid login"
            self.render('login.html', error_login=msg)


class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/login')


class Rot13Page(BlogHandler):
    def get(self):
        self.render("rot13_input.html")

    def post(self):
        items = self.request.get("text")
        result = ''
        for i in items:
            if i in rot13_set:
                result += rot13_set[rot13_set.index(i) + 13]
            else:
                result += i
        self.render("rot13_input.html", rot13_result=result)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', BlogPosts),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', SignUpPage),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', WelcomeHandler),
                               ('/rot13', Rot13Page),
                               ], debug=True)
