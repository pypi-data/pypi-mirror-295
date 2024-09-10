# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing

from pydivkit.core import BaseDiv, Expr, Field

from . import (
    div_animation_direction, div_animation_interpolator, div_typed_value,
)


# Starts specified animator
class DivActionAnimatorStart(BaseDiv):

    def __init__(
        self, *,
        type: str = "animator_start",
        animator_id: typing.Optional[typing.Union[Expr, str]] = None,
        direction: typing.Optional[typing.Union[Expr, div_animation_direction.DivAnimationDirection]] = None,
        duration: typing.Optional[typing.Union[Expr, int]] = None,
        end_value: typing.Optional[div_typed_value.DivTypedValue] = None,
        interpolator: typing.Optional[typing.Union[Expr, div_animation_interpolator.DivAnimationInterpolator]] = None,
        repeat_count: typing.Optional[typing.Union[Expr, int]] = None,
        start_delay: typing.Optional[typing.Union[Expr, int]] = None,
        start_value: typing.Optional[div_typed_value.DivTypedValue] = None,
        **kwargs: typing.Any,
    ):
        super().__init__(
            type=type,
            animator_id=animator_id,
            direction=direction,
            duration=duration,
            end_value=end_value,
            interpolator=interpolator,
            repeat_count=repeat_count,
            start_delay=start_delay,
            start_value=start_value,
            **kwargs,
        )

    type: str = Field(default="animator_start")
    animator_id: typing.Union[Expr, str] = Field(
        description="The identifier of the animator being started.",
    )
    direction: typing.Optional[typing.Union[Expr, div_animation_direction.DivAnimationDirection]] = Field(
        description=(
            "Animation direction. This property sets whether an "
            "animation should play forward,backward, or alternate back "
            "and forth between playing the sequence forward andbackward."
        ),
    )
    duration: typing.Optional[typing.Union[Expr, int]] = Field(
        description="Animation duration in milliseconds.",
    )
    end_value: typing.Optional[div_typed_value.DivTypedValue] = Field(
        description="Overrides value that will be set at the end of animation.",
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
    start_value: typing.Optional[div_typed_value.DivTypedValue] = Field(
        description=(
            "Overrides value that will be set at the start of animation."
        ),
    )


DivActionAnimatorStart.update_forward_refs()
