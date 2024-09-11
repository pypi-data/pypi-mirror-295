# pylint: disable=invalid-name, protected-access
"""
MIT License

Copyright (c) 2024 ItsRqtl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from functools import partial

from disnake.ext.commands import Cog

from .callback import InteractionCallback

__all__ = (
    "_patched_Cog__new__",
    "_patched_Cog_eject",
)

_Cog__new__ = Cog.__new__
_Cog_eject = Cog._eject


def _patched_Cog__new__(cls, *args, **kwargs):
    self = _Cog__new__(cls, *args, **kwargs)
    interaction_callbacks = {}
    for base in reversed(cls.__mro__):
        for elem, value in base.__dict__.items():
            if elem in interaction_callbacks:
                del interaction_callbacks[elem]

            if isinstance(value, InteractionCallback):
                interaction_callbacks[elem] = value.name
                value.callback = partial(value.callback, self)
                if value.name.startswith("ModalCallback::"):
                    args[0].better_interactions.add_modal_callback(value)
                elif value.name.startswith("ComponentCallback::"):
                    args[0].better_interactions.add_component_callback(value)
    self._interaction_callbacks = list(interaction_callbacks.values())
    return self


def _patched_Cog_eject(self, bot):
    for i in self._interaction_callbacks:
        bot.better_interactions.remove_interaction_callback(i)
    _Cog_eject(self, bot)
