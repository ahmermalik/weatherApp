import os         ##this is wused when you're deploying server. it is ok to add it in the beginning of your project.
import tornado.ioloop
import tornado.web
import tornado.log

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
        # render input form
    self.render_template("home.html", {})

    def post(self):
        pass
        # get city name

        # lookup the weather

        # render the weather data


def make_app():                                 ##make_app will return the application and all the routing logic within it.
    return tornado.web.Application([
        (r"/", MainHandler),
        (
         r"/static/(.*)",                           ##this helps the server find the static folder which goes with all the main files.
         tornado.web.StaticFileHandler,
         {'path': 'static'}
        ),
        ], autoreload=True)


PORT = int(os.environ.get('PORT','1337'))
if __name__ == "__main__":
    tornado.log.enable_pretty_logging()

app = make_app()
app.listen(PORT, print('Server started on localhost: ' + str(PORT)))
tornado.ioloop.IOLoop.current().start()
