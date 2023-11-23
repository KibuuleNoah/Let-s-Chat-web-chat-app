from base64 import b64encode, b64decode


def convert_to_base64(data):
    try:
        return b64encode(data).decode()
    except:
        raise NotImplementedError("your provided invalid data fomart")


def convert_to_bytes(data):
    try:
        return b64decode(data)
    except:
        raise NotImplementedError("your provided invalid data fomart")
