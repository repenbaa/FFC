import sys
import librosa
from tensorflow.keras.models import Model
import tensorflow as tf
import numpy as np
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/")  # 根目錄
def HomeSite():
    print('HOMESITE')
    sys.stdout.flush()
    return render_template('audio_Flask.html')


@app.route('/', methods=['POST'])
def upload_file():
    print('UPLOAD_FILE')
    sys.stdout.flush()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        list = os.listdir(app.config['UPLOAD_FOLDER'])
        # 庫不存在就上傳
        if filename not in list or len(list) == 0:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('uploaded_file',
                                filename=filename))
    return


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print('UPLOADED_FILE')
    sys.stdout.flush()
    list = os.listdir(app.config['UPLOAD_FOLDER'])
    person1 = app.config['UPLOAD_FOLDER']+filename
    _text = ''
    if filename in list:
        for i in range(len(list)):
            person2 = app.config['UPLOAD_FOLDER'] + list[i]
            text, dist = infer_return(person1, person2)
            if dist >= 0.7:
                _text = text
                break
            else:
                _text = '無使用者資料'

    return render_template('audio_Flask.html', text=_text)


def infer_return(person1, person2):
    print('I"M A MOD')
    sys.stdout.flush()
    _person1,  _person2 = person1, person2
    feature1, feature2 = infer(_person1)[0], infer(_person2)[0]
    # 对角余弦值
    dist = np.dot(feature1, feature2) / \
        (np.linalg.norm(feature1) * np.linalg.norm(feature2))
    if dist >= 0.7:
        return "%s 和 %s 同一个人，相似度为：%f" % (_person1, _person2, dist), dist
    else:
        return "%s 和 %s 不是同一个人，相似度为：%f" % (_person1, _person2, dist), dist


layer_name = 'global_max_pooling2d'
model = tf.keras.models.load_model(
    './Types_resnet.h5')
intermediate_layer_model = Model(
    inputs=model.input, outputs=model.get_layer(layer_name).output)


# 读取音频数据
def load_data(data_path):
    print('LET ME LOAD_DATA')
    sys.stdout.flush()
    wav, sr = librosa.load(data_path, sr=16000)
    intervals = librosa.effects.split(wav, top_db=20)
    wav_output = []
    for sliced in intervals:
        wav_output.extend(wav[sliced[0]:sliced[1]])
    assert len(wav_output) >= 8000, "有效音频小于0.5s"
    wav_output = np.array(wav_output)
    ps = librosa.feature.melspectrogram(
        y=wav_output, sr=sr, hop_length=256).astype(np.float32)
    ps = ps[np.newaxis, ..., np.newaxis]
    return ps


def infer(audio_path):
    print('NOW INFER')
    sys.stdout.flush()
    data = load_data(audio_path)
    feature = intermediate_layer_model.predict(data)
    return feature


if __name__ == '__main__':
    # 初始化函式
    #app.debug = True
    print('START TO MAIN')
    sys.stdout.flush()
    UPLOAD_FOLDER = './audio_db/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    try:
        port = int(os.environ.get('PORT', 5000))
        print('port is {}, fun is {}'.format(port, 'get'))
        sys.stdout.flush()
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print('Err is {}, fun is {}'.format(e, 'no used get'))
        sys.stdout.flush()
        port = int(os.environ["PORT"])
        app.run(port=port)
