import json
import os
from typing import Optional, List, Callable

from jupdf.pypdfnb_parsing import parse_ipynb, cell_parser_regular, code_parser_regular


class FileNotReadError(Exception):
    """
    Raise this error when a user attempts to perform an operation on a PYPDFNB object's contents
    without first reading a `.ipynb` or `.pypdfnb` file.
    """
    pass


class InvalidJupyterNotebookFileError(Exception):
    """
    Raise this error when a user attempts to read a notebook file that is not of the
    `.ipynb` or `.pypdfnb` extension.
    """
    pass


def check_ipynb_file(ipynb_file: str):
    if not os.path.exists(ipynb_file):
        raise OSError(f'The provided file, {ipynb_file}, could not be found.')
    elif not ipynb_file.endswith('.ipynb'):
        raise InvalidJupyterNotebookFileError(f'The provided file, {ipynb_file}, is not a `.ipynb` file.')    


def check_pypdfnb_file(pypdfnb_file: str):
    if not os.path.exists(pypdfnb_file):
            raise OSError(f'The provided file, {pypdfnb_file}, could not be found.')
    elif not pypdfnb_file.endswith('.pypdfnb'):
        raise InvalidJupyterNotebookFileError(f'The provided file, {pypdfnb_file}, is not a `.pypdfnb` file.')


class PYPDFNB:
    def __init__(self, cell_parser: Callable = cell_parser_regular, code_parser: Callable = code_parser_regular):
        """
        A class to represent a PYPDFNB file, both from `.ipynb` and `.pypdfnb`.

        ### Parsers
        Parser callables can be provided to PYPDFNB objects before calling `read_ipynb` to
        determine how the resulting `.pypdfnb` contents will be formatted. There are two main types
        of parser: the `cell_parser` and the `code_parser`.
        
        The cell parsers determine how cells are placed. 
        - `cell_parser_regular` - if there is enough space in the PDF page, place a cell.
        - `cell_parser_one_cell_per_page` - for each page in the PDF, there must only be one cell.
        - `cell_parser_one_md_cell_per_page` - adds a page break to the end of every markdown cell specifically.
        
        The code parsers determine how code is displayed.
        - `code_parser_regular` - both the source and output are included in the PDF.
        - `code_parser_source_only` - only the source is included in the PDF.
        - `code_parser_output_only` - only the output is included in the PDF.
        
        ### Metadata
        The metadata attributes are used during the conversion of a PYPDFNB instance to PDF. If none are set,
        then the metadata is simply not considered during Pandoc conversion.
        - `title` - will show a document title in the top-left of each page.
        - `author` - will show a document author in the bottom-left of each page.
        - `date` - will show a date in the top-right of each page.
        - `subject` - non-visual; the subject of the document.
        - `keywords` - non-visual; keywords associated with the document.
        - `lang` - non-visual; the language code of the document.
        - `listings` - if True, allow Pandoc to use additional listings. Helpful for code cells in particular.
        - `titlepage` - if True, then insert a title page at the start of the document, complete with the `title`, `author`, and `date`.
        
        Args:
            cell_parser (Callable, optional): determines how cells are placed. Defaults to `cell_parser_regular`.
            code_parser (Callable, optional): determines how code is displayed. Defaults to `code_parser_regular`.
        """
        self.cell_parser = cell_parser
        self.code_parser = code_parser
        
        self.title: Optional[str] = None
        self.author: Optional[str] = None
        self.date: Optional[str] = None
        self.subject: Optional[str] = None
        self.keywords: Optional[list[str]] = None
        self.lang: Optional[str] = None
        self.listings: bool = False
        self.titlepage: bool = False
        
        self._content: List[str] = []
        self._is_open_file_ipynb = False
    
    @property
    def content(self) -> List[str]:
        return self._content

    @property
    def is_empty(self) -> bool:
        return not bool(self._content)
    
    @property
    def metadata(self) -> dict | None:
        """A dictionary of metadata given from the metadata attributes."""
        if any([self.title, self.author, self.date, self.subject, self.keywords, self.lang, self.listings, self.titlepage]):
            return {
                "title": self.title,
                "author": self.author,
                "date": self.date,
                "subject": self.subject,
                "keywords": self.keywords,
                "lang": self.lang,
                "listings": self.listings,
                "titlepage": self.titlepage
            }
        return None

    def read_ipynb(self, ipynb_file: str):
        """Reads a `.ipynb` file, parses the file using the parser callables specified."""
        check_ipynb_file(ipynb_file)
        self._content = parse_ipynb(ipynb_file, self.cell_parser, self.code_parser)
        self._is_open_file_ipynb = True

    def read_pypdfnb(self, path: str):
        """Reads a `.pypdfnb` generated via `self.write_pypdfnb`."""
        check_pypdfnb_file(path)
        
        with open(path, 'r') as f:
            self._content = json.load(f)
        self._is_open_file_ipynb = False

    def write_pypdfnb(self, filename: str, dst_dir: str = '.', ipynb_file: Optional[str] = None):
        """
        Writes a `.ipynb` file to a `.pypdfnb` format, escaping parsing in the future.
        
        If there is no `ipynb_file` provided, check if this instance is open instead. If it is,
        write the currently opened file to a `.pypdfnb`.

        Args:
            filename (str): the name of the pypdfnb. You do not need to include `.pypdfnb` at the end of the file, if you prefer JSON.
            dst_dir (str, optional): the directory to save the .`pypdfbn` to. Defaults to '.'.
            ipynb_file (Optional[str], optional): a path to a `.ipynb` people. Defaults to None.

        Raises:
            FileNotReadError: raised if the instance is not marked as open.
        """
        if ipynb_file is not None:
            check_ipynb_file(ipynb_file)
            content = parse_ipynb(ipynb_file, self.cell_parser, self.code_parser)
        else:
            if not self._is_open_file_ipynb:
                raise FileNotReadError(
                    'There is currently no .ipynb file read. Please read an .ipynb file before using this method without giving a file path.')
            content = self._content
        
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        if filename.endswith('.pypdfnb'):
            filename = filename[:-8]
        with open(f'{dst_dir}/{filename}.pypdfnb', 'w') as f:
            f.write(json.dumps(content))

    def empty(self):
        """Sets the contents of the instance back to `[]`."""
        self._contents = []
        self._is_open_file_ipynb = False
