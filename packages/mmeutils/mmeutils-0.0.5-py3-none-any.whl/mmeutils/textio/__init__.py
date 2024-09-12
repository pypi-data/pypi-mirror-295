"""Text Input/Output Utility Functions"""


from typing import Iterable, List


__all__: List[str] = [
    'strip_discard_empty_lines',
]


def strip_discard_empty_lines(lines: Iterable[str]) -> list[str]:
    """Sanitizes string lines in an iterable such that:

    * Leading and trailing whitespace is discarded ("strip()")
    * Empty lines (including whitespace-only) are discarded

    :param lines: An iterable of string lines to process
    :type lines: Iterable[st]

    :return: The list of normalized (non-empty) strings.
    :rtype: list[str]
    """
    return list(
        [
            line.strip()
            for line in lines
            if line.strip()
        ]
    )
