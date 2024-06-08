import subprocess
import os
import sys

def create_venv_and_run_code(venv_path, requirements_file, code_to_run):
    # Create a virtual environment
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    print("Virtual environment created at", venv_path)

    # Platform-specific virtual environment activation and package installation
    if os.name == "nt":  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate")
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:  # Unix/Linux
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")

    # Install packages from requirements.txt
    if requirements_file:
        subprocess.run([pip_path, "install", "-r", requirements_file], check=True)
        print("Required packages installed from", requirements_file)

    # Run the provided code snippet
    try:
        # Run the Python code snippet in the virtual environment
        output = subprocess.run([pip_path[:-4] + "/python", "-c", code_to_run], check=True, capture_output=True, text=True)
        print("Code ran successfully:", output.stdout)
        return True, None
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)
        return False, e.stderr
