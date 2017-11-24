import hashlib


def md5(string):
    encoder = hashlib.md5()
    encoder.update(string.encode('utf8'))
    return encoder.hexdigest()
