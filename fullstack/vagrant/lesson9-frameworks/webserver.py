from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from connector import *

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += "<form method='POST' enctype='multipart/form-data'\
                 action='hello'><h2>What would you like me to say?</h2><input\
                 name='message' type='text'><input type='submit' value=\
                 'Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1><a href = '/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data'\
                 action='hello'><h2>What would you like me to say?</h2><input\
                 name='message' type='text'><input type='submit' value=\
                 'Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<a href='restaurants/new'>Make a New Restaurant Here</a>"
                output += "<br><br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "<br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "<br><br>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data'\
                 action='/restaurants/new'><input\
                 name='newRestaurantName' type='text'>\
                 <input type='submit' value='Create'></form>"
                output += "<br><br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split('/')[-2]
                restaurantQ = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if restaurantQ:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>%s</h1>" % restaurantQ.name
                    output += "<form method='POST' enctype='multipart/form-data'\
                     action='/restaurants/%s/edit'><input\
                     name='newRestaurantName' type='text'>\
                     <input type='submit' value='Rename'></form>" % restaurantIDPath
                    output += "<br><br>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split('/')[-2]
                restaurantQ = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if restaurantQ:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?</h1>" % restaurantQ.name
                    output += "<form method='POST' enctype='multipart/form-data'\
                     action='/restaurants/%s/delete'>\
                     <input type='submit' value='Delete'></form>" % restaurantIDPath
                    output += "<br><br>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    return


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                newRestaurantName = Restaurant(name=messagecontent[0])
                session.add(newRestaurantName)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split('/')[-2]
                    restaurantQ = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if restaurantQ != []:
                        restaurantQ.name = messagecontent[0]
                        session.add(restaurantQ)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split('/')[-2]
                restaurantQ = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if restaurantQ != []:
                    session.delete(restaurantQ)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()
