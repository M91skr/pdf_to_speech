""" ------------------------------ The PDF to Speech ------------------------------

 In this code, a simple site is designed that reads your PDF files for you. in this site, the user uploads his pdf file.
The text is extracted and read to the user.

"""

from flask import Flask, render_template, request, redirect, flash, url_for, send_file
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from gtts import gTTS
import os

UPLOAD_PDF = 'files'
UPLOAD_AUDIO = 'voices'
ALLOWED_EXTENSIONS = {'pdf'}
language = 'en'

# ------------------------------ Web server ------------------------------

app = Flask(__name__)
app.secret_key = "h@1Lo"


def allowed_file(filename):
    file_extension = filename.rsplit('.', 1)[1].lower()
    is_allowed = False
    if '.' in filename and file_extension in ALLOWED_EXTENSIONS:
        is_allowed = True
    return is_allowed


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(f'{UPLOAD_PDF}/{file_name}')
            return redirect(url_for('displayـcontent', name=file_name))
    return render_template("index.html")


@app.route("/pdf_to_text/<name>", methods=['GET', 'POST'])
def displayـcontent(name):
    content_list = []
    audio_list = []
    with open(f'{UPLOAD_PDF}/{name}', 'rb') as file:
        pdfreader = PdfReader(file)
        for page in range(0, len(pdfreader.pages)):
            pageobj = pdfreader.pages[page]
            content = pageobj.extract_text()
            content_list.append(content)
            myobj = gTTS(text=content, lang=language, slow=False)
            file_name = f'content-{page.numerator}.mp3'
            myobj.save(f'{UPLOAD_AUDIO}/{file_name}')
            audio_list.append(file_name)
    return render_template("content.html", my_lists=zip(content_list, audio_list))


@app.route("/text_to_speach/", methods=['POST'])
def text_to_speach():
    data = request.date
    if data['txt']:
        myobj = gTTS(text=data['txt'], lang=language, slow=False)
        myobj.save("welcome.mp3")
        os.system("mpg321 welcome.mp3")


@app.route('/path/<file_name>')
def voice_path(file_name):
    return send_file(
        f'{UPLOAD_AUDIO}/{file_name}',
        mimetype="audio/wav",
        as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_PDF
