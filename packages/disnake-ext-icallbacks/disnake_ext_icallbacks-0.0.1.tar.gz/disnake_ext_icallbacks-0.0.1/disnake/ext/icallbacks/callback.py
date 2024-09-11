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

import asyncio
import re
from dataclasses import dataclass
from typing import Callable

from .utils import AsyncCallable, custom_ids_validator

__all__ = (
    "InteractionCallback",
    "component_callback",
    "modal_callback",
)


@dataclass
class InteractionCallback:
    name: str
    callback: AsyncCallable
    listeners: list[str | re.Pattern]


def component_callback(*custom_id: str | re.Pattern) -> Callable[[AsyncCallable], InteractionCallback]:
    """Listen for a component interaction with the specified custom ID.

    :param custom_id: The custom ID to listen for.
    :type custom_id: str | re.Pattern
    :raise ValueError: If the callback is not a coroutine.
    :raise ValueError: If custom ID is not all strings or regex patterns.
    :return: The callback decorator.
    :rtype: Callable[[AsyncCallable], InteractionCallback]
    """

    def wrapper(func: AsyncCallable) -> InteractionCallback:
        resolved_custom_id = custom_id or [func.__name__]

        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Callback must be coroutines")

        return InteractionCallback(
            name=f"ComponentCallback::{resolved_custom_id}", callback=func, listeners=resolved_custom_id
        )

    custom_ids_validator(custom_id)
    return wrapper


def modal_callback(*custom_id: str | re.Pattern) -> Callable[[AsyncCallable], InteractionCallback]:
    """Listen for a modal interaction with the specified custom ID.

    :param custom_id: The custom ID to listen for.
    :type custom_id: str | re.Pattern
    :raise ValueError: If the callback is not a coroutine.
    :raise ValueError: If custom ID is not all strings or regex patterns.
    :return: The callback decorator.
    :rtype: Callable[[AsyncCallable], InteractionCallback]
    """

    def wrapper(func: AsyncCallable) -> InteractionCallback:
        resolved_custom_id = custom_id or [func.__name__]

        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Callback must be coroutines")

        return InteractionCallback(
            name=f"ModalCallback::{resolved_custom_id}", callback=func, listeners=resolved_custom_id
        )

    custom_ids_validator(custom_id)
    return wrapper
