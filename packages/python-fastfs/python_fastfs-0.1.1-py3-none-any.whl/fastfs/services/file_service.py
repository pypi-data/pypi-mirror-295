import os
import mimetypes
from fastapi.responses import FileResponse
from fastfs.utils.helpers import guess_type_from_content, get_file_info, format_size, format_date, search_files
from fastfs.views.renderers import render_preview, render_file_list
from fastfs.config import get_settings

settings = get_settings()

def handle_file(path: str, preview: bool = False):
    full_path = os.path.normpath(os.path.join(settings.base_dir, path))
    mime_type, _ = mimetypes.guess_type(full_path)
    
    if preview:
        return render_preview(full_path)
    else:
        return FileResponse(full_path, media_type=mime_type, filename=os.path.basename(full_path))

def handle_directory(path: str, search: str = ''):
    full_path = os.path.normpath(os.path.join(settings.base_dir, path))
    
    if search:
        tree = search_files(full_path, search)
    else:
        tree = build_tree(full_path)
    
    return render_file_list(tree, path)

def build_tree(path: str):
    tree = []
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        relative_path = os.path.relpath(item_path, settings.base_dir)
        if os.path.isdir(item_path):
            tree.append(('folder', item, relative_path))
        else:
            tree.append(('file', item, relative_path))
    return tree