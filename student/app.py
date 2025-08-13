from flask import Flask, render_template, request, redirect

app = Flask(__name__)
signed_names = []  # 存储签到名单

# 签到页面（只处理GET）
@app.route('/', methods=['GET'])
def sign_page():
    return render_template('sign.html')

# 处理签到（只处理POST）
@app.route('/sign', methods=['POST'])
def sign():
    name = request.form.get('name')
    if name:
        signed_names.append(name)
    return redirect('/')

# 查看页面（只处理GET）
@app.route('/view', methods=['GET'])
def view():
    return render_template('view.html', names=signed_names)

if __name__ == '__main__':
    app.run(debug=True, port=5001)