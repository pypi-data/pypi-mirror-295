import os
import sys
from fastapi import FastAPI
from fasthtml.common import *
from fastfs.config import get_settings
from fastfs.services.file_service import handle_directory
from fastfs.views.renderers import render_main_page
from importlib import resources

settings = get_settings()
app = FastHTML(hdrs=(
    Link(rel="stylesheet", href="/app.css", type="text/css"),
    Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css')
))
rt = app.route

@rt("/app.css")
async def get():
    with resources.path('public', 'app.css') as css_path:
        return FileResponse(str(css_path), media_type="text/css")
    # return FileResponse('public/app.css')

@rt("/")
@rt("/{path:path}")
def get(path: str = '', search: str = '', preview: bool = False, hx_request: bool = False):
    print("hello")
    full_path = os.path.normpath(os.path.join(settings.base_dir, path))
    
    if not full_path.startswith(settings.base_dir):
        return Response("Access denied: Path is outside the allowed directory.", status_code=403)

    if not os.path.exists(full_path):
        return Response("Path not found", status_code=404)

    if os.path.isfile(full_path):
        return handle_file(path, preview)
    else:
        file_list = handle_directory(path, search)
        if search or preview or hx_request:
            return file_list
        else:
            return render_main_page(path, file_list)

def main():

    # Override base_dir if provided as command-line argument
    if len(sys.argv) > 1:
        settings.base_dir = sys.argv[1]

    print(f"Serving {settings.base_dir}")

    serve(port=settings.port)

if __name__ == "__main__":
    main()