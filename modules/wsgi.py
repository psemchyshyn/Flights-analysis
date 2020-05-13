'''
FligthsDetector
Pavlo Semchyshyn
'''

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple


from data_dashapps.app1 import app1
from data_dashapps.app2 import app2
from flask_app import flask_app

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    '/app2': app2.server,
})


if __name__ == '__main__':
    run_simple('localhost', 8050, application)
