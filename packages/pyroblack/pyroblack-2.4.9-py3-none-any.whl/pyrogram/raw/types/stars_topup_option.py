#  pyroblack - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#  #  Copyright (C) 2024-present eyMarv <https://github.com/eyMarv>
#
#  This file is part of pyroblack.
#
#  pyroblack is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  pyroblack is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with pyroblack.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class StarsTopupOption(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarsTopupOption`.

    Details:
        - Layer: ``187``
        - ID: ``BD915C0``

    Parameters:
        stars (``int`` ``64-bit``):
            N/A

        currency (``str``):
            N/A

        amount (``int`` ``64-bit``):
            N/A

        extended (``bool``, *optional*):
            N/A

        store_product (``str``, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            payments.GetStarsTopupOptions
    """

    __slots__: List[str] = ["stars", "currency", "amount", "extended", "store_product"]

    ID = 0xbd915c0
    QUALNAME = "types.StarsTopupOption"

    def __init__(self, *, stars: int, currency: str, amount: int, extended: Optional[bool] = None, store_product: Optional[str] = None) -> None:
        self.stars = stars  # long
        self.currency = currency  # string
        self.amount = amount  # long
        self.extended = extended  # flags.1?true
        self.store_product = store_product  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsTopupOption":
        
        flags = Int.read(b)
        
        extended = True if flags & (1 << 1) else False
        stars = Long.read(b)
        
        store_product = String.read(b) if flags & (1 << 0) else None
        currency = String.read(b)
        
        amount = Long.read(b)
        
        return StarsTopupOption(stars=stars, currency=currency, amount=amount, extended=extended, store_product=store_product)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.extended else 0
        flags |= (1 << 0) if self.store_product is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.stars))
        
        if self.store_product is not None:
            b.write(String(self.store_product))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        return b.getvalue()
