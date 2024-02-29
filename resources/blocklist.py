"""
This fiel just contains the blocklist of the JWT tokens. It will be importe by app and the logout resource so
that tockens can be added to blocklist when the user logs out.
"""

BLOCKLIST = set()

