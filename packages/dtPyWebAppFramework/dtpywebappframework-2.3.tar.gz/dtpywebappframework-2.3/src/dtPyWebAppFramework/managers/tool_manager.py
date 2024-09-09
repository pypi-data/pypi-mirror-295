from dtPyAppFramework.decorators import singleton
from dtPyAppFramework.settings import Settings
from dtPyAppFramework.resources import ResourceManager
from ..base_tool import AbstractTool, BaseApp

import logging
import uuid
import traceback


@singleton()
class ToolManager:

    def __init__(self, resource_manager: ResourceManager, settings: Settings, base_app: BaseApp, flask_app, dev_mode=False):
        self.settings = settings
        self.resource_manager = resource_manager
        self.base_app: BaseApp = base_app
        self.tools: dict = {}
        self.cards: list = []
        self.flask_app = flask_app
        self.dev_mode = dev_mode
        self.open_tools = {}

    def open_tool(self, tool_name, content_manager):
        tool_instance_guid = str(uuid.uuid4())
        tool: AbstractTool = self.tools[tool_name](self.flask_app, self.resource_manager,
                                                   f"{self.base_app.full_name()}, Version: {self.base_app.version()}",
                                                   self.settings, content_manager, tool_instance_guid)

        self.open_tools[tool_instance_guid] = tool
        return tool_instance_guid

    def app_path_caller(self, guid, path, request):
        try:
            tool = self.open_tools[guid]
            obj = tool.app_path_caller(path, request, request.method)
            if obj is None:
                obj = tool.tool_static_content(path)
                if obj is None:
                    raise Exception(f'No Valid Content was returned from request "{path}" for App Instance "{guid}".')

            return obj
        except Exception as ex:
            logging.exception(str(ex))
            return self.error(ex, traceback.format_exc())

    def app_about_caller(self, guid, request):
        try:
            tool = self.open_tools[guid]
            return tool.about()
        except Exception as ex:
            logging.exception(str(ex))
            return self.error(ex, traceback.format_exc())

    def app_static(self, guid, path, request):
        try:
            tool = self.open_tools[guid]
            return tool.tool_static_content(path)
        except Exception as ex:
            logging.exception(str(ex))
            return self.error(ex, traceback.format_exc())

    def app_close(self, guid, request):
        try:
            tool = self.open_tools[guid]
            self.open_tools.pop(guid)
            return tool.close()
        except Exception as ex:
            logging.exception(str(ex))
            return self.error(ex, traceback.format_exc())

    @staticmethod
    def error(ex, stack_trace):
        from dtPyWebAppFramework.managers.content_manager import ContentManager
        return ContentManager().error_message(friendly=str(ex), detail=stack_trace)

    def app_home(self, guid, request):
        try:
            tool = self.open_tools[guid]
            handler = tool.tool_disabled
            if tool.is_enabled():
                handler = tool.tool_home

            return handler()
        except Exception as ex:
            logging.exception(str(ex))
            return self.error(ex, traceback.format_exc())

    def close(self):
        for key in self.open_tools:
            logging.info(f'Closing Open Tool: "{key}"')
            self.open_tools[key].close()

    def _read_in_tool(self, module):
        self.cards.append({'name': module.Tool.name(), 'description': module.Tool.description(),
                           'icon': module.Tool.icon(), 'short_name': module.Tool.short_name(), 'enabled': module.Tool.is_enabled(),
                           'disabled_reason': module.Tool.disabled_reason()})
        self.tools[module.Tool.short_name()] = module.Tool

    def load_tools(self, content_manager):
        logging.info('Loading Tools into Context')
        if self.dev_mode:
            logging.warning('Loading Development Tools')
            from ..dev_tools import icon_library, html_creator
            self._read_in_tool(html_creator)
            self._read_in_tool(icon_library)


        else:
            for tool_module in self.base_app.tool_modules():
                logging.info(f'Loading Tool: {tool_module}')
                try:
                    self._read_in_tool(tool_module)

                except Exception as ex:
                    logging.exception(f'Error loading Tool "{tool_module}". {str(ex)}')
