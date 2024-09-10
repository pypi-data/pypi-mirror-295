# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


# Regex filter.
class DivInputFilterRegex(BaseDiv):

    def __init__(
        self, *,
        type: str = "regex",
        pattern: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            pattern=pattern,
            **kwargs,
        )

    type: str = Field(default="regex")
    pattern: typing.Union[Expr, str] = Field(
        description=(
            "A regular expression (pattern) that the input value must "
            "match."
        ),
    )


DivInputFilterRegex.update_forward_refs()
