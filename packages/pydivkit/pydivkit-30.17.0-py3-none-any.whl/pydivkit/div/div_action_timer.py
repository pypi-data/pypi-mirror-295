# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field


# Controls the timer.
class DivActionTimer(BaseDiv):

    def __init__(
        self, *,
        type: str = "timer",
        action: typing.Optional[typing.Union[Expr, DivActionTimerAction]] = None,
        id: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            action=action,
            id=id,
            **kwargs,
        )

    type: str = Field(default="timer")
    action: typing.Union[Expr, DivActionTimerAction] = Field(
        description=(
            "Defines timer action:`start`- starts the timer when "
            "stopped, does onStartaction;`stop`- stops timer, resets the "
            "time, does onEnd action;`pause`- pausetimer, preserves "
            "current time;`resume`- starts timer from paused state, "
            "restoressaved time;`cancel`- stops timer, resets its state, "
            "does onInterruptaction;`reset`- cancels timer and starts it "
            "again."
        ),
    )
    id: typing.Union[Expr, str] = Field(
        description="Timer identifier.",
    )


class DivActionTimerAction(str, enum.Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    CANCEL = "cancel"
    RESET = "reset"


DivActionTimer.update_forward_refs()
