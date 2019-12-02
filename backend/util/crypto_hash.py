import hashlib
import json


def crypto_hash(*args):
    """
    Return sha-256 hash of given arguments
    :param args:
    :return:
    """
    # stringified_data = json.dumps(data)
    stringified_args = sorted(map(lambda data: json.dumps(data), args))
    joined_data = ''.join(stringified_args)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()
