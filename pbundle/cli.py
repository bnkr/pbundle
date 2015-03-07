from __future__ import print_function
import argparse, sys, subprocess, os, re
try:
    import StringIO as stringio
except ImportError:
    import stringio
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

class PbundleCli(object):
    def __init__(self):
        self.cli = None
        self.config = None

    def load_settings(self, argv):
        """Read configuration."""
        parsers = self.get_argument_parser()
        self.config = self.get_config_parser()

        parsed = parsers[0].parse_args(argv[1:])
        parsed.parsers = parsers
        self.cli = parsed

        self.config.read(["requirements.cfg"])

    def run(self):
        """Run using stored settings."""
        if self.cli.command == "help":
            self.cli.parsers[0].print_usage()
            print()
            for subcommand in self.cli.parsers[1]:
                print("*", subcommand.format_help().replace("\n", "\n  "))
            return 0

        return 0

    def get_argument_parser(self):
        """Ceate command-line argument parser."""
        parser = argparse.ArgumentParser()

        commands = parser.add_subparsers(dest="command")

        create = commands.add_parser('create', help="Start a virtualenv.")
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
