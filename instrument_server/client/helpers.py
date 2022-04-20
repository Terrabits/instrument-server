def to_bytes(result):
    if isinstance(result, bytes):
        return result
    if isinstance(result, str):
        # encode str to bytes
        return result.encode()

    # to "bytes str"
    return str(result).encode()
