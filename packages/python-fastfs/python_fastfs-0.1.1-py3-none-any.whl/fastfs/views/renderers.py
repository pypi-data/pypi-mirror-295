from fasthtml.common import *
from fastfs.utils.helpers import get_file_info, format_size, format_date, get_file_icon, get_file_content
import os
from fastfs.config import get_settings

settings = get_settings()

def render_preview(file_path: str) -> Div:
    file_name, mime_type, content = get_file_content(file_path)
    
    if content is not None:
        if mime_type.startswith('image/'):
            preview_content = Div(cls='image-container')(
                Img(src=content, cls="max-w-full max-h-[400px] object-contain")
            )
        elif mime_type == 'application/json' or mime_type.startswith('text/'):
            preview_content = Pre(content, cls="bg-gray-100 p-4 rounded-md overflow-auto")
        else:
            preview_content = P(f"Preview not available for this file type: {mime_type}", cls="text-gray-500 italic")
    else:
        preview_content = P(f"Preview not available for this file type: {mime_type}", cls="text-gray-500 italic")

    return Div(cls='file-preview w-full h-full')(
        H3(file_name, cls="text-lg font-semibold mb-2"),
        preview_content
    )

def render_file_list(tree, current_path: str) -> Div:
    return Table(cls="flex flex-col h-full")(
        # Fixed header
        Thead(cls="bg-gray-50 sticky top-0 z-10")(
            Tr(cls="flex text-left text-xs font-medium text-gray-500 uppercase tracking-wider")(
                Th("Name", cls="w-2/5 p-3"),
                Th("Size", cls="w-1/6 p-3 text-right"),
                Th("Kind", cls="w-1/6 p-3 text-center"),
                Th("Date Added", cls="w-1/4 p-3 text-right"),
            )
        ),
        # Scrollable content
        Tbody(cls="flex-1 overflow-auto")(
            *[Tr(cls="flex hover:bg-gray-50")(
                Td(cls="w-2/5 p-3 flex items-center space-x-2")(
                    I(cls=f'fas {get_file_icon(item[0])} text-gray-400 flex-shrink-0'),
                    Div(cls='truncate')(
                        A(item[1], 
                        href=f'/{os.path.relpath(item[2], settings.base_dir)}' if item[0] == 'folder' else '#',
                        hx_get=f'/{os.path.relpath(item[2], settings.base_dir)}?preview=true' if item[0] == 'file' else None,
                        hx_target='#preview-area',
                        cls='text-gray-900 hover:text-blue-600')
                        # A(item[1], 
                        #     href=f'/{os.path.relpath(item[2], base_dir)}' if item[0] == 'folder' else '#',
                        #     onclick=f"showPreview('{os.path.relpath(item[2], base_dir)}')" if item[0] == 'file' else None,
                        #     cls='text-gray-900 hover:text-blue-600')
                    )
                ),
                Td(format_size(get_file_info(item[2])[0]), cls='w-1/6 p-3 text-right text-gray-500 text-sm'),
                Td(Div(get_file_info(item[2])[2], cls='truncate'), cls='w-1/6 p-3 text-left text-gray-500 text-sm'),
                Td(Div(format_date(get_file_info(item[2])[1]), cls='truncate'), cls='w-1/4 p-3 text-right text-gray-500 text-sm'),
            ) for item in tree]
        )
    )

def render_main_page(path: str, file_list: Div):
    breadcrumb_items = [
        A('~', href='/'),
        *[Span('/') +  A(part, href=f'/{"/".join(path.split("/")[:i+1])}')
          for i, part in enumerate(path.split('/')) if part]
    ]
    
    return Title("File System Interface"), Div(cls="h-screen min-h-screen bg-gray-100 text-gray-900 flex overflow-hidden")(
        # Sidebar
        Div(cls="w-64 bg-white shadow-lg fixed h-full")(
            Div(cls="p-4")(
                Input(type="text", cls="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    placeholder="Search files...",
                    hx_get=f"/{path}", hx_trigger="keyup changed delay:100ms", 
                    hx_target="#file-list-container",
                    hx_push_url="false",
                    name="search"),
            ),
            Div(cls="mt-4")(
                Div("All", cls="px-4 py-2 bg-blue-500 text-white cursor-pointer"),
                Div("Local", cls="px-4 py-2 hover:bg-gray-100 cursor-pointer"),
                Div("FTP", cls="px-4 py-2 hover:bg-gray-100 cursor-pointer"),
                Div("S3", cls="px-4 py-2 hover:bg-gray-100 cursor-pointer")
            )
        ),
        # Main content
        # Div(cls="w-full h-full ml-64 flex flex-col overflow-hidden")(
        Div(cls="ml-64 flex-1 flex flex-col overflow-hidden")(
            # Breadcrumb
            Div(cls="w-full p-4 bg-white shadow-md")(
                Div(cls="text-sm text-gray-600")(*breadcrumb_items)
            ),
            # File list and Preview area
            # Div(cls="h-full flex-grow flex p-6 overflow-hidden")(
            Div(cls="flex-1 flex p-6 space-x-4 overflow-hidden")(
                # File list
                Div(cls="w-3/5 pr-4 h-full max-w-full overflow-auto")(
                    # Div(id="file-list-container", cls="bg-white rounded-lg shadow-md h-[calc(100vh-160px)] overflow-auto")(
                    Div(id="file-list-container", cls="h-full max-h-full flex-1 bg-white rounded-lg shadow-md overflow-hidden")(
                        file_list
                    )
                ),
                # Preview area
                Div(cls="w-2/5 bg-white rounded-lg shadow-md overflow-hidden")(
                    # Div(id='preview-area', cls="h-full p-4 overflow-auto")(
                    Div(id='preview-area', cls="flex-1 p-4 overflow-auto h-full pb-2")(
                        P("Select a file to preview", cls="text-gray-500 italic")
                    )
                )
            )
        ),
    )