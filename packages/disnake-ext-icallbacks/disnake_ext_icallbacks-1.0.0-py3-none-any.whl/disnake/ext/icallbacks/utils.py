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

import inspect
import re
from typing import Callable, Coroutine

__all__ = (
    "AsyncCallable",
    "custom_ids_validator",
)

AsyncCallable = Callable[..., Coroutine]


def custom_ids_validator(custom_ids: tuple[str | re.Pattern]) -> None:
    """Validate the custom IDs.

    :param custom_ids: The custom IDs to validate.
    :type custom_ids: tuple[str  |  re.Pattern]
    :raises ValueError: If the custom IDs are not all strings or regex patterns.
    """
    unpacked_custom_id = []
    for c in custom_ids:
        if inspect.isgenerator(c):
            unpacked_custom_id += list(c)
        else:
            unpacked_custom_id.append(c)
    if not (
        all(isinstance(i, re.Pattern) for i in unpacked_custom_id)
        or all(isinstance(i, str) for i in unpacked_custom_id)
    ):
        raise ValueError("All custom IDs be either a string or a regex pattern, not a mix of both.")
