from __future__ import annotations

from pyrogram.types.object import Object


class ShippingAddress(Object):
    """Contains information about a shipping address.

    Parameters:
        street_line1 (``str``):
            First line for the address.

        street_line1 (``str``):
            Second line for the address.

        city (``str``):
            City for the address.

        state (``str``):
            State for the address, if applicable.

        post_code (``str``):
            Post code for the address.

        country_code (``str``):
            Two-letter ISO 3166-1 alpha-2 country code.
    """

    def __init__(
        self,
        *,
        street_line1: str,
        street_line2: str,
        city: str,
        state: str,
        post_code: str,
        country_code: str,
    ) -> None:
        super().__init__()

        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.city = city
        self.state = state
        self.post_code = post_code
        self.country_code = country_code
