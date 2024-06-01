import subprocess
import threading
import time

def run_python(script_path):
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"Executed {script_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {script_path}: {e}")

def run_executable(executable_path):
    try:
        subprocess.run([executable_path], check=True)
        print(f"Executed {executable_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute {executable_path}: {e}")

if __name__ == "__main__":
    gridGeneration = 'py/grid.py'
    reactionDiffusion = 'bin/app'
    patternToMaze='py/patternToMaze.py'
    remap='py/remap.py'
