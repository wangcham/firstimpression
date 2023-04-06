from flask import Blueprint, request, jsonify, render_template 
from flask_cors import CORS 
import mysql.connector 
from flask import send_file
import os
import imghdr
avatar_app = Blueprint('avatar_app', __name__, static_folder='dist', static_url_path='')
CORS(avatar_app)
app_root = os.path.dirname(os.path.abspath(__file__))
config = { 
    'user': 'root', 
    'password': 'superbl', 
    'host': 'localhost', 
    'database': 'userinfo', 
    'port': '3306', 
    'charset': 'utf8mb4'  
}
#获取用户描述和头像,用户头像更新都在此文件中
@avatar_app.route('/')
def index():
    return render_template('dist/index.html')

def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()
@avatar_app.route('/getavatar',methods=['post'])
def getavatar():
    data = request.get_json()
    username = data['username']
    if not username:
        return jsonify({'status':'fail','message':'getavatar中没有用户名'})
    else:
        conn,cursor = connect()
        sql = "SELECT avatar_url FROM users WHERE username=%s"
        cursor.execute(sql,(username,))
        result = cursor.fetchone()
        if result is not None:
            url = result[0]
            url = str(url)
            url = os.path.join(app_root,url)
            image_type = imghdr.what(url)
            if image_type == 'jpeg':
                mimetype = 'image/jpeg'
            elif image_type == 'png':
                mimetype = 'image/png'
            else:
                print('不属于任何图片类型,mimetype被设置为空')
                mimetype = ''
            close(conn, cursor)
            return send_file(url, mimetype=mimetype)
        else:
            return jsonify({'status': 'fail', 'message': '无返回头像'})

@avatar_app.route('/getdesc', methods=['post'])
def getdesc():
    data = request.get_json()
    username = data['username']
    if not username:
        return jsonify({'status': 'fail', 'message': 'getdesc中无用户名！'})
    else:
        conn, cursor = connect()
        sql = "SELECT description FROM users WHERE username=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result is not None:
            desc = result[0]
            close(conn, cursor)
            if not desc:
                return jsonify('未设置描述')
            else:
                return jsonify(desc)
        else:
            return jsonify({'status': 'fail', 'message': '获取描述发生错误！'})

        
#更新头像功能在upload.py中