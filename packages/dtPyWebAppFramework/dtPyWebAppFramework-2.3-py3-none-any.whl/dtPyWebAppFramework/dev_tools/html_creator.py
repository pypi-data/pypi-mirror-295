from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.settings import Settings

from ..base_tool import AbstractTool
import os
from flask import jsonify, Response, Request


class Tool(AbstractTool):

    def __init__(self, flask_wrapper, resource_manager: ResourceManager, app_name, settings: Settings, content_manager: 'ContentManager', tool_instance_guid):
        super().__init__(flask_wrapper, resource_manager, app_name, settings, content_manager, tool_instance_guid)
        self.code = ''
        self.new_code = False

    @staticmethod
    def is_enabled():
        return True

    def add_custom_endpoints(self):
        self.resource_manager.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"))

    @staticmethod
    def name():
        return "HTML Creator"

    @staticmethod
    def short_name():
        return "html_creator"

    @staticmethod
    def description():
        return "Provides a way to build up HTML content for use in APPS using the styles and layout within the framework."

    @staticmethod
    def icon():
        return 'alarm'

    def tool_home_body_content(self):
        with open(self.resource_manager.get_resource_path('html_creator.html'), mode='r') as body:
            return body.read()

    def close_app(self):
        pass

    @staticmethod
    def version():
        return "1.0"

    @staticmethod
    def disabled_reason():
        return "Provides a way to build up HTML content for use in APPS using the styles and layout within the framework."

    def _update_code(self, new_code):
        with open(self.resource_manager.get_resource_path('poll_script.js'), mode='r') as poll:
            self.code = new_code + '<script>' + poll.read() + '</script>'
            self.new_code = True

    def app_path_caller(self, path: str, request: Request, method: str):
        if path == 'preview':
            self._update_code(request.json['code'])
            return jsonify({'url': 'preview_code', 'success': True}), 200
        if path == 'preview_code':
            if self.new_code:
                self.new_code = False
            return Response(self._format_response_content(self.code, ignore_close=True), 200)
        if path == 'check-for-update':
            if self.new_code:
                return jsonify({'url': 'preview_code', 'redirect': True}), 200
            else:
                return jsonify({'url': 'preview_code', 'redirect': False}), 200
