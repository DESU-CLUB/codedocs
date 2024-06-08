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

    # Generate the activation script to activate the virtual environment
    activate_script = pathlib.Path.cwd().joinpath('activate_and_run.sh')
    with open(activate_script, 'w') as f:
        f.write(f"#!/bin/bash\n")
        f.write(f"source {venv_path.joinpath('bin', 'activate')}\n")
        f.write(f"echo 'Virtual environment activated.'\n")
        f.write(f"pip freeze\n")  # Add any additional commands here
        f.write(f"echo 'Additional commands executed.'\n")

    # Make the generated script executable
    subprocess.run(['chmod', '+x', str(activate_script)])

if __name__ == '__main__':
    _main()
