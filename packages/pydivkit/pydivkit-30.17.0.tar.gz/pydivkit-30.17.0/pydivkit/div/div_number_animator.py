# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import div_action, div_animation_direction, div_animation_interpolator


# Number animator.
class DivNumberAnimator(BaseDiv):

    def __init__(
        self, *,
        type: str = "number_animator",
        cancel_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        direction: typing.Optional[typing.Union[Expr, div_animation_direction.DivAnimationDirection]] = None,
        duration: typing.Optional[typing.Union[Expr, int]] = None,
        end_actions: typing.Optional[typing.Sequence[div_action.DivAction]] = None,
        end_value: typing.Optional[typing.Union[Expr, float]] = None,
        id: typing.Optional[typing.Union[Expr, str]] = None,
        interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = None,
        repeat_count: typing.Optional[typing.Union[Expr, int]] = None,
        start_delay: typing.Optional[typing.Union[Expr, int]] = None,
        start_value: typing.Optional[typing.Union[Expr, float]] = None,
        variable_name: typing.Optional[typing.Union[Expr, str]] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            cancel_actions=cancel_actions,
            direction=direction,
            duration=duration,
            end_actions=end_actions,
            end_value=end_value,
            id=id,
            interpolator=interpolator,
            repeat_count=repeat_count,
            start_delay=start_delay,
            start_value=start_value,
            variable_name=variable_name,
            **kwargs,
        )

    type: str = Field(default="number_animator")
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
    end_value: typing.Union[Expr, float] = Field(
        description="Value that will be set at the end of animation.",
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
    start_value: typing.Optional[typing.Union[Expr, float]] = Field(
        description=(
            "Value that will be set at the start of animation. Can be "
            "omitted, in which casecurrent value of the variable will be "
            "used."
        ),
    )
    variable_name: typing.Union[Expr, str] = Field(
        description="Name of the variable being animated.",
    )


DivNumberAnimator.update_forward_refs()
