from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE


def int_to_bytes(num: int, buffer=None):
    if num == 0:
        return b'\x00'

        # Calculate the number of bytes needed to represent the integer
    byte_length = (num.bit_length() + 7) // 8

    # If no buffer is provided or it's too small, return the bytes directly
    if buffer is None or len(buffer) < byte_length:
        return num.to_bytes(byte_length, ENDIAN_TYPE)

    # Convert integer to bytes directly into the provided buffer
    num_bytes = num.to_bytes(byte_length, ENDIAN_TYPE)

    buffer[:byte_length] = num_bytes
    return bytes(buffer[:byte_length])
