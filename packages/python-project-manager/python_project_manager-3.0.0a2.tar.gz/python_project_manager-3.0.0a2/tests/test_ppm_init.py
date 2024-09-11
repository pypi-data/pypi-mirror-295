import unittest
from click.testing import CliRunner
from python_project_manager.config import Config
from python_project_manager.ppm_commands.ppm_init import init
from tests.helper import shash, working_directory

class TestPpmInit(unittest.TestCase):
    @working_directory(cwd='tests/__cached__')
    def test_ppm_init(self):
        Config.load()
        runner = CliRunner()
        result = runner.invoke(init, ['test_project'], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0, result.output)
        self.assertEqual(result.output, 'Project test_project created\n')

        # Check the '.proj.config' file not using the Config class
        with open('.proj.config', 'r') as config_file:
            config = config_file.read()
            self.assertEqual(shash(config), 3200114494, config)

    @working_directory(cwd='tests/__cached__')
    def test_ppm_init_reinit(self):
        Config.load()
        runner = CliRunner()
        result = runner.invoke(init, ['test_project'], catch_exceptions=False)
        self.assertEqual(result.output, 'Project test_project created\n')
        with open('.proj.config', 'r') as config_file:
            config = config_file.read()
            self.assertEqual(shash(config), 3200114494, config)

        # Reinitialize the project, should not overwrite the '.proj.config' file
        result = runner.invoke(init, ['test_project_override'], catch_exceptions=False)
        self.assertEqual(result.output, 'Project already initialized\n')
        with open('.proj.config', 'r') as config_file:
            config = config_file.read()
            self.assertEqual(shash(config), 3200114494, config)

        # Reinitialize the project by force, should overwrite the '.proj.config' file
        result = runner.invoke(init, ['test_project_override', '--force'], catch_exceptions=False)
        self.assertEqual(result.output, 'Project test_project_override created\n')
        with open('.proj.config', 'r') as config_file:
            config = config_file.read()
            self.assertEqual(shash(config), 1435409181, config)