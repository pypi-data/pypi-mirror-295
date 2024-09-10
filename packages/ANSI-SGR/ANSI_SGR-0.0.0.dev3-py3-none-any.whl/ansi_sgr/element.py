from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import textwrap as _textwrap

import ansi_sgr as _sgr

if _TYPE_CHECKING:
    from typing import Literal
    from pyprotocol import Stringable


def admonition(
    title: Stringable,
    text: Stringable,
    title_styles: int | str | list[int | str] = None,
    title_color: int | str | tuple = None,
    title_bg_color: int | str | tuple = None,
    title_char_top: Stringable | None = None,
    title_char_bottom: Stringable | None = None,
    title_char_left: Stringable | None = None,
    title_char_right: Stringable | None = None,
    title_align: Literal["left", "right", "center"] = "left",
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    text_bg_color: int | str | tuple = None,
    text_char_top: Stringable | None = None,
    text_char_bottom: Stringable | None = None,
    text_char_left: Stringable | None = None,
    text_char_right: Stringable | None = None,
    margin_top: int | None = None,
    margin_middle: int | None = None,
    margin_bottom: int | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
    line_width: int = 50,
):
    title = str(title)
    if title_align == "left":
        title = title.ljust(line_width)
    elif title_align == "right":
        title = title.rjust(line_width)
    else:
        title = title.center(line_width)
    title_section = block(
        title,
        text_styles=title_styles,
        text_color=title_color,
        bg_color=title_bg_color,
        char_top=title_char_top,
        char_bottom=title_char_bottom,
        char_left=title_char_left,
        char_right=title_char_right,
        margin_top=margin_top,
        margin_left=margin_left,
        margin_right=margin_right,
    )
    body_section = block(
        text=text,
        text_styles=text_styles,
        text_color=text_color,
        bg_color=text_bg_color,
        char_top=text_char_top,
        char_bottom=text_char_bottom,
        char_left=text_char_left,
        char_right=text_char_right,
        margin_top=margin_middle,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        line_width=line_width,
    )
    return f"{title_section}\n{body_section}"


def block(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    char_top: Stringable | None = None,
    char_bottom: Stringable | None = None,
    char_left: Stringable | None = None,
    char_right: Stringable | None = None,
    margin_top: int | None = None,
    margin_bottom: int | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
    line_width: int = 50,
):
    lines = _textwrap.wrap(
        text=str(text),
        width=line_width,
        expand_tabs=True,
        tabsize=4,
        replace_whitespace=False,
        drop_whitespace=False,
    )
    if margin_left is None:
        margin_left = margin_right
    if margin_right is None:
        margin_right = margin_left
    if margin_top is None:
        margin_top = margin_bottom
    if margin_bottom is None:
        margin_bottom = margin_top
    if margin_top:
        lines = [" " * line_width] * margin_top + lines
    if margin_bottom:
        lines = lines + [" " * line_width] * margin_bottom
    formatted_lines = []
    for line in lines:
        line = line.ljust(line_width)
        formatted_lines.append(
            inline(
                line,
                text_styles=text_styles,
                text_color=text_color,
                bg_color=bg_color,
                char_left=char_left,
                char_right=char_right,
                margin_left=margin_left,
                margin_right=margin_right,
            )
        )
    if char_top is None:
        char_top = char_bottom or ""
    if char_bottom is None:
        char_bottom = char_top or ""
    if char_left is None:
        char_left = char_right or ""
    if char_right is None:
        char_right = char_left or ""
    total_line_width = line_width + (margin_left or 0) + (margin_right or 0)
    space_left = " " * len(str(char_left)) if char_left else 0
    space_right = " " * len(str(char_right)) if char_right else 0
    if char_top:
        line_top = f"{space_left}{char_top * total_line_width}{space_right}"
        formatted_lines.insert(0, line_top)
    if char_bottom:
        line_bottom = f"{space_left}{char_bottom * total_line_width}{space_right}"
        formatted_lines.append(line_bottom)
    return "\n".join(formatted_lines)


def inline(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    char_left: Stringable | None = None,
    char_right: Stringable | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
):
    sequence = _sgr.create_sequence(text_styles, text_color, bg_color)
    text = str(text)
    if char_left is None:
        char_left = char_right or ""
    if char_right is None:
        char_right = char_left or ""
    if margin_left is None:
        margin_left = margin_right
    if margin_right is None:
        margin_right = margin_left
    if margin_left:
        text = " " * margin_left + text
    if margin_right:
        text = text + " " * margin_right
    text_box = _sgr.apply_sequence(text, sequence, reset=True)
    return f"{char_left}{text_box}{char_right}"
