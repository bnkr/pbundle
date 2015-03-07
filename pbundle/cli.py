from __future__ import print_function
import argparse, sys
try:
    import StringIO as stringio
except ImportError:
    import stringio
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from pbundle.installer import VirtualEnvironment, PipInstaller

class PbundleCli(object):
    class CommandError(Exception):
        pass

    def __init__(self):
        self.cli = None
        self.config = None

    def load_settings(self, argv):
        """Read configuration."""
        parsers = self.get_argument_parser()
        self.config = self.get_config_parser()

        self.cli = parsers[0].parse_args(argv[1:])
        self.cli.parsers = parsers

        self.config.read(["requirements.cfg"])

    def run(self):
        """Run using stored settings."""
        command = getattr(self, "_run_" + self.cli.command, None)
        if not command:
            raise Exception("unpossible")
        try:
            return command() or 0
        except self.CommandError as _:
            return 1

    def _run_help(self):
        self.cli.parsers[0].print_usage()
        print()
        for subcommand in self.cli.parsers[1]:
            print("*", subcommand.format_help().replace("\n", "\n  "))
        return 0

    def _run_create(self):
        venv = VirtualEnvironment(path=self.config.get('virtualenv', 'vendor-dir'));
        venv.create(python=self.config.get("virtualenv", "python"))

    def _run_update(self):
        self._run_create()
        pip = self._make_pip()
        pip.satisfy("requirements.txt", upgrade=True)
        pip.freeze(output="requirements.lock")

    def _run_install(self):
        self._run_create()
        pip = self._make_pip()
        pip.satisfy("requirements.lock")

    def _run_verify(self):
        pip = self._make_pip()
        diffs = pip.find_differences("requirements.lock")

        for name in diffs['missing']:
            print("{0} is missing from environment".format(name))

        for name in diffs['extra']:
            print("{0} should not be in the environment".format(name))

        for name, lock, actual in diffs['inconsistent']:
            messqage = "{0} has a different version locked = {1}, actual = {2}"
            print(message.format(name, lock, actual))

        if any(diffs.values()):
            return 1
        else:
            return 0

    def _make_pip(self):
        return PipInstaller(environment=self.config.get('virtualenv', 'vendor-dir'))

    def get_argument_parser(self):
        """Ceate command-line argument parser."""
        parser = argparse.ArgumentParser()

        commands = parser.add_subparsers(dest="command")

        create = commands.add_parser('create', help="Start a virtualenv and update.")
        update = commands.add_parser('update', help="Update a virtualenv from requirements and freeze.")
        install = commands.add_parser('install', help="Set a virtualenv to the frozen state.")
        verify = commands.add_parser('verify', help="Check the virtualenv is the same as the lock file.")
        help = commands.add_parser('help', help="Show help for all commands.")

        # So we can print one massive help later on.
        subparsers = [create, update, install, verify, help]

        return parser, subparsers

    def get_config_parser(self):
        """Create configuration file parser with default set."""
        default = \
            "[virtualenv]\n" \
            "python = /usr/bin/python\n" \
            "vendor-dir = python_modules\n"

        config = configparser.SafeConfigParser()
        config.readfp(stringio.StringIO(default))

        return config

def main():
    """Main entry point."""
    cli = PbundleCli()
    cli.load_settings(sys.argv)
    sys.exit(cli.run())

if __name__ == "__main__":
    main()
