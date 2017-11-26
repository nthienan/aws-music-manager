import base64
import datetime

from pynamodb.exceptions import DoesNotExist

from chalicelib import utils
from chalicelib.model import Token

SECRET_KEY = '35vlrOmASfNGO8KXa3H'
EXPIRED_AFTER = 24 * 60 * 60 * 1000


def generate_token(email):
    expired_time_stamp = utc() + EXPIRED_AFTER
    token = encode(SECRET_KEY, str.format('{0}:{1}', email, expired_time_stamp))
    return '%s:%s' % (token, utils.md5(token))


def verify_token(token):
    token_info = extract_info(token)
    if not utils.md5(token_info['raw_token']) == token_info['signature']:
        raise Exception('The token is invalid.')
    if utc() > token_info['expired_time']:
        raise Exception('The token has expired.')


def extract_info(token):
    if ':' not in token:
        raise Exception('The token is invalid.')
    raw_data = token.split(':')
    result = {'raw_token': raw_data[0], 'signature': raw_data[1]}
    plain_text = decode(SECRET_KEY, raw_data[0])
    if ':' not in plain_text:
        raise Exception('The token is invalid.')
    text_split = plain_text.split(':')
    result['email'] = text_split[0]
    result['expired_time'] = int(text_split[1])
    return result


def is_valid_token(token):
    try:
        t = Token.get(token)
        if not t.valid:
            return False
        verify_token(token)
        return True
    except (DoesNotExist, Exception) as e:
        return False


def encode(key, string):
    enc = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(string[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode(''.join(enc).encode('utf-8')).decode('utf-8')


def decode(key, string):
    dec = []
    string = base64.urlsafe_b64decode(string).decode('utf-8')
    for i in range(len(string)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(string[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return ''.join(dec)


def utc():
    """
    Get timestamp in UTC timezone as long

    :return: number of milliseconds that present time in UTC timezone
    """
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
