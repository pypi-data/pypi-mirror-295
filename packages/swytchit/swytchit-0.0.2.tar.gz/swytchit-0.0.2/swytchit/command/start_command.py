
from argparse import ArgumentParser
from pathlib import Path
import sys
from swytchit.command import SwytchitCommand

import wizlib


class SwitchCommand(SwytchitCommand):
    name = 'start'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('directory')

    def handle_vals(self):
        super().handle_vals()
        if not wizlib.io.isatty():
            raise Exception('Swytchit only works in interactive tty')
        dirpath = Path(self.directory).resolve()
        if not (dirpath.is_dir()):
            raise Exception(
                'CBE requires an existing directory as an argument')
        if not (dirpath.is_relative_to(Path.home())):
            raise Exception('CBE only operates within user home directory')

    @SwytchitCommand.wrap
    def execute(self):
        pass
