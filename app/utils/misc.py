import uuid


def make_code():
    u = uuid.uuid4()
    return u.hex
