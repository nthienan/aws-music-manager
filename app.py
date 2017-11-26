import uuid
from datetime import datetime

import boto3
from chalice import Chalice, Response
from pynamodb.exceptions import DoesNotExist

from chalicelib import token
from chalicelib import utils
from chalicelib.model import Song, User, Token

app = Chalice(app_name='music-manager')
s3_client = boto3.client('s3')

BUCKET = 'nthienan.com'
DEFAULT_HEADERS = {'Content-Type': 'application/json'}
UNAUTHORIZED_RESPONSE = Response(body={'message': 'Unauthorized'}, status_code=401,
                                 headers=DEFAULT_HEADERS)


###########
#  SONG  #
##########
@app.route('/song/{id}', cors=True)
def get_song_by_id(id):
    if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
            app.current_request.headers['Authorization']):
        return UNAUTHORIZED_RESPONSE
    s = Song.get(id)
    return {'id': s.id, 'name': s.name, 'shared': s.shared}


@app.route('/song', methods=['POST'], cors=True)
def create_song():
    if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
            app.current_request.headers['Authorization']):
        return UNAUTHORIZED_RESPONSE
    data = app.current_request.json_body
    s = Song(**data)
    s.id = Song.uuid()
    s.save()
    return {'id': s.id, 'name': s.name, 'file': s.file, 'shared': s.shared, 'owner': s.owner}


@app.route('/{user_id}/song', cors=True)
def get_song_by_user(user_id):
    if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
            app.current_request.headers['Authorization']):
        return UNAUTHORIZED_RESPONSE
    songs = Song.scan(Song.owner.startswith(user_id))
    return [{'id': s.id, 'name': s.name} for s in songs]


@app.route('/{user_id}/upload', methods=['POST'],
           content_types=['application/octet-stream'], cors=True)
def upload_to_s3(user_id):
    try:
        if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
                app.current_request.headers['Authorization']):
            return UNAUTHORIZED_RESPONSE
        body = app.current_request.raw_body
        file_name = str(uuid.uuid4())
        # write body to tmp file
        tmp_file_name = '/tmp/' + file_name
        with open(tmp_file_name, 'wb') as tmp_file:
            tmp_file.write(body)

        # upload tmp file to s3 bucket
        s3_client.upload_file(tmp_file_name, BUCKET, 'music/%s/%s' % (user_id, file_name))

        return {'path': 'music/%s/%s' % (user_id, file_name)}
    except Exception as e:
        app.log.error('error occurred during upload %s' % e)
        return Response(body={'message': 'upload failed % s' % e},
                        headers=DEFAULT_HEADERS, status_code=400)


###########
#  USERS  #
##########
@app.route('/user', methods=['POST'], cors=True)
def create_user():
    data = app.current_request.json_body
    u = User(**data)
    u.password = utils.md5(u.password)
    u.save()
    return u


@app.route('/user/me', cors=True)
def create_user():
    try:
        if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
                app.current_request.headers['Authorization']):
            return UNAUTHORIZED_RESPONSE
        info = token.extract_info(app.current_request.headers['Authorization'])
        u = User.get(info['email'])
        return {'email': u.email, 'name': u.name}
    except (DoesNotExist, Exception) as e:
        app.log.warn(e)
        return Response(body={'message': 'Token is invalid'}, headers=DEFAULT_HEADERS)


@app.route('/user/{id}', cors=True)
def get_user(id):
    if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
            app.current_request.headers['Authorization']):
        return UNAUTHORIZED_RESPONSE
    users = User.query(id)
    return [{'name': u.name, 'email': u.email} for u in users]


##################
#  AUTHENTICATE  #
#################
@app.route('/login', methods=['POST'], cors=True)
def login():
    try:
        data = app.current_request.json_body
        u = User.get(hash_key=data['email'])
        if u and u.password == utils.md5(data['password']):
            t = token.generate_token(u.email)
            Token(token=t, valid=True, create_at=datetime.utcnow()).save()
            return Response(body={'token': t}, headers=DEFAULT_HEADERS)
        app.log.info('User \'%s\' fails to login due to incorrect email or password' % data['email'])
        return Response(body='Failed to login due to incorrect email or password', status_code=401,
                        headers=DEFAULT_HEADERS)
    except Exception as e:
        app.log.error(e)


@app.route('/logout', cors=True)
def logout():
    try:
        if 'Authorization' not in app.current_request.headers.keys() or not token.is_valid_token(
                app.current_request.headers['Authorization']):
            return UNAUTHORIZED_RESPONSE
        t = Token.get(app.current_request.headers['Authorization'])
        t.valid = False
        t.save()
    except (DoesNotExist, Exception) as e:
        pass
    return Response(body={'message': 'Logout successfully'}, headers=DEFAULT_HEADERS)


############
#  TABLES  #
###########
@app.route('/table/song', methods=['POST'], cors=True)
def create_table():
    try:
        if not Song.exists():
            Song.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            return Response(body={'message': 'Success'}, headers=DEFAULT_HEADERS)
    except Exception as e:
        return Response(body={'message': e}, headers=DEFAULT_HEADERS, status_code=500)


@app.route('/table/user', methods=['POST'], cors=True)
def create_table():
    try:
        if not User.exists():
            User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            return Response(body={'message': 'Success'}, headers=DEFAULT_HEADERS)
    except Exception as e:
        return Response(body={'message': e}, headers=DEFAULT_HEADERS, status_code=500)


@app.route('/table/token', methods=['POST'], cors=True)
def create_table():
    try:
        if not Token.exists():
            Token.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
            return Response(body={'message': 'Success'}, headers=DEFAULT_HEADERS)
    except Exception as e:
        return Response(body={'message': e}, headers=DEFAULT_HEADERS, status_code=500)
