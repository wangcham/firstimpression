from flask import Blueprint, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import os
import datetime
from config import UPLOAD_FOLDER
#注册路由
upload_app = Blueprint('upload_app', __name__, static_folder='dist', static_url_path='')
CORS(upload_app)
config = {
    'user': 'root',
    'password': 'superbl',
    'host': 'localhost',
    'database': 'userinfo',
    'port': '3306',
    'charset': 'utf8mb4'
}

  # 存储用户上传图片的文件夹名在app.py中
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # 允许上传的图片文件格式


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')




@upload_app.route('/')
def index():
    return render_template('dist/index.html')
#注册成功

#连接数据库方法
def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()


@upload_app.route('/upload',methods=['POST'])
def upload():
  
    user_id = request.form.get('user_id')
    text = request.form.get('text')
    image_file = request.files.get('image',None)
    upload_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 获取当前时间
    if image_file is not None:
        if not allowed_file(image_file.filename):
            return jsonify({'status': 'fail', 'message': '只允许上传png,jpg,jpeg格式的图片！'})
    else:
        return jsonify({'status':'fail','message':'空文件！'})

    if not text:
        return jsonify({'status':'fail','message':'空的文本！'})

    conn,cursor = connect()

    os.makedirs(UPLOAD_FOLDER,exist_ok=True)
    image_name = f"{get_current_time()}_{image_file.filename}"
    image_path = os.path.join(UPLOAD_FOLDER, image_name)  # 构造图片保存路径
    image_file.save(image_path)  # 保存图片



    sql = "INSERT INTO image_and_text (user_id, url, text, created_at) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (user_id, image_path, text, upload_time))
    conn.commit()

    # 关闭数据库连接
    close(conn, cursor)
    return jsonify({'status': 'true', 'message': '上传成功！'})

@upload_app.route('/updateavatar',methods=['POST'])
def updateavatar():
    username = request.form.get('username')
    image_file = request.files.get('image',None)
    if image_file is not None:
        if not allowed_file(image_file.filename):
            return jsonify({'status': 'fail', 'message': '只允许上传png,jpg,jpeg格式的图片！'})
    else:
        return jsonify({'status':'fail','message':'空文件！'})

    image_name = f"{get_current_time()}_{image_file.filename}"
    avatar_url = os.path.join('usersavatar', image_name)  # 构造图片保存路径
    image_file.save(avatar_url)  # 保存图片
    conn,cursor = connect()
    sql = "UPDATE users SET avatar_url=%s WHERE username=%s"
    cursor.execute(sql,(avatar_url,username,))
    conn.commit()
    sql = "SELECT avatar_url FROM users WHERE username=%s"
    cursor.execute(sql,(username,))
    result = cursor.fetchone()
    if result is not None:
        url = result[0]
        url = str(url)
        if url == avatar_url:
            return jsonify({'status':'true','message':'头像上传成功'})
        else:
             return jsonify({'status':'fail','message':'上传失败'})
    else:
        return jsonify({'status':'fail','message':'数据库检索失败'})

    
    





