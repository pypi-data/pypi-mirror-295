import uuid


def generate_uuid4(hex_flag=True):
    unique_id = uuid.uuid4()
    if hex_flag:
        unique_id = unique_id.hex
    return unique_id
