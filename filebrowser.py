#!/usr/bin/env python3

import os
import argparse
from flask import Flask, request, redirect
from flask_autoindex import AutoIndex
from werkzeug import secure_filename

parser = argparse.ArgumentParser()

parser.add_argument("port", help="Port used to serve up content", default=8000, type=int)
parser.add_argument("-f", "--folder", help="Folder to serve content from", default="/tmp/")

args = parser.parse_args()

UPLOAD_FOLDER = args.folder

app = Flask(__name__, static_url_path=UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
AutoIndex(app, browse_root=app.config['UPLOAD_FOLDER'])


@app.route("/", defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def index(path):
    if request.method == 'POST':
        if request.files['file'].filename != '':
            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], path), filename))
        return redirect("/" + path)


if __name__ == "__main__":
    print('Serving content from: %s' % args.folder)
    app.run(host='0.0.0.0', port=args.port)
