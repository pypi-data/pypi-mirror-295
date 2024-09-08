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


class InvalidateSignInCodes(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``187``
        - ID: ``CA8AE8BA``

    Parameters:
        codes (List of ``str``):
            N/A

    Returns:
        ``bool``
    """

    __slots__: List[str] = ["codes"]

    ID = 0xca8ae8ba
    QUALNAME = "functions.account.InvalidateSignInCodes"

    def __init__(self, *, codes: List[str]) -> None:
        self.codes = codes  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvalidateSignInCodes":
        # No flags
        
        codes = TLObject.read(b, String)
        
        return InvalidateSignInCodes(codes=codes)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.codes, String))
        
        return b.getvalue()
