from __future__ import annotations

import sys
from enum import Enum as _Enum
import datetime as _datetime
from typing import NamedTuple as _NamedTuple, Sequence as _Sequence, TYPE_CHECKING as _TYPE_CHECKING
import inspect as _inspect
import sys as _sys
import traceback as _traceback
from functools import wraps as _wraps

import ansi_sgr as _sgr
import actionman as _actionman
import mdit as _mdit

from loggerman import style as _style


if _TYPE_CHECKING:
    from typing import Literal, Sequence, Callable, Type
    from pyprotocol import Stringable
    from loggerman.style import LogLevelStyle


class LogLevel(_Enum):
    DEBUG = 0
    SUCCESS = 1
    INFO = 2
    NOTICE = 3
    WARNING = 4
    ERROR = 5
    CRITICAL = 6

class _LogLevelData(_NamedTuple):
    level: LogLevel
    style: LogLevelStyle


class Logger:

    def __init__(self):
        self._doc: _mdit.Document | None = None
        self._initialized: bool = False
        self._realtime_levels: list = []
        self._github: bool = False
        self._github_debug: bool = True
        self._next_section_num: list[int] = []
        self._default_exit_code: int | None = None
        self._exception_handler: dict[Type[Exception], Callable] | None = None
        self._level: dict[str, _LogLevelData] = {}
        self._emoji_caller: str = ""
        self._emoji_time: str = ""
        self._out_of_section: bool = False
        self._target_config_md: dict[str, _mdit.TargetConfig | dict] | None = None
        self._target_config_ansi: _mdit.ANSITargetConfig | dict | None = None
        return

    @property
    def report(self) -> _mdit.Document:
        return self._doc

    def initialize(
        self,
        realtime_levels: Sequence[str | int | LogLevel] | None = None,
        github: bool = False,
        github_debug: bool = True,
        title_number: int | _Sequence[int] = 1,
        exception_handler: dict[Type[Exception], Callable] | None = None,
        exit_code_critical: int | None = None,
        target_config_md: dict[str, _mdit.TargetConfig | dict] | None = None,
        target_config_ansi: _mdit.ANSITargetConfig | dict | None = None,
        level_style_debug: LogLevelStyle = _style.log_level(admo_class="hint", gh_title_prefix="🔘"),
        level_style_success: LogLevelStyle = _style.log_level(admo_class="seealso", gh_title_prefix="✅"),
        level_style_info: LogLevelStyle = _style.log_level(admo_class="note", gh_title_prefix="ℹ️"),
        level_style_notice: LogLevelStyle = _style.log_level(admo_class="attention", gh_title_prefix="❗"),
        level_style_warning: LogLevelStyle = _style.log_level(admo_class="warning", gh_title_prefix="🚨"),
        level_style_error: LogLevelStyle = _style.log_level(admo_class="danger", dropdown=False, gh_title_prefix="🚫"),
        level_style_critical: LogLevelStyle = _style.log_level(admo_class="error", dropdown=False, gh_title_prefix="⛔"),
        prefix_caller: str = "🔔",
        prefix_time: str = "⏰",
    ):
        def process_exit_code():
            error_msg_exit_code = (
                "Argument `exit_code_on_error` must be a positive integer or None, "
                f"but got '{exit_code_critical}' (type: {type(exit_code_critical)})."
            )
            if isinstance(exit_code_critical, int):
                if exit_code_critical <= 0:
                    raise ValueError(error_msg_exit_code)
            elif exit_code_critical is not None:
                raise TypeError(error_msg_exit_code)
            self._default_exit_code = exit_code_critical
            return

        if self._initialized:
            return
        if realtime_levels:
            for level in realtime_levels:
                self._realtime_levels.append(self._get_level_name(level))
        self._github = github
        self._github_debug = github_debug
        self._next_section_num = list(title_number) if isinstance(title_number, Sequence) else [1] * title_number
        self._exception_handler = exception_handler
        process_exit_code()
        self._level = {
            "debug": _LogLevelData(level=LogLevel.DEBUG, style=level_style_debug),
            "success": _LogLevelData(level=LogLevel.SUCCESS, style=level_style_success),
            "info": _LogLevelData(level=LogLevel.INFO, style=level_style_info),
            "notice": _LogLevelData(level=LogLevel.NOTICE, style=level_style_notice),
            "warning": _LogLevelData(level=LogLevel.WARNING, style=level_style_warning),
            "error": _LogLevelData(level=LogLevel.ERROR, style=level_style_error),
            "critical": _LogLevelData(level=LogLevel.CRITICAL, style=level_style_critical),
        }
        self._emoji_caller = prefix_caller
        self._emoji_time = prefix_time
        self._target_config_md = target_config_md
        self._target_config_ansi = target_config_ansi
        self._initialized = True
        return

    def sectioner(
        self,
        title: str | None = None,
        handler: dict[Type[Exception], Callable] | None = None,
        stack_up: int = 0,
        **handler_kwargs,
    ):
        """Decorator for sectioning a function or method."""
        def section_decorator(func: Callable):
            @_wraps(func)
            def section_wrapper(*args, **kwargs):
                if title:
                    self.section(title=title, stack_up=stack_up+1)
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    return exception_handler(self._exception_handler | handler, e, func, args, kwargs)
                else:
                    if title:
                        self.section_end()
                    return result
            return section_wrapper

        def exception_handler(handlers, e, func, args, kwargs):
            for exc_type, exc_handler in handlers.items():
                if isinstance(e, exc_type):
                    to_raise, return_val = exc_handler(self, e, func, args, kwargs, **handler_kwargs)
                    if title:
                        self.section_end()
                    if to_raise:
                        raise to_raise
                    return return_val
            if title:
                self.section_end()
            raise e

        handler = handler or {}
        return section_decorator

    def section(
        self,
        title: str,
        key: str | None = None,
        conditions: str | list[str] | None = None,
        stack_up: int = 0
    ):
        if not self._initialized:
            self.initialize()
        heading = _mdit.element.heading(
            content=title,
            level=self._next_section_num,
            explicit_number=True,
        )
        sig = self._get_sig(stack_up=stack_up + 1)
        if self._realtime_levels:
            heading_ansi = heading.source(target="ansi")
            sig_ansi = sig.source(target="ansi")
            self._print(f"{heading_ansi}\n{sig_ansi}")
        if not self._doc:
            self._doc = _mdit.document(
                heading=heading,
                target_config_md=self._target_config_md,
                target_config_ansi={"ansi": self._target_config_ansi} if self._target_config_ansi else None,
            )
        else:
            self._doc.open_section(heading=heading, key=key, conditions=conditions)
        self._doc.current_section.body.append(content=sig, key="signature")
        self._doc.current_section.body.append(
            content=_mdit.element.ordered_list(),
            key="logs",
        )
        self._next_section_num.append(1)
        return

    def section_end(self):
        self._doc.close_section()
        if len(self._next_section_num) > 1:
            self._next_section_num.pop()
            self._next_section_num[-1] += 1
        self._out_of_section = True
        return

    def log(
        self,
        level: LogLevel | str | int,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ):
        if not self._initialized:
            self.initialize()
        if self._out_of_section:
            self.section(title=self._get_caller_name(stack_up+1), stack_up=stack_up+1)
        self._submit_log(
            level=level,
            title=title,
            content=content,
            content_md=content_md,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            file_content=file_content,
            file_line=file_line,
            file_line_end=file_line_end,
            file_language=file_language,
            stack_up=stack_up + 1
        )
        level_name = self._get_level_name(level)
        level = self._level[level_name]
        if level.level is LogLevel.CRITICAL:
            if sys_exit is None:
                sys_exit = self._default_exit_code is not None
        if level is LogLevel.CRITICAL and sys_exit:
            _sys.stdout.flush()
            _sys.stderr.flush()
            _sys.stdin.flush()
            exit_code = exit_code or self._default_exit_code
            _sys.exit(exit_code)
        return

    def debug(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.DEBUG, title=title, content=content, content_md=content_md, stack_up=stack_up + 1
        )

    def success(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.SUCCESS, title=title, content=content, content_md=content_md, stack_up=stack_up + 1
        )

    def info(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.INFO, title=title, content=content, content_md=content_md, stack_up=stack_up + 1
        )

    def notice(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.NOTICE,
            title=title,
            content=content,
            content_md=content_md,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            file_content=file_content,
            file_line=file_line,
            file_line_end=file_line_end,
            file_language=file_language,
            stack_up=stack_up + 1
        )

    def warning(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.WARNING,
            title=title,
            content=content,
            content_md=content_md,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            file_content=file_content,
            file_line=file_line,
            file_line_end=file_line_end,
            file_language=file_language,
            stack_up=stack_up + 1
        )

    def error(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ) -> None:
        return self.log(
            level=LogLevel.ERROR,
            title=title,
            content=content,
            content_md=content_md,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            file_content=file_content,
            file_line=file_line,
            file_line_end=file_line_end,
            file_language=file_language,
            stack_up=stack_up + 1
        )

    def critical(
        self,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        sys_exit: bool | None = None,
        exit_code: int | None = None,
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ):
        return self.log(
            level=LogLevel.CRITICAL,
            title=title,
            content=content,
            content_md=content_md,
            sys_exit=sys_exit,
            exit_code=exit_code,
            file=file,
            line=line,
            line_end=line_end,
            column=column,
            column_end=column_end,
            file_content=file_content,
            file_line=file_line,
            file_line_end=file_line_end,
            file_language=file_language,
            stack_up=stack_up + 1
        )

    def _submit_log(
        self,
        level: LogLevel | str | int,
        title: Stringable,
        content: Stringable = "",
        content_md: Stringable = "",
        file: Stringable | None = None,
        line: int | None = None,
        line_end: int | None = None,
        column: int | None = None,
        column_end: int | None = None,
        file_content: Stringable | None = None,
        file_line: int | None = None,
        file_line_end: int | None = None,
        file_language: str | None = None,
        stack_up: int = 0,
    ):
        level_name = self._get_level_name(level)
        level = self._level[level_name]
        sig = self._get_sig(stack_up=stack_up + 1)
        admo_content = [sig, "–" * 50, content_md or content]
        admo = _mdit.element.admonition(
            type=level.style.admo_class,
            title=title,
            content=admo_content,
            dropdown=True,
            opened=not level.style.dropdown,
        )
        list_idx = self._doc.current_section.body["logs"].content.content.append(
            content=admo, conditions=[level_name]
        )
        # Only print logs for realtime levels, except for when in GitHub Actions and debugging is enabled,
        # in which case all non-realtime logs are printed as debug messages.
        if level_name not in self._realtime_levels and not (self._github and self._github_debug):
            return
        list_num = list_idx + 1
        if not self._github:
            indent = " " * (len(str(list_num)) + 2)  # add 2 for ". "
            admo_ansi = "\n".join([f"{indent}{line}" for line in admo.source(target="ansi").splitlines()]).strip()
            self._print(f"{list_num}. {admo_ansi}\n")
            return
        # In GitHub
        title = f"{list_num}. {str(title)}"
        if level.style.gh_title_style:
            title = _sgr.element.inline(text=title, **level.style.gh_title_style.dict)
        if level.style.gh_title_prefix:
            title = f"{level.style.gh_title_prefix} {title}"
        content = str(content)
        if level_name in self._realtime_levels:
            annotation_type = self._get_github_annotation_type(level.level)
            if annotation_type:
                log_content = _actionman.log.annotation(
                    typ=annotation_type,
                    message=content,
                    title=title,
                    filename=file,
                    line_start=line,
                    line_end=line_end,
                    column_start=column,
                    column_end=column_end,
                    print_=False,
                )
            else:
                log_content = content
            output = _actionman.log.group(
                title=title,
                details=f"{sig.source(target="ansi")}\n{'–'*50}\n{log_content}",
                print_=False,
            )
        else:
            output = "\n".join(
                _actionman.log.debug(message=line, print_=False)
                for line in ["="*50, title, sig, *content.splitlines(), "="*50]
            )
        self._print(output)
        return

    def _get_sig(self, stack_up: int = 0) -> _mdit.InlineMDContainer:
        timestamp = _datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caller = self._get_caller_name(stack_up=stack_up + 1)
        return _mdit.inline_container(
            self._emoji_time,
            " ",
            _mdit.element.code_span(timestamp),
            " | ",
            self._emoji_caller,
            " ",
            _mdit.element.code_span(caller),
        )

    @staticmethod
    def _get_level_name(level: str | int | LogLevel) -> str:
        if isinstance(level, LogLevel):
            return level.name.lower()
        if isinstance(level, int):
            return LogLevel(level).name.lower()
        return level

    @staticmethod
    def _get_level_enum(level: str | int | LogLevel) -> LogLevel:
        if isinstance(level, LogLevel):
            return level
        if isinstance(level, int):
            return LogLevel(level)
        return LogLevel[level.upper()]

    @staticmethod
    def _print(text: str):
        # Flush the standard output and error streams to ensure the text is printed immediately
        # and not buffered in between other print statements (e.g. tracebacks).
        _sys.stdout.flush()
        _sys.stderr.flush()
        print(text, flush=True)
        return

    @staticmethod
    def _get_open_exception():
        exception = sys.exc_info()[1]
        if not exception:
            return
        name = exception.__class__.__name__
        traceback = _traceback.format_exc()
        return name, exception, traceback

    @staticmethod
    def _get_github_annotation_type(level: LogLevel) -> Literal["notice", "warning", "error"] | None:
        mapping = {
            LogLevel.NOTICE: "notice",
            LogLevel.WARNING: "warning",
            LogLevel.ERROR: "error",
            LogLevel.CRITICAL: "error",
        }
        return mapping[level] if level in mapping else None

    @staticmethod
    def _get_caller_name(stack_up: int = 0) -> str:
        stack = _inspect.stack()
        # The caller is the second element in the stack list
        caller_frame = stack[2 + stack_up]
        module = _inspect.getmodule(caller_frame[0])
        module_name = module.__name__ if module else "<module>"
        # Get the function or method name
        func_name = caller_frame.function
        # Combine them to get a fully qualified name
        fully_qualified_name = f"{module_name}.{func_name}"
        return fully_qualified_name
