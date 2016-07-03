import argparse
import logging.config

from bublik.conf import settings


class BaseCommand:
    arguments = (
        {
            'flags': ('--host',),
            'action': 'store',
            'help': 'Host for runserver',
            'type': str,
        },
    )

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Bublik arguments')
        for arg in self.arguments:
            flags = arg.pop('flags')
            self.parser.add_argument(*flags, **arg)

    def execute(self, loop, argv):
        namespace = self.parser.parse_args(argv)
        return loop.run_until_complete(self.handle(loop, namespace))

    async def handle(self, loop, namespace):
        """
        The actual logic of the command. Subclasses must implement
        this method.

        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
