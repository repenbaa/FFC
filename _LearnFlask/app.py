import os
from flask import Flask, render_template  # 讀html用
# 用於接收資料成功後，轉址的功能redirect包含url_for是固定用法
from flask import request, redirect, url_for
# ajax jquery會用到json傳輸資料
from flask import jsonify, json
#
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

## 今天學習flask導向用法, 未來將透過首頁.html的btn填寫好導向而非在網址處輸入

# 會去抓第一個遇到的函式, 我認為根目錄該設定為首頁


@app.route("/")  # 根目錄
def HomeSite():
    return render_template('home.html')

# URL導向簡易輸出方法
# print site string


@app.route("/hello_2")
def hello():
    return 'hello world_2'

# print simpole site


@app.route("/text")
def text():
    return '<h1>Hello World</h1>'

# print simpole site.html


@app.route("/home")
def home():
    return render_template('home.html')

# 擷取網址參數
# get url string & return; <name> 代表接收 name 參數為 字串型態


@app.route('/data/appInfo/0/<name>', methods=['GET'])
def queryDataMessageByName(name):
    print("type(name) : ", type(name))
    return 'String => {}'.format(name)

# get url int & return; <int:id> 代表接收 id 變數名稱 參數為 整數型態


@app.route('/data/appInfo/1/<int:id>', methods=['GET'])
def queryDataMessageById(id):
    print("type(id) : ", type(id))
    return 'int => {}'.format(id)

# get url int & return; <float:version> 代表接收 version 變數名稱 參數為 整數型態


@app.route('/data/appInfo/2/<float:version>', methods=['GET'])
def queryDataMessageByVersion(version):
    print("type(version) : ", type(version))
    return 'float => {}'.format(version)

# 以某html為基底延伸網頁導向至自訂的(test/app/data)網頁, 設定不同型態並送出參數方法


@app.route('/home/text')  # 對這網頁送text
def pageText():
    text = "來自/page/test, 所帶參數; 哈囉"
    return render_template('home.html', text=text)


@app.route('/home/app')  # 對這網頁送appInfo
def pageAppInfo():
    appInfo = {
        'id': 5,
        'name': 'Python - Flask',
        'version': '1.0.1',
        'author': 'Enoxs',
        'remark': 'Python - Web Framework'
    }
    return render_template('home.html', appInfo=appInfo)


@app.route('/home/data')  # 對這網頁送data
def pageData():
    data = {
        '01': 'Text Text Text',
        '02': 'Text Text Text1',
        '03': 'Text Text Text2',
        '04': 'Text Text Text3',
        '05': 'Text Text Text4'
    }
    return render_template('home.html', data=data)  # 給html的變數名稱


# request之轉址方法edirect(url_for())
"""
@app.route('/home/Submit', methods=['POST', 'GET'])
def submit():
    # 表單填資料的name是帶參數的重點
    if request.method == 'POST':
        user = request.form['user']  # 取得對應的資料
        print('post:user=>', user)
        # 有空改寫一夏url_for改變return
        return redirect(url_for('success', name=user, action='post'))
    else:
        user = request.args.get('user')
        print('get:user=>', user)
        # 導向網址並帶上兩筆參數
        return redirect(url_for('success', name=user, action='get'))

# success<名稱無法更改, 目前不論如何載入時無法顯示圖片
# 可能考慮僅使用在參數傳遞時使用吧, 不然一個正常的網頁拿到參數卻不能顯示其他路徑很難用


@app.route('/success/<action>/<name>')
def success(name, action):
    data = {
        'name': name,
        'action': action
    }
    return render_template('home.html', data_2=data)
"""

# 捨棄轉址redirect(url_for())的方法


@app.route('/home/Submit', methods=['POST', 'GET'])
def submit():
    # 表單填資料的name是帶參數的重點
    if request.method == 'POST':
        # user = request.form['user']  # 取得對應的資料
        #print('post:user=>', user)
        data = {
            'name': request.form['user'],
            'action': 'post'
        }
        return render_template('home.html', data_2=data)
        # return redirect(url_for('success', name=user, action='post'))
    else:
        #user = request.args.get('user')
        #print('get:user=>', user)
        data = {
            'name': request.args.get('user'),
            'action': 'get'
        }
        return render_template('home.html', data_2=data)
        # 導向網址並帶上兩筆參數
        # return redirect(url_for('success', name=user, action='get'))


# 蒐集前端資料填入自定json格式儲存對應路徑後寫與讀的方法
# write/load -> post/get -> json 方法


@app.route('/home/data/message/get', methods=['GET'])
def getDataMessage():
    if request.method == "GET":
        with open('static/data/message.json', 'r') as f:
            data = json.load(f)
            print("text : ", data)
        return jsonify(data)  # 直接回傳 data 也可以，都是 json 格式


@app.route('/home/data/message/post', methods=['POST'])
def setDataMessage():
    if request.method == "POST":
        data = {
            'appInfo': {
                'id': request.form['app_id'],
                'name': request.form['app_name'],
                'version': request.form['app_version'],
                'author': request.form['app_author'],
                'remark': request.form['app_remark']
            }
        }
        print(type(data))
        with open('static/data/input.json', 'w+') as f:
            json.dump(data, f)
        return jsonify(result='OK')

###


def allowed_file(filename):  # 副檔名檢查
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # if file and allowed_file(file.filename): # 副檔名檢查
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                               filename))
        return redirect(url_for('uploaded_file',
                                filename=filename))
    return


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    data = {
        'upload': app.config['UPLOAD_FOLDER'],
        'file': filename
    }
    return render_template('home.html', data_3=data)
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # 初始化函式
    app.debug = True
    UPLOAD_FOLDER = './audio_db'
    ALLOWED_EXTENSIONS = set('mp3')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(host='0.0.0.0')
