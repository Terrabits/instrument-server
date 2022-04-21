def ellipsis_bytes(bytes):
    if len(bytes) < 25:
        # short enough
        return bytes

    # too long; apply ellipsis
    return bytes[:22] + b'...'
