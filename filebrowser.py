#!/usr/bin/env python3

import argparse
import logging
import os

from flask import Flask, flash, request, make_response
from flask_autoindex import AutoIndex
from werkzeug.utils import secure_filename
import ssl


parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", help="Port used to serve up content", default=8000, type=int)
parser.add_argument("-f", "--folder", help="Folder to serve content from", default="/tmp/")
parser.add_argument("--ssl", help="Enables SSL encryption for your server", default=False, action='store_true')
parser.add_argument("--fullchain", help="Sets the path for the Full Chain certificate", default="fullchain.pem")
parser.add_argument("--privkey", help="Sets the path for the Private Key", default="privkey.key")

args = parser.parse_args()

UPLOAD_FOLDER = args.folder

app = Flask(__name__, static_url_path=UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
if args.ssl:
    context = ssl.SSLContext()
    context.load_cert_chain(args.fullchain, args.privkey)

AutoIndex(app, browse_root=app.config['UPLOAD_FOLDER'])
logging.basicConfig(filename='filebrowser.log', level=logging.DEBUG)
log = logging.getLogger('pydrop')


@app.route("/", defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    if request.method == 'POST':
        if request.files['file'].filename != '':
            file = request.files['file']
            save_path = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], path), secure_filename(file.filename))

            current_chunk = int(request.form['dzchunkindex'])

            # If the file already exists it's ok if we are appending to it,
            # but not if it's new file that would overwrite the existing one
            if os.path.exists(save_path) and current_chunk == 0:
                # 400 and 500s will tell dropzone that an error occurred and show an error
                flash("File already exists", "danger")
                return make_response(('File already exists', 400))

            try:
                with open(save_path, 'ab') as f:
                    f.seek(int(request.form['dzchunkbyteoffset']))
                    f.write(file.stream.read())
            except OSError:
                # log.exception will include the traceback so we can see what's wrong
                flash("Couldn't write to file", "danger")
                log.exception('Could not write to file')
                return make_response(("Not sure why,"
                                      " but we couldn't write the file to disk", 500))

            total_chunks = int(request.form['dztotalchunkcount'])

            if current_chunk + 1 == total_chunks:
                # This was the last chunk, the file should be complete and the size we expect
                if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                    flash(f"File {file.filename} was completed, "
                          f"but has a size mismatch."
                          f"Was {os.path.getsize(save_path)} but we"
                          f" expected {request.form['dztotalfilesize']} ", "warning")
                    log.error(f"File {file.filename} was completed, "
                              f"but has a size mismatch."
                              f"Was {os.path.getsize(save_path)} but we"
                              f" expected {request.form['dztotalfilesize']} ")
                    return make_response(('Size mismatch', 500))
                else:
                    flash("File Uploaded Successfully", "success")
                    log.info(f'File {file.filename} has been uploaded successfully')
            else:
                log.debug(f'Chunk {current_chunk + 1} of {total_chunks} '
                          f'for file {file.filename} complete')

            return make_response(("Chunk upload successful", 200))


if __name__ == "__main__":
    print('Serving content from: %s' % args.folder)
    if args.ssl:
        app.run(host='0.0.0.0', port=args.port, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=args.port)
