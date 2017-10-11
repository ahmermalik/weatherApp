import os         ##this is wused when you're deploying server. it is ok to add it in the beginning of your project.
import tornado.ioloop
import tornado.web
import tornado.log
#from models import weather
import requests

from jinja2 import \
  Environment, PackageLoader, select_autoescape                     #This is setting up jinja to know where the python module is located.

ENV = Environment(                                                  #the module and which directory within the module has your templates
  loader=PackageLoader('myapp', 'templates'),
  autoescape=select_autoescape(['html', 'xml'])
)


class TemplateHandler(tornado.web.RequestHandler):
  def render_template (self, tpl, context):
    template = ENV.get_template(tpl)
    self.write(template.render(**context))


class MainHandler(TemplateHandler):
  def get(self):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')

    self.render_template("home.html", {})

  def post(self):
    url = "http://api.openweathermap.org/data/2.5/weather"

    city = self.get_body_argument('city_name')
    querystring = {"q": city, "APIKEY": "c33c99977dff2b8b60a9b4be2d2046fd"}
    response = requests.get(url, params=querystring)
    print(response.json())
    self.render_template("home.html", {'data': response.json()}) ##self.render is the template and the 'data': response.json() is the context.

class PageHandler(TemplateHandler):
  def get(self, page):
    self.set_header(
      'Cache-Control',
      'no-store, no-cache, must-revalidate, max-age=0')
    self.render_template(page + '.html', {})


def make_app():                                 ##make_app will return the application and all the routing logic within it.
    return tornado.web.Application([
    (r"/", MainHandler),
    (r"/weather/(.*)", PageHandler),
    (r"/static/(.*)",                           ##this helps the server find the static folder which goes with all the main files.
     tornado.web.StaticFileHandler,
     {'path': 'static'}
    ),
    ], autoreload=True)


PORT = int(os.environ.get('PORT', '1337'))
if __name__ == "__main__":
    tornado.log.enable_pretty_logging()

app = make_app()
app.listen(PORT, print('Server started on localhost: ' + str(PORT)))
tornado.ioloop.IOLoop.current().start()
