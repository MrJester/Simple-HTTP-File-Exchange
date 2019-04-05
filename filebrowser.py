import os

from flask import Flask, request, redirect
from flask_autoindex import AutoIndex
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp/'

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
    app.run(host='0.0.0.0', port=5001)
