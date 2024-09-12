import os

from lced_utils.buffer_utils import get_project_bind


def find_handler_folders_and_files(handler_files, directory, folder_pattern):
    """
    递归查找指定目录及其子目录中所有名为`folder_pattern`的文件夹，
    并在这些文件夹中查找所有`.folder_pattern`后缀的文件。
    """
    for obj in os.listdir(directory):
        add_directory = os.path.join(directory, obj)
        if os.path.isdir(add_directory):
            find_handler_folders_and_files(
                handler_files, add_directory, ".".join([folder_pattern, obj])
            )
        elif os.path.isfile(add_directory) and obj.lower().endswith(
            f"{folder_pattern.split('.')[0]}.py"
        ):
            handler_files.append(f"{folder_pattern}.{obj.replace('.py', '')}")
            __import__(f"{folder_pattern}.{obj.replace('.py', '')}")


def process_handler_files():
    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    work_folder = get_project_bind()["work_folder"]
    directory = os.path.join(project_root_path, work_folder)
    handler_files = []
    find_handler_folders_and_files(handler_files, directory, work_folder)
    return handler_files
