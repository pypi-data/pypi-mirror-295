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


class StarsRevenueStatus(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.StarsRevenueStatus`.

    Details:
        - Layer: ``187``
        - ID: ``79342946``

    Parameters:
        current_balance (``int`` ``64-bit``):
            N/A

        available_balance (``int`` ``64-bit``):
            N/A

        overall_revenue (``int`` ``64-bit``):
            N/A

        withdrawal_enabled (``bool``, *optional*):
            N/A

        next_withdrawal_at (``int`` ``32-bit``, *optional*):
            N/A

    """

    __slots__: List[str] = ["current_balance", "available_balance", "overall_revenue", "withdrawal_enabled", "next_withdrawal_at"]

    ID = 0x79342946
    QUALNAME = "types.StarsRevenueStatus"

    def __init__(self, *, current_balance: int, available_balance: int, overall_revenue: int, withdrawal_enabled: Optional[bool] = None, next_withdrawal_at: Optional[int] = None) -> None:
        self.current_balance = current_balance  # long
        self.available_balance = available_balance  # long
        self.overall_revenue = overall_revenue  # long
        self.withdrawal_enabled = withdrawal_enabled  # flags.0?true
        self.next_withdrawal_at = next_withdrawal_at  # flags.1?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRevenueStatus":
        
        flags = Int.read(b)
        
        withdrawal_enabled = True if flags & (1 << 0) else False
        current_balance = Long.read(b)
        
        available_balance = Long.read(b)
        
        overall_revenue = Long.read(b)
        
        next_withdrawal_at = Int.read(b) if flags & (1 << 1) else None
        return StarsRevenueStatus(current_balance=current_balance, available_balance=available_balance, overall_revenue=overall_revenue, withdrawal_enabled=withdrawal_enabled, next_withdrawal_at=next_withdrawal_at)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.withdrawal_enabled else 0
        flags |= (1 << 1) if self.next_withdrawal_at is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.current_balance))
        
        b.write(Long(self.available_balance))
        
        b.write(Long(self.overall_revenue))
        
        if self.next_withdrawal_at is not None:
            b.write(Int(self.next_withdrawal_at))
        
        return b.getvalue()
