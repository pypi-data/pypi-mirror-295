import os
import mimetypes
import datetime
import fnmatch
from typing import List, Tuple

def guess_type_from_content(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type is None:
        try:
            # Check file extension first
            if file_path.lower().endswith(('.log', '.txt', '.csv', '.md')):
                return 'text/plain'
            # Add JSON detection
            if file_path.lower().endswith('.json'):
                return 'application/json'
            
            with open(file_path, 'rb') as f:
                file_head = f.read(256)  # Read first 256 bytes
            
            # Check if content is printable ASCII
            if all(32 <= byte <= 126 or byte in (9, 10, 13) for byte in file_head):
                return 'text/plain'
            
            # Check for common file signatures
            if file_head.startswith(b'\xFF\xD8\xFF'):
                mime_type = 'image/jpeg'
            elif file_head.startswith(b'\x89PNG\r\n\x1a\n'):
                mime_type = 'image/png'
            elif file_head.startswith(b'GIF87a') or file_head.startswith(b'GIF89a'):
                mime_type = 'image/gif'
            elif file_head.startswith(b'%PDF'):
                mime_type = 'application/pdf'
            elif file_head.startswith(b'PK\x03\x04'):
                mime_type = 'application/zip'
            # Add more file signatures as needed
            
            # If still unknown, use a generic binary type
            if mime_type is None:
                mime_type = 'application/octet-stream'
        
        except IOError:
            mime_type = 'application/octet-stream'
    
    return mime_type

def get_file_info(file_path: str) -> Tuple[int, datetime.datetime, str]:
    try:
        stats = os.stat(file_path)
        size = stats.st_size
        creation_time = datetime.datetime.fromtimestamp(stats.st_mtime)
        mime_type, _ = mimetypes.guess_type(file_path)
        file_type = mime_type.split('/')[-1].upper() if mime_type else os.path.splitext(file_path)[1][1:].upper() or "Unknown"
        return size, creation_time, file_type
    except OSError:
        return 0, datetime.datetime.now(), "Unknown"

def format_date(date: datetime.datetime) -> str:
    now = datetime.datetime.now()
    if date.date() == now.date():
        return f"Today, {date.strftime('%I:%M %p')}"
    elif date.year == now.year:
        return date.strftime("%d %b, %I:%M %p")
    else:
        return date.strftime("%d %b %Y, %I:%M %p")

def format_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

def search_files(base_path: str, search_term: str) -> List[Tuple[str, str, str]]:
    matches = []
    for root, dirnames, filenames in os.walk(base_path):
        for filename in fnmatch.filter(filenames, f'*{search_term}*'):
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, base_path)
            matches.append(('file', filename, relative_path))
        for dirname in fnmatch.filter(dirnames, f'*{search_term}*'):
            full_path = os.path.join(root, dirname)
            relative_path = os.path.relpath(full_path, base_path)
            matches.append(('folder', dirname, relative_path))
    return matches

def get_file_icon(item_type: str) -> str:
    return 'fa-folder' if item_type == 'folder' else 'fa-file'

def get_file_content(file_path):
    mime_type = guess_type_from_content(file_path)
    file_name = os.path.basename(file_path)
    
    if mime_type:
        if mime_type == 'application/json':
            try:
                with open(file_path, 'r') as file:
                    content = json.load(file)
                return file_name, mime_type, json.dumps(content, indent=2)
            except json.JSONDecodeError:
                return file_name, mime_type, "Invalid JSON file"
        elif mime_type.startswith('text/'):
            with open(file_path, 'r') as file:
                return file_name, mime_type, file.read()
        elif mime_type.startswith('image/'):
            with open(file_path, 'rb') as file:
                image_data = base64.b64encode(file.read()).decode('utf-8')
            return file_name, mime_type, f"data:{mime_type};base64,{image_data}"
    
    return file_name, "application/octet-stream", None