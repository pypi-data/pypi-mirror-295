import secrets as _secrets

from .__main__ import never_gonna_give_you_up

if _secrets.randbelow(2) == 0:
    never_gonna_give_you_up()
