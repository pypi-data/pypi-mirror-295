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

from disnake.ext.commands import Cog
from disnake.ext.commands.common_bot_base import CommonBotBase

import disnake

from .callback import component_callback, modal_callback
from .extension import _patched_Cog__new__, _patched_Cog_eject
from .manager import InteractionsManager

__all__ = (
    "component_callback",
    "modal_callback",
    "setup",
)


def setup(bot: CommonBotBase) -> InteractionsManager:
    disnake.component_callback = component_callback
    disnake.modal_callback = modal_callback
    Cog.__new__ = _patched_Cog__new__
    Cog._eject = _patched_Cog_eject
    return InteractionsManager(bot)
