import hashlib
import uuid

import boto3
from chalice import Chalice, Response

from chalicelib.model import Song, User

app = Chalice(app_name='music-manager')
s3_client = boto3.client('s3')
BUCKET = 'nthienan.com'


###########
#  SONG  #
##########
@app.route('/song/{id}', cors=True)
def get_song_by_id(id):
    try:
        songs = Song.owner_index.query(id)
        return [{'id': s.id, 'name': s.name} for s in songs]
    except Exception as e:
        app.log.error('%s' % e)


@app.route('/song', methods=['POST'], cors=True)
def create_song():
    try:
        data = app.current_request.json_body
        s = Song(**data)
        s.id = Song.uuid()
        s.save()
        return s
    except Exception as e:
        app.log.error('error occurred during create song %s' % e)


@app.route('/{user_id}/song', cors=True)
def get_song_by_user(user_id):
    try:
        songs = Song.scan(Song.owner.startswith(user_id))
        return [{'id': s.id, 'name': s.name} for s in songs]
    except Exception as e:
        app.log.error('%s' % e)


@app.route('/{user_id}/upload', methods=['POST'],
           content_types=['application/octet-stream'], cors=True)
def upload_to_s3(user_id):
    try:
        # get raw body of PUT request
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
        return Response(message='upload failed %s' % e,
                        headers={'Content-Type': 'text/plain'}, status_code=400)


###########
#  USERS  #
##########
@app.route('/user', methods=['POST'], cors=True)
def create_user():
    try:
        data = app.current_request.json_body
        u = User(**data)
        encoder = hashlib.md5()
        encoder.update(u.password.encode('utf8'))
        u.password = encoder.hexdigest()
        u.save()
        return u
    except Exception as e:
        app.log.error('%s' % e)


@app.route('/user/{id}', cors=True)
def get_user(id):
    try:
        users = User.query(id)
        return [{'name': u.name, 'email': u.email} for u in users]
    except Exception as e:
        app.log.error('%s' % e)


##################
#  AUTHENTICATE  #
#################


############
#  TABLES  #
###########
@app.route('/table/song', methods=['POST'], cors=True)
def create_table():
    try:
        if not Song.exists():
            Song.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        return "OK"
    except Exception as e:
        app.log.error('error occurred during create table %s' % e)


@app.route('/table/user', methods=['POST'], cors=True)
def create_table():
    try:
        if not User.exists():
            User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
        return "OK"
    except Exception as e:
        app.log.error('error occurred during create table %s' % e)
