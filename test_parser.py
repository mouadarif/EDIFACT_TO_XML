import subprocess
import sys
import os
from pathlib import Path
import argparse # Import argparse

def run_command(command, env_vars):
    print(f"Executing: {' '.join(command)}")
    script_dir = Path(__file__).parent
    print(f"Subprocess CWD will be: {script_dir.resolve()}")

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=False, cwd=script_dir, env=env_vars, timeout=60)
        print("STDOUT:")
        print(process.stdout)
        if process.stderr:
            print("STDERR:")
            print(process.stderr)
        if process.returncode != 0:
            print(f"Command failed with return code {process.returncode}")
        else:
            print(f"Command completed successfully with return code {process.returncode}")
        return process.stdout, process.stderr, process.returncode
    except subprocess.TimeoutExpired:
        print("STDERR: Command timed out after 60 seconds.")
        return "", "TimeoutExpired", -1
    except Exception as e:
        print(f"STDERR: Subprocess execution failed with exception: {e}")
        return "", str(e), -1

def main():
    parser = argparse.ArgumentParser(description="Test EDIFACT parser CLI.")
    parser.add_argument("input_edi", help="Path to the input EDI file.")
    parser.add_argument("output_xml", help="Path for the output XML file.")
    args = parser.parse_args()

    edi_file_path = Path(args.input_edi)
    xml_output_path = Path(args.output_xml)

    print(f"--- Test Environment (test_parser.py) ---")
    print(f"Python Executable (for test_parser.py): {sys.executable}")
    print(f"CWD (for test_parser.py): {Path().resolve()}")
    print(f"Input EDI file: {edi_file_path.resolve()}")
    print(f"Output XML file: {xml_output_path.resolve()}")

    if not edi_file_path.exists():
        print(f"CRITICAL ERROR: Input EDI file '{edi_file_path}' not found.")
        return

    # Prepare environment for subprocess - this was the successful configuration
    sub_env = os.environ.copy()
    sub_env["PYTHONPATH"] = "/"
    print(f"Subprocess PYTHONPATH set to: {sub_env['PYTHONPATH']}")

    # This refers to the project root directory as 'app' when PYTHONPATH is '/'
    module_name_for_cli = "app.cli"

    print(f"\n--- Testing Conversion: python -m {module_name_for_cli} {edi_file_path} {xml_output_path} ---")
    convert_command = [
        sys.executable, "-m", module_name_for_cli,
        str(edi_file_path),
        str(xml_output_path),
        "--format", "xml",
        "--log-level", "DEBUG"
    ]
    run_command(convert_command, sub_env)

    print(f"\n--- Checking for XML Output File: {xml_output_path} ---")
    if xml_output_path.exists():
        print(f"SUCCESS: XML output file '{xml_output_path}' was created.")
        print(f"Size: {xml_output_path.stat().st_size} bytes.")
        # Optional: print first few lines of XML for quick check
        # with open(xml_output_path, 'r') as f:
        #     print(f.read(500) + "...")
    else:
        print(f"ERROR: XML output file '{xml_output_path}' was NOT created.")

if __name__ == "__main__":
    main()
