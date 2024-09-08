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


class StarsSubscription(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarsSubscription`.

    Details:
        - Layer: ``187``
        - ID: ``538ECF18``

    Parameters:
        id (``str``):
            N/A

        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        until_date (``int`` ``32-bit``):
            N/A

        pricing (:obj:`StarsSubscriptionPricing <pyrogram.raw.base.StarsSubscriptionPricing>`):
            N/A

        canceled (``bool``, *optional*):
            N/A

        can_refulfill (``bool``, *optional*):
            N/A

        missing_balance (``bool``, *optional*):
            N/A

        chat_invite_hash (``str``, *optional*):
            N/A

    """

    __slots__: List[str] = ["id", "peer", "until_date", "pricing", "canceled", "can_refulfill", "missing_balance", "chat_invite_hash"]

    ID = 0x538ecf18
    QUALNAME = "types.StarsSubscription"

    def __init__(self, *, id: str, peer: "raw.base.Peer", until_date: int, pricing: "raw.base.StarsSubscriptionPricing", canceled: Optional[bool] = None, can_refulfill: Optional[bool] = None, missing_balance: Optional[bool] = None, chat_invite_hash: Optional[str] = None) -> None:
        self.id = id  # string
        self.peer = peer  # Peer
        self.until_date = until_date  # int
        self.pricing = pricing  # StarsSubscriptionPricing
        self.canceled = canceled  # flags.0?true
        self.can_refulfill = can_refulfill  # flags.1?true
        self.missing_balance = missing_balance  # flags.2?true
        self.chat_invite_hash = chat_invite_hash  # flags.3?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsSubscription":
        
        flags = Int.read(b)
        
        canceled = True if flags & (1 << 0) else False
        can_refulfill = True if flags & (1 << 1) else False
        missing_balance = True if flags & (1 << 2) else False
        id = String.read(b)
        
        peer = TLObject.read(b)
        
        until_date = Int.read(b)
        
        pricing = TLObject.read(b)
        
        chat_invite_hash = String.read(b) if flags & (1 << 3) else None
        return StarsSubscription(id=id, peer=peer, until_date=until_date, pricing=pricing, canceled=canceled, can_refulfill=can_refulfill, missing_balance=missing_balance, chat_invite_hash=chat_invite_hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.canceled else 0
        flags |= (1 << 1) if self.can_refulfill else 0
        flags |= (1 << 2) if self.missing_balance else 0
        flags |= (1 << 3) if self.chat_invite_hash is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.id))
        
        b.write(self.peer.write())
        
        b.write(Int(self.until_date))
        
        b.write(self.pricing.write())
        
        if self.chat_invite_hash is not None:
            b.write(String(self.chat_invite_hash))
        
        return b.getvalue()
