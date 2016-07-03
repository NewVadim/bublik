import importlib

from collections import OrderedDict

from bublik.conf import settings


class AppsSettings:
    def __init__(self):
        self.apps = OrderedDict()
        for app in settings.INSTALED_APPS:
            app_label = app.split('.')[-1]
            cls_name = '{app_label}Settings'.format(
                app_label=''.join(map(lambda x: x.capitalize(), app_label.split('_'))))

            settings_module = importlib.import_module('{}.conf'.format(app))
            self.apps[app] = getattr(settings_module, cls_name)(label=app_label)

apps_settings = AppsSettings()
