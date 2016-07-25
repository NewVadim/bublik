import argparse
import logging.config
import os
import pkgutil
import sys
from importlib import import_module

from bublik.core.management.commands.base import BaseCommand


class ManagementUtility(object):
    """
    Encapsulates the logic of the django-admin and manage.py utilities.

    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    """
    def __init__(self, loop, argv):
        self.loop = loop
        self.command = argv[1] if len(argv) > 1 else None
        self.argv = argv[2:]
        self.parser = argparse.ArgumentParser(description='Bublik arguments')
        # self.parser.add_argument()  # help

    def execute(self):
        commands = self.get_commands()
        try:
            app_name = commands[self.command]
        except KeyError:
            sys.stderr.write("Unknown command: {}\n".format(self.command))
            sys.exit(1)

        command = self.load_command_class(app_name)
        command.execute(self.loop, self.argv)

    def get_commands(self):
        """
        Returns a dictionary mapping command names to their callback applications.

        This works by looking for a management.commands package in django.core, and
        in each installed application -- if a commands package exists, all commands
        in that package are registered.

        Core commands are always included. If a settings module has been
        specified, user-defined commands will also be included.

        The dictionary is in the format {command_name: app_name}. Key-value
        pairs from this dictionary can then be used in calls to
        load_command_class(app_name, command_name)

        If a specific version of a command must be loaded (e.g., with the
        startapp command), the instantiated module can be placed in the
        dictionary in place of the application name.

        The dictionary is cached on the first call and reused on subsequent
        calls.
        """
        commands = {name: 'bublik.core' for name in self.find_commands(__path__[0])}

        # for app_config in reversed(list(apps.get_app_configs())):
        #     path = os.path.join(app_config.path, 'management')
        #     commands.update({name: app_config.name for name in self.find_commands(path)})

        return commands

    def find_commands(self, management_dir):
        command_dir = [os.path.join(management_dir, 'commands')]
        return [name for _, name, is_pkg in pkgutil.iter_modules(command_dir)
                if not is_pkg and not name.startswith('_')]

    def load_command_class(self, app_name):
        """
        Given a command name and an application name, returns the Command
        class instance. All errors raised by the import process
        (ImportError, AttributeError) are allowed to propagate.
        """
        module = import_module('%s.management.commands.%s' % (app_name, self.command))
        return module.Command()


def execute_from_command_line(loop, argv):
    """
    A simple method that runs a ManagementUtility.
    """
    from site_settings import settings, apps_settings

    utility = ManagementUtility(loop, argv)
    utility.execute()
