import re as _re

import numpy as _np


def plotTitle(titleStr: 'str', target_line_length: 'int'=70) -> 'str':
    """
    Format a long plot title, nicely wrapping text,
    including strings with math blocks ($a = b$) which should not be broken.

    :param titleStr: input title
    :type titleStr: str
    :param target_line_length: Targeted (non-strict) line length for wrapping, defaults to 70
    :type target_line_length: int, optional
    :return: formatted title with line breaks
    :rtype: str
    """

    titleStr = titleStr.strip()

    spaces = [m.start() for m in _re.finditer(" ", titleStr)]
    mathblocks_all = [m.start() for m in _re.finditer("\$", titleStr)]
    if len(mathblocks_all) > 0:
        mathblocks = []
        for i in range(len(mathblocks_all), 2):
            mathblocks.append((mathblocks_all[i], mathblocks_all[i + 1]))

        for r in mathblocks:
            [spaces.remove(i) for i in range(r[0], r[1]) if i in spaces]

    spaces = _np.array(spaces)

    lines = []
    remaining_length = len(titleStr)
    i0 = 0
    while remaining_length > 0:
        if len(titleStr[i0:]) < target_line_length:
            lines.append(titleStr[i0:])
            break
        line_length = target_line_length
        i = spaces[spaces < line_length * (len(lines) + 1)].max()
        lines.append(titleStr[i0:i])
        i0 = i + 1
        remaining_length = len(titleStr[i0:])

    str = ""
    for l in lines:
        str += l + "\n"

    return str[:-1]
