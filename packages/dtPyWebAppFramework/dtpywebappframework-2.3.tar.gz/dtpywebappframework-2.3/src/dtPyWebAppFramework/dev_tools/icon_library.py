from ..base_tool import AbstractTool
import os
from flask import Request


class Tool(AbstractTool):

    @staticmethod
    def is_enabled():
        return True

    def add_custom_endpoints(self):
        self.resource_manager.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_resources"))

    @staticmethod
    def name():
        return "Icons Library"

    @staticmethod
    def short_name():
        return "icon_library"

    @staticmethod
    def description():
        return "Shows the icons which can be used to represent apps you host via this framework."

    @staticmethod
    def icon():
        return 'image'

    def tool_home_body_content(self):
        with open(self.resource_manager.get_resource_path('icon_library.html'), mode='r') as body:
            return body.read()

    def close_app(self):
        pass

    @staticmethod
    def version():
        return "1.0"

    @staticmethod
    def disabled_reason():
        return ""

    def app_path_caller(self, path: str, request: Request, method: str):
        raise NotImplementedError
