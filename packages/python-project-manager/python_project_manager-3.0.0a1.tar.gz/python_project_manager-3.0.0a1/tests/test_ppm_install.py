import os
import unittest
from unittest.mock import patch
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from python_project_manager.ppm_commands.ppm_install import install
from tests.helper import mock_run_command, shash, working_directory
from python_project_manager.venv import _VENV_SITE_PACKAGES

class TestPpmInstall(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_install(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_install.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])

            # Addlines to the requirements file
            with open('requirements.txt', 'w') as file:
                file.write('Pygments~=2.17.2\n')
                file.write('build~=1.2.1\n')
                file.write('certifi~=2024.2.2\n')

            runner.invoke(install, ['requests'], catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            requirement_file_string = ''
            with open('requirements.txt', 'r') as file:
                requirement_file_string = file.read()

            # Run tests
            self.assertEqual(shash(packages), 691631167, msg=packages)
            self.assertEqual(shash(requirement_file_string), 1280992123, msg=requirement_file_string)

    @working_directory(cwd='tests/__cached__')
    def test_ppm_install_dev(self):
        captured_output = []
        with patch('python_project_manager.ppm_commands.ppm_install.run_command', mock_run_command(captured_output)):
            Config.load()
            runner = CliRunner()
            runner.invoke(init, ['test_project'])

            # Addlines to the requirements file
            with open('requirements-dev.txt', 'w') as file:
                file.write('Pygments~=2.17.2\n')
                file.write('build~=1.2.1\n')
                file.write('certifi~=2024.2.2\n')

            runner.invoke(install, ['requests', '--dev'], catch_exceptions=False)
            
            # Get all folders in packages
            packages = [f for f in os.listdir(_VENV_SITE_PACKAGES) if os.path.isdir(os.path.join(_VENV_SITE_PACKAGES, f))]
            requirement_file_string = ''
            with open('requirements-dev.txt', 'r') as file:
                requirement_file_string = file.read()

            # Run tests
            self.assertEqual(shash(packages), 691631167, msg=packages)
            self.assertEqual(shash(requirement_file_string), 1280992123, msg=requirement_file_string)
