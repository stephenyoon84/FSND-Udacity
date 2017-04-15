import os
import webapp2
import jinja2
import re

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class BlogContent(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render('base.html')

class BlogPage(Handler):
    def render_blog(self, subject="", content="", error="", created=""):
        posts = db.GqlQuery("SELECT * FROM BlogContent ORDER by created desc limit 10")
        self.render("blog.html", subject=subject,
                    content=content, created=created, posts=posts)
    def get(self):
        self.render_blog()

class NewPost(Handler):
    def get(self):
        self.render("newpost.html")
    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            c = BlogContent(subject = subject, content = content)
            c_key = c.put()
            self.redirect('/blog/%d' % c_key.id())
        else:
            error = "we need both a title and some artwork!"
            self.render("newpost.html", subject = subject,
                        content = content, error=error)

class Permalink(BlogPage):
    def get(self, posts_id):
        s = BlogContent.get_by_id(int(posts_id))
        self.render("post.html", s=s)

app = webapp2.WSGIApplication([(r'/', MainPage),
                            (r'/blog', BlogPage),
                            (r'/blog/newpost', NewPost),
                            (r'/blog/(\d+)', Permalink)],
                             debug = True)
