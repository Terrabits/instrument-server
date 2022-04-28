# constants
NoneType = type(None)


def to_bytes(data):
    if data is None:
        return

    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode()
    if isinstance(data, bool):
        return str(data).lower().encode()
    # else
    return str(data).encode()


def ellipsis_bytes(data):
    if len(data) < 25:
        # short enough
        return data

    # too long; apply ellipsis
    return data[:22] + b'...'
