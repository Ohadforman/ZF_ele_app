
import subprocess
import sys

def run_skidl_script(script_path):
    try:
        # Run the SKiDL script. This requires the SKiDL package to be installed and properly set up.
        # subprocess.run() is used here to execute the script as if it was run from the command line.
        # Ensure that the Python environment has SKiDL installed and configured.
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        # If the script runs successfully, the following line will be executed
        print("PCB generated successfully.")
    except subprocess.CalledProcessError as e:
        # If there's an error during the execution, print the error message
        print("Error occurred while running the SKiDL script:", e.stderr)

if __name__ == "__main__":
    # Example: python this_script.py your_skidl_script.py
    if len(sys.argv) < 2:
        print("Usage: python this_script.py path_to_skidl_script.py")
    else:
        script_path = sys.argv[1]
        run_skidl_script(script_path)
