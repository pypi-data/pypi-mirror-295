from dtPyAppFramework.decorators import singleton
from dtPyAppFramework.resources import ResourceManager
from dtPyAppFramework.settings import Settings

from ..base_tool import BaseApp
from typing import TYPE_CHECKING
from flask import send_from_directory, Response
from jinja2 import Environment, FileSystemLoader, Template

import logging
import os

if TYPE_CHECKING:
    pass


@singleton()
class ContentManager:

    def __init__(self, resource_manager: ResourceManager, settings: Settings, base_app: 'BaseApp',
                 flask_app, tool_manager, html_template_dir, core_app):
        self.resource_manager = resource_manager
        self.settings = settings
        self.base_app: 'BaseApp' = base_app
        self.core_app = core_app
        self.flask_app = flask_app
        self.tool_manager = tool_manager
        self.jinja_env = Environment(loader=FileSystemLoader(html_template_dir))

    def base_template(self, content, additional_data=None):
        base_template = self.jinja_env.get_template('base.html')
        data = self.base_app.as_dict()
        data['content'] = content
        data['framework_copyright'] = self.core_app['copyright']

        if additional_data is not None:
            for key in additional_data:
                data[key] = additional_data[key]
        return base_template.render(data)

    def please_wait_template(self, request, message):
        data = {'request': request, 'message': message}
        with open(self.resource_manager.get_resource_path('please_wait_template.html'), mode='r') as base_template:
            template = Template(base_template.read())
            return template.render(data)

    def error_card(self):
        with open(self.resource_manager.get_resource_path('error_card.html'), mode='r') as base_template:
            return base_template.read()

    def _format_response_content(self, content: str, **kwargs):
        template = Template(content)
        data = {}
        for index, (key, value) in enumerate(kwargs.items()):
            data[key] = value

        rendered_template = template.render(data)
        return self.base_template(rendered_template, data)

    def error_message(self, friendly, detail):
        return Response(self._format_response_content(self.error_card(), friendly=friendly, detail=detail), 500)

    def tool_disabled(self):
        with open(self.resource_manager.get_resource_path('tool_disabled.html'), mode='r') as base_template:
            return base_template.read()

    def about(self):
        core = self.core_app
        core['tab_title'] = 'dtPyWebAppFramework'
        core['tab_id'] = 'tab_id'
        core['selected'] = False
        base_app = self.base_app.as_dict()
        base_app['tab_title'] = base_app['full_name']
        base_app['tab_id'] = 'base_app'
        base_app['selected'] = True
        return [base_app, core]

    def home(self):
        home_template = self.jinja_env.get_template('home.html')
        rendered_home_output = home_template.render({'cards': self.tool_manager.cards})
        return Response(self.base_template(rendered_home_output), 200)

    def assets(self, path):
        for resource_path in self.resource_manager.resource_paths:
            if os.path.exists(os.path.join(resource_path[0], "assets", path)):
                logging.debug(f"Rendering: {resource_path[0]}/assets/{path}")
                return send_from_directory(f'{resource_path[0]}/assets', path)

    def exit(self):
        logging.debug(f"Rendering: exit.html")
        exit_template = self.jinja_env.get_template('exit.html')
        rendered_exit_output = exit_template.render(self.base_app.as_dict())
        return Response(self.base_template(rendered_exit_output, {'closed': True}), 200)

