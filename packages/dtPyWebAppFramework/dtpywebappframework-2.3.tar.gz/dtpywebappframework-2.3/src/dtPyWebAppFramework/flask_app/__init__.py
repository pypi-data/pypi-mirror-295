from threading import Thread
from flask import Flask, Response

import random
import sys


class FlaskAppWrapper(Thread):
    app = None

    def __init__(self, name, settings):
        super().__init__()
        self.settings = settings
        self.app = Flask(name)
        self.web_server_host = self.settings.get('web_server.host', '127.0.0.1')
        self.web_server_port = self.settings.get('web_server.port', random.randint(4040, 8080))

    def run(self):
        self.app.run(host=self.web_server_host, port=self.web_server_port, debug=False, threaded=True)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods)
