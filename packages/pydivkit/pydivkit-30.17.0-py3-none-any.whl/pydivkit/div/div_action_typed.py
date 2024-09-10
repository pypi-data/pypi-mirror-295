# Generated code. Do not modify.
# flake8: noqa: F401, F405, F811

from __future__ import annotations

import enum
import typing
from typing import Union

from pydivkit.core import BaseDiv, Expr, Field

from . import (
    div_action_animator_start, div_action_animator_stop,
    div_action_array_insert_value, div_action_array_remove_value,
    div_action_array_set_value, div_action_clear_focus,
    div_action_copy_to_clipboard, div_action_dict_set_value,
    div_action_focus_element, div_action_set_variable, div_action_show_tooltip,
    div_action_timer, div_action_video,
)


DivActionTyped = Union[
    div_action_animator_start.DivActionAnimatorStart,
    div_action_animator_stop.DivActionAnimatorStop,
    div_action_array_insert_value.DivActionArrayInsertValue,
    div_action_array_remove_value.DivActionArrayRemoveValue,
    div_action_array_set_value.DivActionArraySetValue,
    div_action_clear_focus.DivActionClearFocus,
    div_action_copy_to_clipboard.DivActionCopyToClipboard,
    div_action_dict_set_value.DivActionDictSetValue,
    div_action_focus_element.DivActionFocusElement,
    div_action_set_variable.DivActionSetVariable,
    div_action_show_tooltip.DivActionShowTooltip,
    div_action_timer.DivActionTimer,
    div_action_video.DivActionVideo,
]
