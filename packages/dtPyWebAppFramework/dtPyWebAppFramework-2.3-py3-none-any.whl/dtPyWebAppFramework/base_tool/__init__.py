import os.path

from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.settings import Settings
from flask import Response, send_from_directory, Request
from jinja2 import Template

import logging

from typing import TYPE_CHECKING
from abc import abstractmethod

if TYPE_CHECKING:
    from ..managers.content_manager import ContentManager


class BaseApp:

    def __init__(self):
        self._closed = False

    @abstractmethod
    def resources(self) -> str:
        pass

    @abstractmethod
    def short_name(self) -> str:
        pass

    @abstractmethod
    def full_name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def version(self) -> str:
        pass

    @abstractmethod
    def tool_modules(self) -> list:
        pass

    @abstractmethod
    def copyright(self) -> list:
        pass

    @property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = value

    def as_dict(self) -> dict:
        return {
            "banner_background_color": self.banner_background_color(),
            "logo": self.logo(),
            "banner_font_color": self.banner_font_color(),
            "copyright": self.copyright(),
            "version": self.version(),
            "description": self.description(),
            "full_name": self.full_name(),
            "short_name": self.short_name(),
            "closed": self.closed
        }

    def banner_background_color(self) -> str:
        return '#060d39'

    def logo(self) -> str:
        return '/assets/images/dt-logo.png'

    def banner_font_color(self) -> str:
        return '#ffffff'


class AbstractTool(object):

    def __init__(self, flask_wrapper, resource_manager: ResourceManager, app_name, settings: Settings, content_manager: 'ContentManager',
                 tool_instance_guid):
        super().__init__()
        self.app_name = app_name
        self.flask_wrapper = flask_wrapper
        self.settings: Settings = settings
        self.tool_instance_guid = tool_instance_guid
        self.content_manager: 'ContentManager' = content_manager
        self.resource_manager: ResourceManager = resource_manager
        self.add_custom_endpoints()

    @staticmethod
    @abstractmethod
    def is_enabled():
        pass

    @abstractmethod
    def add_custom_endpoints(self):
        pass

    @staticmethod
    @abstractmethod
    def name():
        pass

    @staticmethod
    @abstractmethod
    def version():
        pass

    @staticmethod
    @abstractmethod
    def short_name():
        pass

    @staticmethod
    @abstractmethod
    def description():
        pass

    @staticmethod
    @abstractmethod
    def icon():
        pass

    @abstractmethod
    def tool_home_body_content(self):
        pass

    @staticmethod
    @abstractmethod
    def disabled_reason():
        pass

    def tool_static_content(self, path):
        resource = self.resource_manager.get_resource_path(f'{self.short_name()}/{path}')
        if resource is None:
            resource = self.resource_manager.get_resource_path(f'{path}')

        if resource is None:
            raise Exception(f'The request for content at path {path} could not be processed as content not found.')

        logging.info(f"Rendering: {resource}")
        return send_from_directory(resource.replace(path, ''), path)

    @abstractmethod
    def app_path_caller(self, path: str, request: Request, method: str):
        pass

    @abstractmethod
    def close_app(self):
        pass

    def about(self):
        base_tabs = self.content_manager.about()
        for t in base_tabs:
            t['selected'] = False
        base_tabs.insert(0, {'name': self.name(), 'description': self.description(), 'version': self.version(),
                             'logo': self.icon(), 'tab_title': self.name(), 'tab_id': 'tool', 'selected': True})
        return base_tabs

    def close(self):
        logging.info('closing this app')
        self.close_app()
        return Response("", 200)

    def as_dict(self):
        return {
            "is_enabled": self.is_enabled(), "tool_name": self.name(), "tool_short_name": self.short_name(),
            "tool_description": self.description(), "icon": self.icon(), "disabled_reason": self.disabled_reason()
        }

    def _format_response_content(self, content: str, **kwargs):
        template = Template(content)
        data = self.as_dict()
        for index, (key, value) in enumerate(kwargs.items()):
            data[key] = value

        rendered_template = template.render(data)
        with open(ResourceManager().get_resource_path('app.html'), 'r') as base_app:
            template = Template(base_app.read())
            data['app_content'] = rendered_template
            rendered_template = template.render(data)

        return self.content_manager.base_template(rendered_template, data)

    def tool_home(self):
        return Response(self._format_response_content(self.tool_home_body_content()), 200)

    def tool_disabled(self):
        return Response(self._format_response_content(self.content_manager.tool_disabled()), 404)

    def error_message(self, friendly, detail):
        return Response(self._format_response_content(self.content_manager.error_card(), friendly=friendly, detail=detail), 500)

    def please_wait(self, task_id, message):
        return Response(self._format_response_content(self.content_manager.please_wait_template(), task_id=task_id, message=message), 200)
