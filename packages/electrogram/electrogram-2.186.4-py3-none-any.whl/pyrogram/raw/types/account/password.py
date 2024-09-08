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


class Password(TLObject):  # type: ignore
    """Configuration for two-factor authorization

    Constructor of :obj:`~pyrogram.raw.base.account.Password`.

    Details:
        - Layer: ``187``
        - ID: ``957B50FB``

    Parameters:
        new_algo (:obj:`PasswordKdfAlgo <pyrogram.raw.base.PasswordKdfAlgo>`):
            The KDF algorithm for SRP two-factor authentication to use when creating new passwords

        new_secure_algo (:obj:`SecurePasswordKdfAlgo <pyrogram.raw.base.SecurePasswordKdfAlgo>`):
            The KDF algorithm for telegram passport

        secure_random (``bytes``):
            Secure random string

        has_recovery (``bool``, *optional*):
            Whether the user has a recovery method configured

        has_secure_values (``bool``, *optional*):
            Whether telegram passport is enabled

        has_password (``bool``, *optional*):
            Whether the user has a password

        current_algo (:obj:`PasswordKdfAlgo <pyrogram.raw.base.PasswordKdfAlgo>`, *optional*):
            The KDF algorithm for SRP two-factor authentication of the current password

        srp_B (``bytes``, *optional*):
            Srp B param for SRP authorization

        srp_id (``int`` ``64-bit``, *optional*):
            Srp ID param for SRP authorization

        hint (``str``, *optional*):
            Text hint for the password

        email_unconfirmed_pattern (``str``, *optional*):
            A password recovery email with the specified pattern is still awaiting verification

        pending_reset_date (``int`` ``32-bit``, *optional*):
            The 2FA password will be automatically removed at this date, unless the user cancels the operation

        login_email_pattern (``str``, *optional*):
            A verified login email with the specified pattern is configured

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetPassword
    """

    __slots__: List[str] = ["new_algo", "new_secure_algo", "secure_random", "has_recovery", "has_secure_values", "has_password", "current_algo", "srp_B", "srp_id", "hint", "email_unconfirmed_pattern", "pending_reset_date", "login_email_pattern"]

    ID = 0x957b50fb
    QUALNAME = "types.account.Password"

    def __init__(self, *, new_algo: "raw.base.PasswordKdfAlgo", new_secure_algo: "raw.base.SecurePasswordKdfAlgo", secure_random: bytes, has_recovery: Optional[bool] = None, has_secure_values: Optional[bool] = None, has_password: Optional[bool] = None, current_algo: "raw.base.PasswordKdfAlgo" = None, srp_B: Optional[bytes] = None, srp_id: Optional[int] = None, hint: Optional[str] = None, email_unconfirmed_pattern: Optional[str] = None, pending_reset_date: Optional[int] = None, login_email_pattern: Optional[str] = None) -> None:
        self.new_algo = new_algo  # PasswordKdfAlgo
        self.new_secure_algo = new_secure_algo  # SecurePasswordKdfAlgo
        self.secure_random = secure_random  # bytes
        self.has_recovery = has_recovery  # flags.0?true
        self.has_secure_values = has_secure_values  # flags.1?true
        self.has_password = has_password  # flags.2?true
        self.current_algo = current_algo  # flags.2?PasswordKdfAlgo
        self.srp_B = srp_B  # flags.2?bytes
        self.srp_id = srp_id  # flags.2?long
        self.hint = hint  # flags.3?string
        self.email_unconfirmed_pattern = email_unconfirmed_pattern  # flags.4?string
        self.pending_reset_date = pending_reset_date  # flags.5?int
        self.login_email_pattern = login_email_pattern  # flags.6?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Password":
        
        flags = Int.read(b)
        
        has_recovery = True if flags & (1 << 0) else False
        has_secure_values = True if flags & (1 << 1) else False
        has_password = True if flags & (1 << 2) else False
        current_algo = TLObject.read(b) if flags & (1 << 2) else None
        
        srp_B = Bytes.read(b) if flags & (1 << 2) else None
        srp_id = Long.read(b) if flags & (1 << 2) else None
        hint = String.read(b) if flags & (1 << 3) else None
        email_unconfirmed_pattern = String.read(b) if flags & (1 << 4) else None
        new_algo = TLObject.read(b)
        
        new_secure_algo = TLObject.read(b)
        
        secure_random = Bytes.read(b)
        
        pending_reset_date = Int.read(b) if flags & (1 << 5) else None
        login_email_pattern = String.read(b) if flags & (1 << 6) else None
        return Password(new_algo=new_algo, new_secure_algo=new_secure_algo, secure_random=secure_random, has_recovery=has_recovery, has_secure_values=has_secure_values, has_password=has_password, current_algo=current_algo, srp_B=srp_B, srp_id=srp_id, hint=hint, email_unconfirmed_pattern=email_unconfirmed_pattern, pending_reset_date=pending_reset_date, login_email_pattern=login_email_pattern)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.has_recovery else 0
        flags |= (1 << 1) if self.has_secure_values else 0
        flags |= (1 << 2) if self.has_password else 0
        flags |= (1 << 2) if self.current_algo is not None else 0
        flags |= (1 << 2) if self.srp_B is not None else 0
        flags |= (1 << 2) if self.srp_id is not None else 0
        flags |= (1 << 3) if self.hint is not None else 0
        flags |= (1 << 4) if self.email_unconfirmed_pattern is not None else 0
        flags |= (1 << 5) if self.pending_reset_date is not None else 0
        flags |= (1 << 6) if self.login_email_pattern is not None else 0
        b.write(Int(flags))
        
        if self.current_algo is not None:
            b.write(self.current_algo.write())
        
        if self.srp_B is not None:
            b.write(Bytes(self.srp_B))
        
        if self.srp_id is not None:
            b.write(Long(self.srp_id))
        
        if self.hint is not None:
            b.write(String(self.hint))
        
        if self.email_unconfirmed_pattern is not None:
            b.write(String(self.email_unconfirmed_pattern))
        
        b.write(self.new_algo.write())
        
        b.write(self.new_secure_algo.write())
        
        b.write(Bytes(self.secure_random))
        
        if self.pending_reset_date is not None:
            b.write(Int(self.pending_reset_date))
        
        if self.login_email_pattern is not None:
            b.write(String(self.login_email_pattern))
        
        return b.getvalue()
