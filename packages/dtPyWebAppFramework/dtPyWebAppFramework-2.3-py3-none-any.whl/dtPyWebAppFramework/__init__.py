import os
import sys
import importlib
import time
import logging
import webbrowser
import shutil

from argparse import ArgumentParser
from threading import Thread
from flask import request, jsonify, send_file

from dtPyAppFramework.application import AbstractApp
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.paths import ApplicationPaths

from .flask_app import FlaskAppWrapper
from .managers.content_manager import ContentManager
from .managers.tool_manager import ToolManager
from .base_tool import BaseApp
from .commons import find_base_app_class

dir_path = os.path.dirname(os.path.realpath(__file__))

# Define module-level variables with version-related information
with open(os.path.join(dir_path, 'version.dat'), 'r') as _version:
    __version__ = _version.read()

with open(os.path.join(dir_path, 'description.dat'), 'r') as _description:
    __description__ = _description.read()


# Function to retrieve the version
def version():
    """Returns the version of the module."""
    return __version__


def name():
    return "dtPyWebAppFramework"


def copyright_():
    return "© dtPyWebAppFramework Copyright 2023-2024 Digital-Thought - All Rights Reserved"


def description():
    return __description__


class WebApp(AbstractApp):

    def __init__(self, base_app) -> None:
        self.base_app: BaseApp = base_app

        super().__init__(description=self.base_app.description(),
                         version=self.base_app.version(),
                         short_name=self.base_app.short_name(),
                         full_name=self.base_app.full_name(),
                         console_app=os.environ.get("DEV_MODE", None) is not None)

        self.flask_app: FlaskAppWrapper = None
        self.settings: Settings = None
        self.resource_manager: ResourceManager = None
        self.content_manager: ContentManager = None
        self.tool_manager: ToolManager = None

    def define_args(self, arg_parser: ArgumentParser):
        arg_parser.add_argument('--dev_mode', action='store_true', required=False, help='Run in Dev Mode')

    def _open_home_page(self):
        home_url = f"http://{self.flask_app.web_server_host}:{self.flask_app.web_server_port}/"
        webbrowser.open(home_url, new=0, autoraise=True)
        logging.info(f'Web Toolkit available on: {home_url}')

    def main(self, args):
        self.settings = Settings()
        self.resource_manager = ResourceManager()
        self.flask_app = FlaskAppWrapper(self.app_spec['short_name'], settings=self.settings)
        self.resource_manager.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"))

        custom_resource_path = os.path.abspath(self.base_app.resources())
        if os.path.exists(custom_resource_path):
            logging.info(f'Adding custom application resource path: "{custom_resource_path}"')
            self.resource_manager.add_resource_path(custom_resource_path)

        self.tool_manager = ToolManager(resource_manager=self.resource_manager,
                                        settings=self.settings,
                                        base_app=self.base_app,
                                        flask_app=self.flask_app, dev_mode=args.dev_mode)
        self.content_manager = ContentManager(resource_manager=self.resource_manager,
                                              settings=self.settings,
                                              base_app=self.base_app, flask_app=self.flask_app,
                                              tool_manager=self.tool_manager,
                                              html_template_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"),
                                              core_app={'version': version(), 'name': name(), 'description': description(),
                                                        'copyright': copyright_(), 'logo': '/assets/images/dt-logo.png'}
                                              )

        self.tool_manager.load_tools(self.content_manager)

        self.flask_app.add_endpoint(endpoint='/', endpoint_name='home', handler=self.content_manager.home)
        self.flask_app.add_endpoint(endpoint='/exit', endpoint_name='exit', handler=self.exit)
        self.flask_app.add_endpoint(endpoint='/close', endpoint_name='close', handler=self.exit, methods=['POST'])
        self.flask_app.add_endpoint(endpoint='/get-about', endpoint_name='about-content', handler=self.about, methods=['GET'])
        self.flask_app.add_endpoint(endpoint='/get-settings', endpoint_name='settings-content', handler=self.settings_content, methods=['GET'])
        self.flask_app.add_endpoint(endpoint='/add-secret', endpoint_name='add-secret', handler=self.add_secret, methods=['POST'])
        self.flask_app.add_endpoint(endpoint='/clear-secrets', endpoint_name='clear-secrets', handler=self.clear_secrets, methods=['POST'])
        self.flask_app.add_endpoint(endpoint='/persist-settings', endpoint_name='persist-settings', handler=self.persist_settings, methods=['POST'])

        self.flask_app.add_endpoint(endpoint='/download-logs', endpoint_name='download-logs', handler=self.download_logs, methods=['GET'])
        self.flask_app.add_endpoint(endpoint='/open-app', endpoint_name='open-app', handler=self.open_app, methods=['POST'])
        self.flask_app.add_endpoint(endpoint='/assets/<path:path>', endpoint_name='assets', handler=self.content_manager.assets)
        self.flask_app.add_endpoint(endpoint='/app-instance/<path:guid>', endpoint_name='app-instance-home', handler=self.app_home)
        self.flask_app.add_endpoint(endpoint='/app-instance/<path:guid>/close', endpoint_name='app-instance-close', handler=self.app_close,
                                    methods=['POST'])
        self.flask_app.add_endpoint(endpoint='/app-instance/<path:guid>/get-about', endpoint_name='app-instance-about-content',
                                    handler=self.app_about_caller, methods=['GET'])
        self.flask_app.add_endpoint(endpoint='/app-instance/static/<path:path>', endpoint_name='app-instance-static', handler=self.app_home)
        self.flask_app.add_endpoint(endpoint='/app-instance/<path:guid>/<path:path>', endpoint_name='app-instance-request-handler',
                                    handler=self.app_path_caller,
                                    methods=['POST', 'GET', 'PUT', 'DELETE'])

        cli = sys.modules['flask.cli']
        log = logging.getLogger('werkzeug')
        log.disabled = True
        cli.show_server_banner = lambda *x: None
        self.flask_app.start()
        self._open_home_page()
        self.flask_app.join()

    def clear_secrets(self):
        if request.is_json:
            data = request.get_json()
            try:
                if data['scope'] is not None:
                    Settings().secret_manager.get_store(data['scope']).delete_secret(data['key'])
                    return jsonify({'state': 'success'}), 200
                else:
                    details = self.settings.secret_manager.get_local_stores_index()
                    for key in details:
                        for val in details[key]['index']:
                            Settings().secret_manager.get_store(key).delete_secret(val)
                    return jsonify({'state': 'success'}), 200
            except Exception as ex:
                logging.exception(str(ex))
                return jsonify({'state': 'error', 'msg': str(ex)}), 500

    def persist_settings(self):
        if request.is_json:
            data = request.get_json()
            try:
                content = data['content']
                scope = data['scope']
                Settings().persist_settings(content, scope)

                return jsonify({'state': 'success'}), 200

            except Exception as ex:
                logging.exception(str(ex))
                return jsonify({'state': 'error', 'msg': str(ex)}), 500

    def add_secret(self):
        if request.is_json:
            data = request.get_json()
            try:
                if data['currentUser']:
                    Settings().secret_manager.get_store('User_Local_Store').set_secret(data['secretName'], data['secretValue'])
                else:
                    Settings().secret_manager.get_store('App_Local_Store').set_secret(data['secretName'], data['secretValue'])
                return jsonify({'state': 'success'}), 200
            except Exception as ex:
                logging.exception(str(ex))
                return jsonify({'state': 'error', 'msg': str(ex)}), 500

    def app_path_caller(self, guid, path):
        guid = guid.replace('/', '')
        return self.tool_manager.app_path_caller(guid, path, request)

    def app_about_caller(self, guid):
        guid = guid.replace('/', '')
        return jsonify(self.tool_manager.app_about_caller(guid, request)), 200

    def app_static(self, guid, path):
        guid = guid.replace('/', '')
        return self.tool_manager.app_static(guid, path, request)

    def app_close(self, guid):
        guid = guid.replace('/', '')
        return self.tool_manager.app_close(guid, request)

    def app_home(self, guid):
        guid = guid.replace('/', '')
        return self.tool_manager.app_home(guid, request)

    def open_app(self):
        if request.is_json:
            data = request.get_json()
            guid = self.tool_manager.open_tool(data['app'], self.content_manager)
            return jsonify({'redirect_path': f'/app-instance/{guid}/'}), 200

    def download_logs(self):
        path = ApplicationPaths().logging_root_path
        dirs = [(d, os.path.getctime(os.path.join(path, d))) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        if not dirs:
            return None
        latest_dir = max(dirs, key=lambda x: x[1])
        log_directory = path + '/' + latest_dir[0]
        logging.info(f'Zipping Log Directory: {log_directory}')
        dest = ApplicationPaths().tmp_root_path + '/logs_' + latest_dir[0]

        shutil.make_archive(dest, 'zip', log_directory)
        return send_file(dest + '.zip', as_attachment=True)

    def close_app(self):
        self.tool_manager.close()
        time.sleep(2)
        logging.info("Closing app at user's request")
        os._exit(0)

    def exit(self):
        thread = Thread(target=self.close_app)
        thread.start()

        self.base_app.closed = True
        return self.content_manager.exit()

    def about(self):
        return jsonify(self.content_manager.about()), 200

    def settings_content(self):
        settings = {'secrets': self.settings.secret_manager.get_local_stores_index(),
                    'settings': self.settings.get_raw_settings()}
        return jsonify(settings), 200


def start(base_app):
    WebApp(base_app).run()
