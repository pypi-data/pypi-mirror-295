import unittest
from unittest.mock import patch
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_run import run
from tests.helper import mock_run_command, shash, working_directory

class TestPpmRun(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_run(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_run.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(run, ['start'], catch_exceptions=False)
            self.assertEqual(shash(captured_output), 4095795366, msg=''.join(captured_output))