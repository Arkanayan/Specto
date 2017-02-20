from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        file_name = "sound_file"
        if file_name not in request.files:
            print("no file part")
            return redirect(request.url)
        file = request.files[file_name]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # File is accepted
            generate_spec(file)
            return redirect(request.url)
    
    return render_template('index.html')

def generate_spec(file):
    from scipy.io import wavfile
    import matplotlib.pyplot as plt
    import numpy as np
   # try:
    rate, data = wavfile.read(file.filename)
    trimmed_data = np.trim_zeros(data.flatten())
    #plt.plot(range(len(data)),data)
    plt.specgram(trimmed_data, NFFT=512, Fs=rate)
    plt.savefig(file.filename + ".png")
    # except Exception as identifier:
    #     print("Exception occurred.")

if __name__ == "__main__":
    app.run(debug=True)