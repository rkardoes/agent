import os
import subprocess

def run_python_file(working_directory, file_path, args=None):

    try:

        abs_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_dir_path, file_path))

        valid_target_path = os.path.commonpath([abs_dir_path, target_path]) ==  abs_dir_path

        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if target_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, timeout=30, text=True)
        return_code = process.returncode
        stdout = process.stdout
        stderr = process.stderr

        output = []

        if return_code != 0:
            output.append(f"Process exited with code {return_code}")
        else:
            output.append(f"Process completed successfully")

        if not stdout and not stderr:
            output.append(f"No output produced")
        else:
            output.extend([f"STDOUT: {stdout}", f"STDERR: {stderr}"])

        output_str = "\n".join(output)
        return output_str 

    except Exception as e:
        return f"Error: executing Python file: {e}"