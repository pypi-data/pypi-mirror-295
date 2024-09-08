#####################################################################
# dvval.py
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
"""DVVAL data item."""

from secsgem.secs import variables

from .base import DataItemBase


class DVVAL(DataItemBase):
    """Data value.

    :Types:
       - :class:`Array <secsgem.secs.variables.Array>`
       - :class:`Boolean <secsgem.secs.variables.Boolean>`
       - :class:`U1 <secsgem.secs.variables.U1>`
       - :class:`U2 <secsgem.secs.variables.U2>`
       - :class:`U4 <secsgem.secs.variables.U4>`
       - :class:`U8 <secsgem.secs.variables.U8>`
       - :class:`I1 <secsgem.secs.variables.I1>`
       - :class:`I2 <secsgem.secs.variables.I2>`
       - :class:`I4 <secsgem.secs.variables.I4>`
       - :class:`I8 <secsgem.secs.variables.I8>`
       - :class:`F4 <secsgem.secs.variables.F4>`
       - :class:`F8 <secsgem.secs.variables.F8>`
       - :class:`String <secsgem.secs.variables.String>`
       - :class:`Binary <secsgem.secs.variables.Binary>`

    **Used In Function**
        - :class:`SecsS06F08 <secsgem.secs.functions.SecsS06F08>`

    """

    __type__ = variables.Dynamic
    __allowedtypes__ = [
        variables.Array,
        variables.Boolean,
        variables.U1,
        variables.U2,
        variables.U4,
        variables.U8,
        variables.I1,
        variables.I2,
        variables.I4,
        variables.I8,
        variables.F4,
        variables.F8,
        variables.String,
        variables.Binary,
    ]
