import os
import shutil
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_venv import venv
from python_project_manager.venv import _VENV_SITE_PACKAGES, _VENV_PATH
from tests.helper import mock_run_command, shash, working_directory

class TestPpmVenv(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_venv(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_venv.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])
            with open('requirements.txt', 'w') as file:
                file.write('build~=1.2.1\n')
            with open('requirements-dev.txt', 'w') as file:
                file.write('certifi~=2024.2.2\n')
            shutil.rmtree(_VENV_PATH, ignore_errors=True)
            
            runner.invoke(venv, catch_exceptions=False, input='y\n') # colorama~=0.4.6
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            self.assertEqual(shash(packages), 3605667815, msg=packages)