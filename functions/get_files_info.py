import os

def get_files_info(working_directory, directory="."):
    
    try:
        abs_dir_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_dir_path, directory))
        # print(f"abs_dir_path = {abs_dir_path}")
        # print(f"target_dir = {target_dir}")
        # print(f"commonpath = {os.path.commonpath([abs_dir_path, target_dir])}")
    # Will be True or False
        valid_target_dir = os.path.commonpath([abs_dir_path, target_dir]) ==  abs_dir_path
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            f'Error: "{directory}" is not a directory'
        dir_items = []
        for item in os.listdir(target_dir):
            # print(item)
            item_name = item
            item_size = os.path.getsize(f"{target_dir}/{item}")
            is_dir = os.path.isdir(f"{target_dir}/{item}")
            dir_items.append(f"- {item_name}: file_size={item_size} bytes, is_dir={is_dir}")
        return "\n".join(dir_items)
    except Exception as e:
        return f"Error: exception \"{e}\" was raised"