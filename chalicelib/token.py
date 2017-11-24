import base64

import datetime

SECRET_KEY = "S3cr3ctK3y!"
# token will be invalid after 24 hours since it was generated
EXPIRED_AFTER = 24 * 60 * 60 * 1000


def gen_token(email):
    expired_time_stamp = utc() + EXPIRED_AFTER
    return encode(SECRET_KEY, str.format("{0}:{1}", email, expired_time_stamp))


def verify_token(token):
    plain_text = decode(SECRET_KEY, token)
    if ":" not in plain_text:
        raise Exception("The token is invalid.")
    text_split = plain_text.split(":")
    expired_time_stamp = long(text_split[1])
    if utc() > expired_time_stamp:
        raise Exception("The token has expired.")


def encode(key, string):
    """
    https://stackoverflow.com/a/16321853/4283455
    https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher

    :param key: secret key used to encode string
    :param string: string that will be encoded
    :return: encoded string
    """
    enc = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(string[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc))


def decode(key, string):
    dec = []
    string = base64.urlsafe_b64decode(string.encode("ascii"))
    for i in range(len(string)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(string[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def utc():
    """
    Get timestamp in UTC timezone as long

    :return: number of milliseconds that present time in UTC timezone
    """
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
