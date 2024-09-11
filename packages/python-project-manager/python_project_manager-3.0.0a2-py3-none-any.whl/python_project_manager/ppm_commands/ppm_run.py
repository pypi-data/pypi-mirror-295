from python_project_manager import Config
import click
from python_project_manager.run_command import run_command

@click.command()
@click.argument('command_name', type=str)
@click.option('--local', '-l', is_flag=True, help='Run the script in the local environment not the virtual environment')
@click.option('--script', '-s', is_flag=True, help='Run as a python script or file')
def run(command_name, local, script) -> None:
    '''
    <command_name> - Name of the script to be run
    '''    
    cli_command: str = Config.get(f'scripts.{command_name}')

    if not cli_command:
        print(f"Script '{command_name}' not found")
        return

    if script: # Run as a python script
        is_python_file = cli_command.endswith('.py')
        if not is_python_file:
            py_script = cli_command
        else:
            with open(cli_command, 'r') as file:
                py_script = file.read()
        exec(py_script)
        return

    run_command(cli_command, not local)