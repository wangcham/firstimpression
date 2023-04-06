from flask import Blueprint, request, jsonify, render_template 
from flask_cors import CORS 
import mysql.connector 
from flask import send_file
import os
import imghdr
getimage_app = Blueprint('getimage_app', __name__, static_folder='dist', static_url_path='')
CORS(getimage_app)
app_root = os.path.dirname(os.path.abspath(__file__))
config = { 
    'user': 'root', 
    'password': 'superbl', 
    'host': 'localhost', 
    'database': 'userinfo', 
    'port': '3306', 
    'charset': 'utf8mb4'  
}

@getimage_app.route('/')
def index():
    return render_template('dist/index.html')

def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()
@getimage_app.route('/getimage', methods=['POST'])
def getimage():
    data = request.get_json()
    username = data['username']
    n = data['n']  # 默认为0，表示从第0张图片开始查询
    if not username:
        return jsonify({'status': 'fail', 'message': 'getimage中无用户名'})
    else:
        conn, cursor = connect()
        sql = "SELECT url FROM image_and_text WHERE user_id=%s LIMIT 1 OFFSET %s"
        cursor.execute(sql, (username, n))
        result = cursor.fetchone()
        if result is not None:
            url = result[0]
            url = str(url)
            print(url)
            url = os.path.join(app_root, url)
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
            return jsonify({'status': 'fail', 'message': '无返回图片'})
