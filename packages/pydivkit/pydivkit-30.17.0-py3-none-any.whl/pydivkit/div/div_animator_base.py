# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import div_action, div_animation_direction, div_animation_interpolator


class DivAnimatorBase(BaseDiv):

    def __init__(
        self, *,
        cancel_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        direction: typing.Optional[typing.Union[Expr, div_animation_direction.DivAnimationDirection]] = None,
        duration: typing.Optional[typing.Union[Expr, int]] = None,
        end_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        id: typing.Optional[typing.Union[Expr, str]] = None,
        interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = None,
        repeat_count: typing.Optional[typing.Union[Expr, int]] = None,
        start_delay: typing.Optional[typing.Union[Expr, int]] = None,
        variable_name: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            cancel_actions=cancel_actions,
            direction=direction,
            duration=duration,
            end_actions=end_actions,
            id=id,
            interpolator=interpolator,
            repeat_count=repeat_count,
            start_delay=start_delay,
            variable_name=variable_name,
            **kwargs,
        )

    cancel_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = Field(
        description=(
            "Actions performed when the animator is cancelled. For "
            "example, when an actionwith `animator_stop` type is "
            "received"
        ),
    )
    direction: typing.Optional[typing.Union[Expr, div_animation_direction.DivAnimationDirection]] = Field(
        description=(
            "Animation direction. This property sets whether an "
            "animation should play forward,backward, or alternate back "
            "and forth between playing the sequence forward andbackward."
        ),
    )
    duration: typing.Union[Expr, int] = Field(
        description="Animation duration in milliseconds.",
    )
    end_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = Field(
        description="Actions performed when the animator completes animation.",
    )
    id: typing.Union[Expr, str] = Field(
        description="Animator identificator",
    )
    interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = Field(
        description="Interpolation function.",
    )
    repeat_count: typing.Optional[typing.Union[Expr, int]] = Field(
        description=(
            "The number of times the animation will repeat before it "
            "finishes. `0` enablesinfinite repeats."
        ),
    )
    start_delay: typing.Optional[typing.Union[Expr, int]] = Field(
        description="Animation start delay in milliseconds.",
    )
    variable_name: typing.Union[Expr, str] = Field(
        description="Name of the variable being animated.",
    )


DivAnimatorBase.update_forward_refs()
