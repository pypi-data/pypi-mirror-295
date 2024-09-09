import json
from functools import reduce
from typing import Callable, Tuple, List

PNG_SIGNAL_S = "<png-start>"
PNG_SIGNAL_E = "<png-end>"


def __parse_markdown_cell(cell: dict) -> List[str]:
    return cell["source"]


def __parse_output(output: dict) -> List[str]:
    output_parsers = {
        "stream": lambda o: __parse_stdout_output(o) if o["name"] == "stdout" else [],
        "display_data": lambda o: [PNG_SIGNAL_S, o["data"]["image/png"], PNG_SIGNAL_E] if "image/png" in o["data"] else []
    }
    return output_parsers.get(output["output_type"], lambda o: [])(output)


def __parse_stdout_output(output: dict) -> List[str]:
    return ['```\n'] + ['>>> ' + out for out in output.get("text", [])] + ['```\n'] if output.get("text") else []


def __handle_cell(cell_parser, code_parser, cell: dict) -> List[str]:
    parsed_cell = cell_parser(cell)
    parsed_code = code_parser(cell)
    return parsed_cell + parsed_code


def cell_parser_regular(cell: dict) -> List[str]:
    """Parses cells such that cells are placed in the next available space in a PDF."""
    return ['\n\n'] + __parse_markdown_cell(cell) + ['\n'] if cell["cell_type"] == "markdown" else []


def cell_parser_one_cell_per_page(cell: dict) -> List[str]:
    """Parses cells such that every cell ends with a page break."""
    if cell["cell_type"] == "markdown":
        return ['\n\\newpage'] + ['\n\n'] + __parse_markdown_cell(cell) + ['\n']
    elif cell["cell_type"] == "code":
        return ['\n\\newpage']
    return []


def cell_parser_one_md_cell_per_page(first_cell: bool, cell: dict) -> Tuple[List[str], bool]:
    """Parses cells such that each markdown cell specifically starts with a page break."""
    content = ['\n\n'] + __parse_markdown_cell(cell)
    if cell["cell_type"] == "markdown":
        if first_cell:
            return content, False
        return ['\\newpage'] + content, False
    return [], first_cell


def code_parser_regular(cell: dict) -> List[str]:
    """Parses code cells such that both the code itself and the code's output are included within the PDF."""
    code_content = ['\n```py\n'] + cell["source"] + ['\n```\n\n'] if cell["cell_type"] == "code" else []
    output_content = reduce(lambda acc, output: acc + __parse_output(output), cell["outputs"], []) if cell["cell_type"] == "code" else []
    return code_content + output_content


def code_parser_source_only(cell: dict) -> List[str]:
    """Parses code cells such that only the code itself is included within the PDF."""
    return ['\n```py\n'] + cell["source"] + ['\n```\n\n'] if cell["cell_type"] == "code" else []


def code_parser_output_only(cell: dict) -> List[str]:
    """Parses code cells such that only the code's output is included within the PDF."""
    return reduce(lambda acc, output: acc + __parse_output(output), cell["outputs"], []) if cell["cell_type"] == "code" else []


def __handle_cell_with_first_cell(cell_parser, code_parser, first_cell, cell: dict) -> Tuple[List[str], bool]:
    if cell_parser == cell_parser_one_md_cell_per_page:
        parsed_cell, first_cell = cell_parser(first_cell, cell)
    else:
        parsed_cell = cell_parser(cell)
    parsed_code = code_parser(cell)
    return parsed_cell + parsed_code, first_cell


def parse_ipynb(path: str, 
          cell_parser: Callable = cell_parser_regular, 
          code_parser: Callable = code_parser_regular) -> List[str]:
    """Parses a `.ipynb` file, converting its JSON structure to a `.pypdfnb` JSON structure.

    Args:
        path (str): the path of the `.ipynb` file to parse.
        cell_parser (Callable, optional): the cell parsing Callable to utilize when parsing. Defaults to `cell_parser_regular`.
        code_parser (Callable, optional): the code parsing Callable to utilize when parsing. Defaults to `code_parser_regular`.

    Returns:
        List[str]: the `.pypdfnb` JSON structure - a list of strings representing the `.ipynb` contents.
    """
    with open(path, 'r') as f:
        file_data = json.load(f)

    first_cell = True

    content = []
    for cell in file_data["cells"]:
        if cell_parser == cell_parser_one_md_cell_per_page:
            parsed_cell, first_cell = __handle_cell_with_first_cell(cell_parser, code_parser, first_cell, cell)
        else:
            parsed_cell, first_cell = __handle_cell(cell_parser, code_parser, cell), first_cell

        content += parsed_cell

    return content