from __future__ import annotations

from typing import NamedTuple as _NamedTuple, TYPE_CHECKING as _TYPE_CHECKING
import ansi_sgr as _sgr

if _TYPE_CHECKING:
    from ansi_sgr.protocol import ANSIInlineStyle


class LogLevelStyle(_NamedTuple):
    admo_class: str
    gh_title_style: ANSIInlineStyle | None
    gh_title_prefix: str
    dropdown: bool
    show_caller: bool
    show_time: bool


def log_level(
    admo_class: str,
    gh_title_style: ANSIInlineStyle | dict | None = _sgr.protocol.ANSIInlineStyle(text_styles="bold"),
    gh_title_prefix: str = "",
    dropdown: bool = True,
    show_caller: bool = True,
    show_time: bool = True,
) -> LogLevelStyle:
    gh_title_style = gh_title_style if isinstance(
        gh_title_style, _sgr.protocol.ANSIInlineStyle
    ) else (_sgr.protocol.ANSIInlineStyle(**gh_title_style) if gh_title_style else None)
    return LogLevelStyle(
        admo_class=admo_class,
        gh_title_style=gh_title_style,
        gh_title_prefix=gh_title_prefix,
        dropdown=dropdown,
        show_caller=show_caller,
        show_time=show_time,
)