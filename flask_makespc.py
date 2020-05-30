# MIT License
#
# Copyright (c) 2020 Oli Wright <oli.wright.github@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# flask_makespc.py
#
# Flask container for makespc.py
# Simple script to convert images to the Stop Press Canvas .SPC format which
# is used on Amstrad PCW8256 and friends.

import os
from flask import Flask, flash, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from makespc import convert_to_spc

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
PREVIEW_FOLDER = 'previews'
APP_UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLDER)
APP_OUTPUT_FOLDER = os.path.join(APP_ROOT, OUTPUT_FOLDER)
APP_PREVIEW_FOLDER = os.path.join(APP_ROOT, PREVIEW_FOLDER)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/preview/<path:filename>', methods=['GET', 'POST'])
def preview(filename):
    return send_from_directory(PREVIEW_FOLDER, filename=filename)

@app.route('/output/<path:filename>', methods=['GET', 'POST'])
def output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename=filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    html = '''
    <!doctype html>
    <title>Convert an image to .SPC</title>
    <h1>Make SPC Online</h1>
    <p>This tool converts images to Stop Press Canvas .SPC format, popular on Amstrad PCW8256 computers.</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Convert to SPC>
    </form>
    '''

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            input_filename = secure_filename(file.filename)
            full_input_filename = os.path.join(APP_UPLOAD_FOLDER, input_filename)
            file.save(full_input_filename)
            basename, extension = os.path.splitext(input_filename)
            preview_filename = basename + ".png"
            full_preview_filename = os.path.join(APP_PREVIEW_FOLDER, preview_filename)
            output_filename = basename + ".spc"
            full_output_filename = os.path.join(APP_OUTPUT_FOLDER, output_filename)
            convert_to_spc(full_input_filename, full_preview_filename, full_output_filename)
            html += '''
            <p>Click the image to download your SPC file.</p>
            <a href="/output/%s"><img src="/preview/%s"/></a>
            ''' % (output_filename, preview_filename)
    return html


