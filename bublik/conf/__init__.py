import os
import importlib

from bublik.conf import global_settings

__author__ = 'vadim'

ENVIRONMENT_VARIABLE = 'BUBLIK_SETTINGS_MODULE'


class BaseSettings:
    settings_attrs = ['settings']

    def __init__(self):
        self.settings = {}

    def __getattr__(self, item):
        try:
            value = self.settings[item]
        except KeyError:
            raise AttributeError('Setting module {module} has not attribute {attr}'.format(
                module=self.module, attr=item
            ))

        return value

    def __setattr__(self, key, value):
        if key in self.settings_attrs:
            super(BaseSettings, self).__setattr__(key, value)
        else:
            self.settings[key] = value

    def update(self, kwargs):
        self.settings.update(kwargs)


class Settings(BaseSettings):
    settings_attrs = ['module', 'settings']

    def __init__(self):
        super(Settings, self).__init__()
        self.module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not self.module:
            raise EnvironmentError('SETTINGS_MODULE not found!')

        settings_module = importlib.import_module(self.module)
        self.settings.update({
            **{name: getattr(settings_module, name) for name in dir(global_settings) if name.upper()}
            **{name: getattr(settings_module, name) for name in dir(settings_module) if name.upper()}
        })


class AppSettings(BaseSettings):
    def __init__(self, label):
        self.label = label
        super(AppSettings, self).__init__()
        upper_label = label.upper()
        self.settings.update({key: value for key, value in os.environ.items() if key.startswith(upper_label)})
        self.settings.update({key: value for key, value in os.environ.items() if key.startswith(upper_label)})


settings = Settings()
