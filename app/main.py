import json
import os
from flask import Flask, jsonify, request
from boto3 import client
 
app = Flask(__name__)

def get_client():
    return client(
        's3',
        'us-east-1',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
    )
 
@app.route("/")
def home_view():
        return "<h1>Hello Libranzas from flask and Heroku</h1>"


@app.route('/upload_files', methods=['POST'])
def upload_files():
    """ Endpoint to load files.
    """
    if request.method == 'POST':
        type_upload = request.args.get('type')
        body = json.loads(request.files['json'].read().decode('utf-8'))
        s3 = get_client()

        if type_upload == "libranzas":
            try:

                root_file = "./src/files/cargados/formato_libranzas__" + \
                    body.get('doc') + "." + body.get('type').split('/')[1]
                with open(root_file, "wb") as fp:
                    fp.write(request.files['file'].read())
                    
                name_file_S3 = "inputs/formato_libranzas_" + \
                    body.get('doc') + \
                    "." + body.get('type').split('/')[1]

                s3.upload_file(
                    root_file,
                    "qa-libranzas-archive",
                    name_file_S3,
                    ExtraArgs={
                        'ContentType': 'application/pdf',
                        'ContentDisposition': 'inline'
                    }
                )
                os.remove(root_file)

                return jsonify({'status': 'OK', 'mensaje': 'archivo subido exitosamente'})
            except Exception as e:
                return jsonify({'status': 'error', 'mensaje': e})

        elif type_upload == "comercio":
            try:
                root_file = "./src/files/cargados/formato_cam_comercio_" + \
                    body.get('doc') + "." + body.get('type').split('/')[1]
                with open(root_file, "wb") as fp:
                    fp.write(request.files['file'].read())

                name_file_S3 = "inputs/formato_cam_comercio_" + \
                    body.get('doc') + \
                    "." + body.get('type').split('/')[1]

                s3.upload_file(
                    root_file,
                    "qa-libranzas-archive",
                    name_file_S3,
                    ExtraArgs={
                        'ContentType': 'application/pdf',
                        'ContentDisposition': 'inline'
                    }
                )

                os.remove(root_file)
                return jsonify({'status': 'OK', 'mensaje': 'archivo subido exitosamente'})
            except Exception as e:
                return jsonify({'status': 'error', 'mensaje': e})

        return jsonify({"status": "ok"})

    else:
        return jsonify({'status': 'error', 'mensaje': 'La solicitud debe ser un POST'})
