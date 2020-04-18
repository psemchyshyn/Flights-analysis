from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


from dash_app1 import app1
from flask_app import flask_app

application = DispatcherMiddleware(flask_app, {
    '/origin_destination_analysis': app1.server
})


if __name__ == '__main__':
    run_simple('localhost', 8050, application)
