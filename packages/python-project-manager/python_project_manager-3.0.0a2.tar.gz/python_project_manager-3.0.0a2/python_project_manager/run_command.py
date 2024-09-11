import subprocess
from python_project_manager.venv import activate_venv, deactivate_venv

def run_command(command: str, use_venv: bool, *, return_output: bool = False) -> None:
    '''
    Runs a command in the shell.

    Args:
        command (str): The command to run.
        cwd (str): The current working directory to run the command in.
        use_venv (bool): If True, the command will be run in the virtual environment.
    '''

    if use_venv:
        command = [activate_venv(), command]
    else:
        command = [deactivate_venv(), command]
    
    command = [c for c in command if c] # Remove any empty strings from the
    command = ' && '.join(command)

    with subprocess.Popen(command,
        shell=True,
        stdout=subprocess.PIPE if return_output else None,
        stderr=subprocess.PIPE) as process:
        stdout, stderr = process.communicate()
        if return_output:
            return stdout.decode(errors='replace')
        if process.returncode:
            print('') # Guarantes a seperation between the command output and the next line
            raise Exception(f"Command '{command}' failed with error code {process.returncode}.\n\n<<Command Traceback>>\n{stderr.decode(errors='replace')}")