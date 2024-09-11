import unittest
from unittest.mock import patch
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_list import list
from tests.helper import mock_run_command, shash, working_directory

class TestPpmList(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_list(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_list.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(list, catch_exceptions=False)
            self.assertEqual(shash(captured_output), 4181304811, msg=''.join(captured_output))

class TestPpmList(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_list_help(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_list.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            runner.invoke(list, ['--help'], catch_exceptions=False)
            self.assertEqual(shash(captured_output), 1546755243, msg=''.join(captured_output))
    

