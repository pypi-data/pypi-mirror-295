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


class UpdateMessageExtendedMedia(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.Update`.

    Details:
        - Layer: ``187``
        - ID: ``D5A41724``

    Parameters:
        peer (:obj:`Peer <pyrogram.raw.base.Peer>`):
            N/A

        msg_id (``int`` ``32-bit``):
            N/A

        extended_media (List of :obj:`MessageExtendedMedia <pyrogram.raw.base.MessageExtendedMedia>`):
            N/A

    """

    __slots__: List[str] = ["peer", "msg_id", "extended_media"]

    ID = 0xd5a41724
    QUALNAME = "types.UpdateMessageExtendedMedia"

    def __init__(self, *, peer: "raw.base.Peer", msg_id: int, extended_media: List["raw.base.MessageExtendedMedia"]) -> None:
        self.peer = peer  # Peer
        self.msg_id = msg_id  # int
        self.extended_media = extended_media  # Vector<MessageExtendedMedia>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateMessageExtendedMedia":
        # No flags
        
        peer = TLObject.read(b)
        
        msg_id = Int.read(b)
        
        extended_media = TLObject.read(b)
        
        return UpdateMessageExtendedMedia(peer=peer, msg_id=msg_id, extended_media=extended_media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        b.write(Vector(self.extended_media))
        
        return b.getvalue()
