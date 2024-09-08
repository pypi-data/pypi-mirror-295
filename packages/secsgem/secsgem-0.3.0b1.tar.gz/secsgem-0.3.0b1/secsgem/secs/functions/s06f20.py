#####################################################################
# s06f20.py
#
# (c) Copyright 2021, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################
"""Class for stream 06 function 20."""

from secsgem.secs.data_items import V
from secsgem.secs.functions.base import SecsStreamFunction


class SecsS06F20(SecsStreamFunction):
    """individual report data.

    Args:
        value: parameters for this function (see example)

    Examples:
        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F20
        [
            V: L/BOOLEAN/U1/U2/U4/U8/I1/I2/I4/I8/F4/F8/A/B
            ...
        ]

        >>> import secsgem.secs
        >>> secsgem.secs.functions.SecsS06F20(["ASD", 1337])
        S6F20
          <L [2]
            <A "ASD">
            <U2 1337 >
          > .

    Data Items:
        - :class:`V <secsgem.secs.data_items.V>`

    """

    _stream = 6
    _function = 20

    _data_format = [V]

    _to_host = True
    _to_equipment = False

    _has_reply = False
    _is_reply_required = False

    _is_multi_block = True
