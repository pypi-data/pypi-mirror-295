import base64
import os
import pkg_resources
import re
import subprocess

from jupdf.pypdfnb import PYPDFNB

PNG_PATTERN = re.compile(r'(<png-start>(.+?)<png-end>)', re.DOTALL)


def __ensure_temp():
    if not os.path.exists('temp'):
        os.mkdir('temp')


def __write_temp_md_file(prepared_pypdfnb_content: str, temp_md_path: str) -> None:
    with open(temp_md_path, 'w') as f:
        f.write(prepared_pypdfnb_content)


def __get_prepared_pypdfnb_content_with_metadata(prepared_pypdfnb_content: str, metadata: dict) -> str:
    keywords = metadata.get("keywords", [])
    kstring = '[' + ', '.join(keywords) + ']' if keywords else ''
    
    a = [f'title: "{metadata["title"]}"'] if metadata.get("title") else []
    b = [f'author: [{metadata["author"]}]'] if metadata.get("author") else []
    c = [f'date: "{metadata["date"]}"'] if metadata.get("date") else []
    d = [f'subject: "{metadata["subject"]}"'] if metadata.get("subject") else []
    e = [f'keywords: {kstring}'] if kstring else []
    f = [f'lang: "{metadata["lang"]}"'] if metadata.get("lang") else [] 
    g = [f'listings: {metadata["listings"]}'] if metadata.get("listings") else []
    h = [f'titlepage: {metadata["titlepage"]}'] if metadata.get("titlepage") else []

    lines = a + b + c + d + e + f + g + h
    
    if lines:
        mstring = \
f"""---
{'\n'.join(lines)}
...
"""
        return mstring + '\n' + prepared_pypdfnb_content
    else:
        return prepared_pypdfnb_content


def __build_pandoc_command(temp_md_path: str, out_path: str, template_path: str) -> list:
    return [
        'pandoc',
        temp_md_path,
        '-o', out_path,
        '--pdf-engine=xelatex',
        '--template', template_path,
    ]

def __run_pandoc_command(command: list) -> bool:
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error in Pandoc conversion: {e}")
        return False


def __remove_temp_file(temp_md_path: str) -> None:
    if os.path.exists(temp_md_path):
        os.remove(temp_md_path)


def __prepare_pypdfnb_content(pypdfnb: PYPDFNB) -> str:
    prepared_pypdfnb = ''.join(pypdfnb.content)
    
    __ensure_temp()

    def replace_png(match):
        nonlocal img_count
        img = match.group(2)
        img_data = base64.b64decode(img)
        img_path = f'temp/{img_count}.png'
        
        with open(img_path, 'wb') as f:
            f.write(img_data)
        
        img_count += 1
        return f'\n![]({img_path})'

    img_count = 0
    prepared_pypdfnb = re.sub(PNG_PATTERN, replace_png, prepared_pypdfnb)
    
    return prepared_pypdfnb


def convert(pypdfnb: PYPDFNB, dst: str) -> bool:
    temp_md_path = 'temp/temp.md'
    template_path = pkg_resources.resource_filename('jupdf', 'tex/modded_eisvogel.tex')
    
    __ensure_temp()
    
    prepared_pypdfnb_content = __prepare_pypdfnb_content(pypdfnb)
    
    if pypdfnb.metadata is not None:
        meta_prepared_pypdfnb_content = __get_prepared_pypdfnb_content_with_metadata(prepared_pypdfnb_content, pypdfnb.metadata)
    else:
        meta_prepared_pypdfnb_content = prepared_pypdfnb_content
    
    __write_temp_md_file(meta_prepared_pypdfnb_content, temp_md_path)
    
    pandoc_command = __build_pandoc_command(temp_md_path, dst, template_path)
    
    pandoc_cmd_successful = __run_pandoc_command(pandoc_command)
    
    __remove_temp_file(temp_md_path)
    
    return pandoc_cmd_successful
