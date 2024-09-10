from passlib.context import CryptContext

from fastapi_easystart.helpers.itercompat import is_iterable


def make_hashable(value):
    """
    Attempt to make value hashable or raise a TypeError if it fails.

    The returned value should generate the same hash for equal values.
    """
    if isinstance(value, dict):
        return tuple(
            [
                (key, make_hashable(nested_value))
                for key, nested_value in sorted(value.items())
            ]
        )
    # Try hash to avoid converting a hashable iterable (e.g. string, frozenset)
    # to a tuple.
    try:
        hash(value)
    except TypeError:
        if is_iterable(value):
            return tuple(map(make_hashable, value))
        # Non-hashable, non-iterable.
        raise
    return value


# Utility functions for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
