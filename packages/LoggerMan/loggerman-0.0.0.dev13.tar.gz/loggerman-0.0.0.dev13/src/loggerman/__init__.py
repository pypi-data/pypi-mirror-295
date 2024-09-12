"""LoggerMan"""
from __future__ import annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from loggerman import style
from loggerman.logger import Logger, LogLevel


if _TYPE_CHECKING:
    from typing import Type, Sequence, Callable
    from mdit.protocol import TargetConfig, ANSITargetConfig
    from loggerman.style import LogLevelStyle


logger = Logger()


def create(
    realtime_levels: Sequence[str | int | LogLevel] | None = tuple(range(1, 7)),
    github: bool = False,
    github_debug: bool = True,
    title_number: int | Sequence[int] = 1,
    exception_handler: dict[Type[Exception], Callable] | None = None,
    exit_code_critical: int | None = None,
    target_config_md: dict[str, TargetConfig | dict] | None = None,
    target_config_ansi: ANSITargetConfig | dict | None = None,
    level_style_debug: LogLevelStyle = style.log_level(admo_class="hint", gh_title_prefix="🔘"),
    level_style_success: LogLevelStyle = style.log_level(admo_class="seealso", gh_title_prefix="✅"),
    level_style_info: LogLevelStyle = style.log_level(admo_class="note", gh_title_prefix="ℹ️"),
    level_style_notice: LogLevelStyle = style.log_level(admo_class="attention", gh_title_prefix="❗"),
    level_style_warning: LogLevelStyle = style.log_level(admo_class="warning", gh_title_prefix="🚨"),
    level_style_error: LogLevelStyle = style.log_level(admo_class="danger", dropdown=False,
                                                        gh_title_prefix="🚫"),
    level_style_critical: LogLevelStyle = style.log_level(admo_class="error", dropdown=False,
                                                           gh_title_prefix="⛔"),
    prefix_caller: str = "🔔",
    prefix_time: str = "⏰",
) -> Logger:
    return Logger().initialize(**locals())
