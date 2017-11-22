import boto3
from chalice import Chalice, Response

from chalicelib.model import Song

app = Chalice(app_name='music-manager')
s3_client = boto3.client('s3')
BUCKET = 'nthienan.com'


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/song', methods=['POST'])
def create_song():
    data = app.current_request.json_body
    s = Song(**data)
    s.save()
    return data


@app.route('/upload/{file_name}', methods=['POST'],
           content_types=['application/octet-stream'])
def upload_to_s3(file_name):
    try:
        # get raw body of PUT request
        body = app.current_request.raw_body

        # write body to tmp file
        tmp_file_name = '/tmp/' + file_name
        with open(tmp_file_name, 'wb') as tmp_file:
            tmp_file.write(body)

        # upload tmp file to s3 bucket
        s3_client.upload_file(tmp_file_name, BUCKET, file_name)

        return Response(body='upload successful: {}'.format(file_name),
                        status_code=200,
                        headers={'Content-Type': 'text/plain'})
    except Exception as e:
        app.log.error('error occurred during upload %s' % e)
        return Response(message='upload failed %s' % e,
                        headers={'Content-Type': 'text/plain'}, status_code=400)
