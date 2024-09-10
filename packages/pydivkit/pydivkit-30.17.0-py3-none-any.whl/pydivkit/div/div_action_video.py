# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


# Controls given video.
class DivActionVideo(BaseDiv):

    def __init__(
        self, *,
        type: str = "video",
        action: typing.Optional[typing.Union[Expr, DivActionVideoAction]] = None,
        id: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            action=action,
            id=id,
            **kwargs,
        )

    type: str = Field(default="video")
    action: typing.Union[Expr, DivActionVideoAction] = Field(
        description=(
            "Defines video action:`start` - play if it is ready or plans "
            "to play when videobecomes ready;`pause` - pauses video "
            "playback."
        ),
    )
    id: typing.Union[Expr, str] = Field(
        description="Video identifier.",
    )


class DivActionVideoAction(str, enum.Enum):
    START = "start"
    PAUSE = "pause"


DivActionVideo.update_forward_refs()
