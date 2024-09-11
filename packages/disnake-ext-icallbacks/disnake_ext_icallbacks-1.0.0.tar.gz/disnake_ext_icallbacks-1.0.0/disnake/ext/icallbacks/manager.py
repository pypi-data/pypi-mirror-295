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

import re
from functools import partial
from typing import Callable, cast

from disnake.ext.commands.common_bot_base import CommonBotBase

from disnake import MessageInteraction, ModalInteraction

from .callback import InteractionCallback, component_callback, modal_callback
from .utils import AsyncCallable

__all__ = (
    "InjectedBotBase",
    "InteractionsManager",
)


class InjectedBotBase(CommonBotBase):
    """A semi-stub class for type hinting."""

    better_interactions: "InteractionsManager"
    """The interactions manager for the bot."""

    def component_callback(self, *custom_id: str | re.Pattern) -> Callable[[AsyncCallable], InteractionCallback]:
        """Listen for a component interaction with the specified custom ID."""

    def modal_callback(self, *custom_id: str | re.Pattern) -> Callable[[AsyncCallable], InteractionCallback]:
        """Listen for a modal interaction with the specified custom ID."""


class InteractionsManager:
    """The manager for the better interactions extension."""

    def __init__(self, bot: CommonBotBase) -> None:
        # cast the bot for type hinting
        bot = cast(InjectedBotBase, bot)

        self.bot = bot
        self._component_callbacks = {}
        self._regex_component_callbacks = {}
        self._modal_callback = {}
        self._regex_modal_callbacks = {}

        # inject the manager into the bot
        self.bot.better_interactions = self

        # define the component and modal callback decorators
        def _component_callback(
            bot: InjectedBotBase, *custom_id: str | re.Pattern
        ) -> Callable[[AsyncCallable], InteractionCallback]:
            def wrapper(func: AsyncCallable) -> InteractionCallback:
                result = component_callback(*custom_id)(func)
                bot.better_interactions.add_component_callback(result)
                return result

            return wrapper

        def _modal_callback(
            bot: InjectedBotBase, *custom_id: str | re.Pattern
        ) -> Callable[[AsyncCallable], InteractionCallback]:
            def wrapper(func: AsyncCallable) -> InteractionCallback:
                result = modal_callback(*custom_id)(func)
                bot.better_interactions.add_modal_callback(result)
                return result

            return wrapper

        # inject the component and modal callback decorators
        self.bot.component_callback = partial(_component_callback, bot)
        self.bot.modal_callback = partial(_modal_callback, bot)

        # register listeners for interactions
        self.bot.add_listener(self._dispatch_interaction, "on_message_interaction")
        self.bot.add_listener(self._dispatch_interaction, "on_modal_submit")

    def _add_interaction_callback(self, callback: InteractionCallback, type_: str) -> None:
        """Register an interaction callback.

        :param callback: The callback to register.
        :type callback: InteractionCallback
        :param type_: The type of interaction to register.
        :type type_: str
        :raises ValueError: If the type is not `component` or `modal`.
        :raises ValueError: If there are multiple callbacks for the same custom ID.
        """
        if type_ not in ["component", "modal"]:
            raise ValueError("Invalid type! Must be either `component` or `modal`")
        if type_ == "component":
            callbacks = [self._regex_component_callbacks, self._component_callbacks]
        elif type_ == "modal":
            callbacks = [self._regex_modal_callbacks, self._modal_callback]
        for listener in callback.listeners:
            if isinstance(listener, re.Pattern):
                if listener in callbacks[0]:
                    raise ValueError(f"Duplicate {type_.capitalize()}! Multiple {type_} callbacks for `{listener}`")
                callbacks[0][listener] = callback
            else:
                if listener in callbacks[1]:
                    raise ValueError(f"Duplicate {type_.capitalize()}! Multiple {type_} callbacks for `{listener}`")
                callbacks[1][listener] = callback

    def add_component_callback(self, callback: InteractionCallback) -> None:
        """Register a component interaction callback.

        :param callback: The callback to register.
        :type callback: InteractionCallback
        """
        self._add_interaction_callback(callback, "component")

    def add_modal_callback(self, callback: InteractionCallback) -> None:
        """Register a modal interaction callback.

        :param callback: The callback to register.
        :type callback: InteractionCallback
        """
        self._add_interaction_callback(callback, "modal")

    def remove_interaction_callback(self, name: str) -> None:
        """Remove an interaction callback by its name.

        :param name: The name of the callback to remove.
        :type name: str
        """
        callback_ls = [
            self._component_callbacks,
            self._regex_component_callbacks,
            self._modal_callback,
            self._regex_modal_callbacks,
        ]
        for callbacks in callback_ls:
            remove = []
            for k, v in callbacks.items():
                if v.name == name:
                    remove.append(k)
            for k in remove:
                del callbacks[k]

    async def _dispatch_interaction(self, interaction: MessageInteraction | ModalInteraction) -> None:
        """Dispatch an interaction to the correct callback.

        :param interaction: The interaction to dispatch.
        :type interaction: MessageInteraction
        """
        if isinstance(interaction, MessageInteraction):
            callbacks = self._component_callbacks
            regex_callbacks = self._regex_component_callbacks
        elif isinstance(interaction, ModalInteraction):
            callbacks = self._modal_callback
            regex_callbacks = self._regex_modal_callbacks

        callback = callbacks.get(interaction.data.custom_id)
        if not callback:
            for regex, cb in regex_callbacks.items():
                if regex.match(interaction.data.custom_id):
                    callback = cb
                    break

        if callback:
            await callback.callback(interaction)
