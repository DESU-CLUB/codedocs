# https://stackoverflow.com/questions/60066755/how-to-start-and-run-a-virtualenv-in-python-script/60072329#60072329
#!/usr/bin/env python3

#!/usr/bin/env python3

import pathlib
import subprocess
import venv
import os

class _EnvBuilder(venv.EnvBuilder):

    def __init__(self, *args, **kwargs):
        self.context = None
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        self.context = context

def _venv_create(venv_path):
    venv_builder = _EnvBuilder(with_pip=True)
    venv_builder.create(venv_path)
    return venv_builder.context

def _run_python_in_venv(venv_context, command):
    command = [venv_context.env_exe] + command
    print(command)
    return subprocess.check_call(command)

def _run_bin_in_venv(venv_context, command):
    command[0] = str(pathlib.Path(venv_context.bin_path).joinpath(command[0]))
    print(command)
    return subprocess.check_call(command)

def _main():
    venv_path = pathlib.Path.cwd().joinpath('virt')
    venv_context = _venv_create(venv_path)
    _run_python_in_venv(venv_context, ['-m', 'pip', 'install', '-U', 'pip'])
    _run_bin_in_venv(venv_context, ['pip', 'install', 'attrs'])

if __name__ == '__main__':
    _main()
    
    # Activate the virtual environment in a new shell session
    activate_script = pathlib.Path.cwd().joinpath('virt', 'bin', 'activate')
    if os.name == 'nt':  # Windows
        activate_script = pathlib.Path.cwd().joinpath('virt', 'Scripts', 'activate.bat')
    
    print(f"\nTo activate the virtual environment, run:\nsource {activate_script}")

    # For Windows
    if os.name == 'nt':
        print(f"On Windows, run:\n{activate_script}")

    # Print out the packages in this environment
    subprocess.run(['virt/bin/pip', 'freeze'])

    # Print out the environment I am in
    subprocess.run(['which', 'python'])
