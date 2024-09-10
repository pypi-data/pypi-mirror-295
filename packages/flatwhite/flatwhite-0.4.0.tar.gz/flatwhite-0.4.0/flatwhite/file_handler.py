import os
import shutil

# Define file extensions for each category
file_extensions = {
    'pics': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.ico', '.webp', '.heic', '.raw', '.nef', '.cr2', '.orf', '.arw', '.dng'],
    'sounds': ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma', '.mid', '.opus', '.ra'],
    'docs': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.odt', '.csv', '.epub', '.mobi', '.log']
}

def handle_files(directory, action='organize', types=None, additional_ext=None):
    """
    Organizes or deletes files in the directory based on their file type.

    Parameters:
    directory (str): Path of the directory to process.
    action (str): Action to perform ('organize' or 'delete').
    types (list): List of file types to organize or delete ('pics', 'sounds', 'docs').
    additional_ext (str): Additional file extensions to consider, comma-separated.
    """
    if not os.path.exists(directory):
        print(f'{directory} does not exist!')
        return

    if types is None:
        types = []

    additional_ext = [ext.strip() for ext in (additional_ext or '').split(',') if ext.strip()]
    extensions_to_handle = sum([file_extensions.get(t, []) for t in types], []) + additional_ext

    if not extensions_to_handle:
        print('No criteria provided!')
        return

    for file in os.listdir(directory):
        ext = os.path.splitext(file)[1].lower()
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            continue

        if ext in extensions_to_handle:
            if action == 'organize':
                sub_dir = os.path.join(directory, types[0].capitalize())
                os.makedirs(sub_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(sub_dir, file))
            elif action == 'delete':
                os.remove(file_path)
                print(f'Deleted: {file_path}')

def list_directory_structure(root_dir, indent_level=0):
    """
    Recursively lists the directory structure starting from the root directory.

    Parameters:
    root_dir (str): Path of the root directory to start listing from.
    indent_level (int): Current indentation level for pretty printing.
    """
    try:
        for item in os.listdir(root_dir):
            item_path = os.path.join(root_dir, item)
            print(' ' * indent_level + '|-- ' + item)
            if os.path.isdir(item_path):
                list_directory_structure(item_path, indent_level + 4)
    except PermissionError:
        pass
