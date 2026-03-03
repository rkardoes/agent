import os

def write_file(working_directory, file_path, content):

    try:

        abs_dir_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_dir_path, file_path))

        valid_target_path = os.path.commonpath([abs_dir_path, target_path]) ==  abs_dir_path

        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parents = os.path.dirname(target_path)
        os.makedirs(parents, exist_ok=True)

        with open(target_path, "w") as f:
                f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: exception \"{e}\" was raised"