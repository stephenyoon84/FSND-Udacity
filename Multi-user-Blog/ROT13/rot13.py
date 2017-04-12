import os

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, rot13, **params):
        t = jinja_env.get_template(rot13)
        return t.render(params)

    def render(self, rot13, **kw):
        self.write(self.render_str(rot13, **kw))

class MainPage(Handler):
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
        self.render("rot13_input.html", rot13_result = result)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

rot13_set = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
            'Q','R','S','T','U','V','W','X','Y','Z','A','B','C','D','E','F','G',
            'H','I','J','K','L','M',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z','a','b','c','d','e','f','g',
            'h','i','j','k','l','m']
