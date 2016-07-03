#!/usr/bin/env python

import os
import sys
import asyncio

if __name__ == "__main__":
    os.environ.setdefault("BUBLIK_SETTINGS_MODULE", "_base.settings")
    # import ipdb;ipdb.set_trace()
    from bublik.core.management import execute_from_command_line

    loop = asyncio.get_event_loop()
    execute_from_command_line(loop, sys.argv)
