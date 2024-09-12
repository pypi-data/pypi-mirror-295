"""File Input/Output Utility Functions"""


from typing import List, Optional


__all__: List[str] = [
    'read_text_file_to_string',
    'validate_json_file',
]


import json

from logging import debug
from pathlib import Path


def read_text_file_to_string(file_name: Optional[str|Path]) -> str:
    """Read contents of a text file into a single string.

    Lines will be normalized ie. stripped and empty lines discarded.
    Lines will then be joined using the line-separation character (\\n).

    :param file_name: Name/path of the file to process.
    :type file_name: Optional[str|Path]

    :return: A string of all the non-empty lines joined by \\n.
    :rtype: str
    """
    with open(str(file_name), 'r', encoding='utf-8') as file:
        from ..textio import strip_discard_empty_lines

        lines = strip_discard_empty_lines(file.readlines())
        return '\n'.join(lines)


def validate_json_file(file_name: Optional[str|Path]) -> bool:
    """Validate that a JSON file is neither empty nor invalid.

    Empty means all whitespace, an empty object or an empty array.
    Invalid means it cannot be parsed as valid JSON.
    And the file must exist in the first place.

    :param file_name: Name/path of the JSON file to check.
    :type file_name: Optional[str|Path]

    :return: True if file exists and has valid non-empty JSON content.
        False otherwise.
    :rtype: bool
    """

    if not Path(str(file_name)).exists():
        debug(f'validate_json_file(): File {str(file_name)} not found')
        return False

    contents = read_text_file_to_string(file_name)

    if contents == '':
        debug(f'validate_json_file(): {str(file_name)} is empty')
        return False

    try:
        obj = json.loads(contents)

        if len(obj) == 0:
            debug(f'validate_json_file(): {str(file_name)} has empty object/array')
            return False
        
        else:
            debug(f'validate_json_file(): {str(file_name)} is valid')
            return True
    
    except json.JSONDecodeError as jde:
        debug(f'validate_json_file(): {str(file_name)} is invalid: {jde}')
        return False
