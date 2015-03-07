from unittest import TestCase
from pbundle.cli import PbundleCli

class CliTest(TestCase):
    def test_help_printed(self):
        cli = PbundleCli()
        cli.load_settings(["bin", "help"])
        self.assertEquals(0, cli.run())
