from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
import textwrap as _textwrap
import wcwidth as _wcwidth

import ansi_sgr as _sgr

if _TYPE_CHECKING:
    from typing import Literal
    from pyprotocol import Stringable


def admonition(
    title: Stringable,
    text: Stringable,
    emoji: Stringable | None = None,
    title_styles: int | str | list[int | str] = "bold",
    title_color: int | str | tuple = (255, 255, 255),
    title_bg_color: int | str | tuple = (70, 0, 0),
    title_margin_top: int | None = None,
    title_margin_bottom: int | None = None,
    title_margin_left: int | None = None,
    title_margin_right: int | None = None,
    title_align: Literal["left", "right", "center"] = "left",
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    text_bg_color: int | str | tuple = None,
    text_margin_top: int | None = None,
    text_margin_bottom: int | None = None,
    text_margin_left: int | None = None,
    text_margin_right: int | None = None,
    text_align: Literal["left", "right", "center"] = "left",
    char_top: Stringable | None = None,
    char_bottom: Stringable | None = "━",
    char_left: Stringable | None = "┃",
    char_right: Stringable | None = "┃",
    char_top_left: Stringable | None = "┏",
    char_top_right: Stringable | None = "┓",
    char_bottom_left: Stringable | None = "┗",
    char_bottom_right: Stringable | None = "┛",
    line_width: int = 70,
):
    title = str(title)
    if emoji:
        title = f"{emoji} {title}"
    title_section = block(
        text=title,
        text_styles=title_styles,
        text_color=title_color,
        bg_color=title_bg_color,
        char_top=char_top,
        char_bottom="",
        char_left=char_left,
        char_right=char_right,
        char_top_left=char_top_left,
        char_top_right=char_top_right,
        margin_top=title_margin_top,
        margin_bottom=title_margin_bottom,
        margin_left=title_margin_left or text_margin_left,
        margin_right=title_margin_right or text_margin_right,
        line_width=line_width,
        align=title_align,
    )
    body_section = block(
        text=text,
        text_styles=text_styles,
        text_color=text_color,
        bg_color=text_bg_color,
        char_top="",
        char_bottom=char_bottom,
        char_left=char_left,
        char_right=char_right,
        char_bottom_left=char_bottom_left,
        char_bottom_right=char_bottom_right,
        margin_top=text_margin_top,
        margin_bottom=text_margin_bottom,
        margin_left=text_margin_left or title_margin_left,
        margin_right=text_margin_right or title_margin_right,
        line_width=line_width,
        align=text_align,
    )
    return f"{title_section}\n{body_section}"


def block(
    text: Stringable,
    text_styles: int | str | list[int | str] = None,
    text_color: int | str | tuple = None,
    bg_color: int | str | tuple = None,
    char_top: Stringable | None = "━",
    char_bottom: Stringable | None = "━",
    char_left: Stringable | None = "┃",
    char_right: Stringable | None = "┃",
    char_top_left: Stringable | None = "┏",
    char_top_right: Stringable | None = "┓",
    char_bottom_left: Stringable | None = "┗",
    char_bottom_right: Stringable | None = "┛",
    margin_top: int | None = None,
    margin_bottom: int | None = None,
    margin_left: int | None = None,
    margin_right: int | None = None,
    line_width: int = 50,
    align: Literal["left", "right", "center"] = "left",
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
        screen_width = _wcwidth.wcswidth(line)
        char_width = len(line)
        extra_padding = char_width - screen_width
        width = line_width + extra_padding
        if align == "left":
            line = line.ljust(width)
        elif align == "right":
            line = line.rjust(width)
        else:
            line = line.center(width)
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
    total_line_width = line_width + (margin_left or 0) + (margin_right or 0)
    if char_top:
        line_top = f"{char_top_left}{char_top * total_line_width}{char_top_right}"
        formatted_lines.insert(0, line_top)
    if char_bottom:
        line_bottom = f"{char_bottom_left}{char_bottom * total_line_width}{char_bottom_right}"
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
