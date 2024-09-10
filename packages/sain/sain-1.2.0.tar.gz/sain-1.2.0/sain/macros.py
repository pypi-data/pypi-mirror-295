# BSD 3-Clause License
#
# Copyright (c) 2022-Present, nxtlo
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""A module that contains useful decorators for marking objects.

It appends useful messages to warn at runtime and to the object documentation.
"""

from __future__ import annotations

__all__ = ("deprecated", "unimplemented", "todo", "doc", "unsafe")

import functools
import inspect
import typing
import warnings

if typing.TYPE_CHECKING:
    import collections.abc as collections

    import _typeshed

    P = typing.ParamSpec("P")
    U = typing.TypeVar("U")
    Read = _typeshed.FileDescriptorOrPath


@typing.final
class Error(RuntimeWarning):
    """A runtime warning that is used as the category warning for all the markers."""

    __slots__ = ("message",)

    def __init__(self, message: str | None = None) -> None:
        self.message = message


def _warn(msg: str, stacklevel: int = 2) -> None:
    warnings.warn(message=msg, stacklevel=stacklevel, category=Error)


def unsafe(fn: collections.Callable[P, U]) -> collections.Callable[P, U]:
    """Mark a function as unsafe.

    The caller of the decorated function is responsible for the undefined behavior if occurred.
    """
    m = "\n# Safety ⚠️\nCalling this method on `None` is considered [undefined behavior](https://en.wikipedia.org/wiki/Undefined_behavior)."
    if fn.__doc__:
        # append this message to an existing document.
        fn.__doc__ = inspect.cleandoc(fn.__doc__) + f"\n{m}"
    else:
        fn.__doc__ = m

    return fn


@functools.cache
def _obj_type(obj: type[typing.Any]) -> str:
    return "class" if inspect.isclass(obj) else "function"


def unstable(
    *, reason: typing.LiteralString = "none"
) -> collections.Callable[
    [collections.Callable[P, typing.Any]],
    collections.Callable[P, typing.NoReturn],
]:
    """A decorator that marks an internal object explicitly unstable.

    Unstable objects never run, even inside the standard library.

    Calling any object that is unstable will raise an `RuntimeError` exception.
    Also using this outside the library isn't allowed.

    Example
    -------
    ```py

    from sain.macros import unstable

    @unstable(reason = "none")
    def unstable_function() -> int:
        return -1

    if unstable_function():
        # never reachable

    ```
    """

    def decorator(
        obj: collections.Callable[P, U],
    ) -> collections.Callable[P, typing.NoReturn]:
        @functools.wraps(obj)
        def wrapper(*_args: P.args, **_kwargs: P.kwargs) -> typing.NoReturn:
            if obj.__doc__ != "__intrinsics__":
                # This has been used outside of the lib.
                raise RuntimeError(
                    "Stability attributes may not be used outside of the core library",
                )

            name = obj.__name__
            if name.startswith("_"):
                name = name.lstrip("_")

            raise RuntimeError(f"{_obj_type(obj)} `{name}` is not stable: {reason}")

        # idk why pyright doesn't know the type of wrapper.
        m = (
            f"\n# Stability ⚠️\nThis {_obj_type(obj)} is unstable, "
            "Calling it may result in failure or [undefined behavior](https://en.wikipedia.org/wiki/Undefined_behavior)."
        )
        if wrapper.__doc__:
            # append this message to an existing document.
            wrapper.__doc__ = inspect.cleandoc(wrapper.__doc__) + f"{m}"
        else:
            wrapper.__doc__ = m

        return wrapper

    return decorator


def deprecated(
    *,
    since: typing.Literal["CURRENT_VERSION"] | typing.LiteralString | None = None,
    removed_in: typing.LiteralString | None = None,
    use_instead: typing.LiteralString | None = None,
    hint: typing.LiteralString | None = None,
) -> collections.Callable[
    [collections.Callable[P, U]],
    collections.Callable[P, U],
]:
    """A decorator that marks a function as deprecated.

    An attempt to call the object that's marked will cause a runtime warn.

    Example
    -------
    ```py
    from sain import deprecated

    @deprecated(
        since = "1.0.0",
        removed_in ="3.0.0",
        use_instead = "UserImpl()",
        hint = "Hint for ux."
    )
    class User:
        ...

    user = User() # This will cause a warning at runtime.
    ```

    Parameters
    ----------
    since : `str`
        The version that the function was deprecated. the `CURRENT_VERSION` is used internally only.
    removed_in : `str | None`
        If provided, It will log when will the object will be removed in.
    use_instead : `str | None`
        If provided, This should be the alternative object name that should be used instead.
    hint: `str`
        An optional hint for the user.
    """

    def _create_message(obj: typing.Any) -> str:
        msg = f"{_obj_type(obj)} `{obj.__module__}.{obj.__name__}` is deprecated."

        if since is not None:
            if since == "CURRENT_VERSION":
                from sain import __version__ as _version

                msg += " since " + _version
            else:
                msg += " since " + since

        if removed_in:
            msg += f" Scheduled for removal in `{removed_in}`."

        if use_instead is not None:
            msg += f" Use `{use_instead}` instead."

        if hint:
            msg += f" Hint: {hint}"
        return msg

    def decorator(func: collections.Callable[P, U]) -> collections.Callable[P, U]:
        message = _create_message(func)

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> U:
            _warn(message)
            return func(*args, **kwargs)

        # idk why pyright doesn't know the type of wrapper.
        m = f"\n# Warning ⚠️\n{message}."
        if wrapper.__doc__:
            # append this message to an existing document.
            wrapper.__doc__ = inspect.cleandoc(wrapper.__doc__) + f"{m}"
        else:
            wrapper.__doc__ = m
        return wrapper

    return decorator


def todo(message: typing.LiteralString | None = None) -> typing.NoReturn:
    """A place holder that indicates unfinished code.

    Example
    -------
    ```py
    from sain import todo

    def from_json(payload: dict[str, int]) -> int:
        # Calling this function will raise `Error`.
        todo()
    ```

    Parameters
    ----------
    message : `str | None`
        Multiple optional arguments to pass if the error was raised.
    """
    raise Error(f"not yet implemented: {message}" if message else "not yet implemented")


def unimplemented(
    *,
    message: typing.LiteralString | None = None,
    available_in: typing.LiteralString | None = None,
) -> collections.Callable[
    [collections.Callable[P, U]],
    collections.Callable[P, U],
]:
    """A decorator that marks an object as unimplemented.

    An attempt to call the object that's marked will cause a runtime warn.

    Example
    -------
    ```py
    from sain import unimplemented

    @unimplemented("User object is not implemented yet.")
    class User:
        ...
    ```

    Parameters
    ----------
    message : `str | None`
        An optional message to be displayed when the function is called. Otherwise default message will be used.
    available_in : `str | None`
        If provided, This will be shown as what release this object be implemented.
    """

    def _create_message(obj: typing.Any) -> str:
        msg = (
            message
            or f"{_obj_type(obj)} `{obj.__module__}.{obj.__name__}` is not yet implemented."
        )  # noqa: W503

        if available_in:
            msg += f" Available in `{available_in}`."
        return msg

    def decorator(obj: collections.Callable[P, U]) -> collections.Callable[P, U]:
        message = _create_message(obj)

        @functools.wraps(obj)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> U:
            _warn(message)
            return obj(*args, **kwargs)

        # idk why pyright doesn't know the type of wrapper.
        m = f"\n# Warning ⚠️\n{message}."
        if wrapper.__doc__:
            # append this message to an existing document.
            wrapper.__doc__ = inspect.cleandoc(wrapper.__doc__) + f"{m}"
        else:
            wrapper.__doc__ = m
        return wrapper

    return decorator


def doc(
    path: Read,
) -> collections.Callable[
    [collections.Callable[P, U]],
    collections.Callable[P, U],
]:
    """Set `path` to be the object's documentation.

    Example
    -------
    ```py
    from sain import doc
    from pathlib import Path

    @doc(Path("../README.md"))
    class User:

        @doc("bool.html")
        def bool_docs() -> None:
            ...
    ```

    Parameters
    ----------
    path: `type[int] | type[str] | type[bytes] | type[PathLike[str]] | type[PathLike[bytes]]`
        The path to read the content from.
    """

    def decorator(f: collections.Callable[P, U]) -> collections.Callable[P, U]:
        with open(path, "r") as file:
            f.__doc__ = file.read()

        @functools.wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> U:
            return f(*args, **kwargs)

        return wrapper

    return decorator
