import os
from typing import Iterable

import fitz

from jupdf.pypdfnb import PYPDFNB, FileNotReadError
from jupdf.pypdfnb_converter import convert


def __handle_temp(func):
    def wrapper(*args, **kwargs):
        if os.path.exists('temp'):
            os.system('rmdir /s /q temp')
        result = func(*args, **kwargs)
        if os.path.exists('temp'):
            os.system('rmdir /s /q temp')
        return result
    return wrapper


@__handle_temp
def single_to_pdf(pypdfnb: PYPDFNB, dst: str) -> bool:
    """Converts a single `PYPDFNB` instance to a single PDF file.

    Args:
        pypdfnb (PYPDFNB): the `PYPDFNB` instance to convert.
        dst (str): the path to save the `.pdf` file too.

    Raises:
        FileNotReadError: raised if the contents of `pypdfnb` are empty (`[]`).
    
    Returns:
        bool: whether or not the operation was successful.
    """
    if pypdfnb.is_empty:
        raise FileNotReadError
    return convert(pypdfnb, dst)


@__handle_temp
def multiple_to_pdf(pypdfnbs: Iterable[PYPDFNB], dst: str) -> None:
    """Converts an iterable of `PYPDFNB` instances to a single PDF file. Skips any instances are empty.

    Args:
        pypdfnbs (Iterable[PYPDFNB]): the iterable of `PYPDFNB` instances to convert.
        dst (str): the path to save the `.pdf` file too.
    """
    pdfs = []
    for i, pypdfnb in enumerate(pypdfnbs):
        if pypdfnb.is_empty:
            continue
        if convert(pypdfnb, f'temp/tmp-{i}.pdf'):
            pdfs.append(f'temp/tmp-{i}.pdf')
    
    if not pdfs:
        return
    
    r = fitz.open()
    
    for pdf in pdfs:
        with fitz.open(pdf) as f:
            r.insert_pdf(f)
    
    r.save(dst)
