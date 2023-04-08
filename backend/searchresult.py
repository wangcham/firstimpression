from flask import Blueprint, request, jsonify, render_template 
from flask_cors import CORS 
import mysql.connector 
from flask import send_file
import os
import imghdr
from datetime import datetime
searchresult_app = Blueprint('searchresult_app', __name__, static_folder='dist', static_url_path='')
CORS(searchresult_app)
app_root = os.path.dirname(os.path.abspath(__file__))
config = { 
    'user': 'root', 
    'password': 'superbl', 
    'host': 'localhost', 
    'database': 'userinfo', 
    'port': '3306', 
    'charset': 'utf8mb4'  
}

@searchresult_app.route('/')
def index():
    return render_template('dist/index.html')

def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()
#获取用户卡片
@searchresult_app.route('/get_userinfo_from_results',methods=['post'])
def get_userinfo_from_results():
    data = request.get_json()
    searchtext = data['searchtext']
    conn,cursor = connect()
    
    sql = "SELECT username, description FROM users WHERE username LIKE %s COLLATE utf8mb4_general_ci"
    searchtext = '%'+searchtext+'%'
    cursor.execute(sql,(searchtext,))
    results = cursor.fetchall()
    data=[]
    for result in results:
            username = result[0]
            desc = result[1]
            item = {'username': username, 'desc': desc}
            data.append(item)
    close(conn, cursor)
    return jsonify(data)
#获取卡片信息
@searchresult_app.route('/get_cards_from_results',methods=['post'])
def get_cards_from_results():
    data = request.get_json()
    searchtext = data['searchtext']
    conn,cursor = connect()

    sql = "SELECT text, created_at, user_id FROM image_and_text WHERE text LIKE %s COLLATE utf8mb4_general_ci"
    searchtext = '%'+searchtext+'%'
    cursor.execute(sql,(searchtext,))
    results = cursor.fetchall()
    data =[]
    for result in results:
         text = result[0]
         created_at = result[1]
         username = result[2]
         card = {'text':text,'created_at':created_at,'username':username}
         data.append(card)
    close(conn,cursor)
    if not data:
        return jsonify({'status':'fail','message':'data里为空值'})
    else:
        return jsonify(data)
#从卡片信息中获取图片
@searchresult_app.route('/get_images_from_results',methods=['post'])
def get_images_from_results():
    data = request.get_json()
    username = data['username']
    created_at = data['created_at']
    date_obj = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S %Z')
    mysql_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    conn,cursor = connect()
    sql = "SELECT url FROM image_and_text WHERE user_id=%s AND created_at=%s"
    cursor.execute(sql,(username,mysql_date_str,))
    result = cursor.fetchone()
    if result is not None:
        url = result[0]
        url = str(url)
        url = os.path.join(app_root,url)
        image_type = imghdr.what(url)
        if image_type == 'jpeg':
            mimetype ='image/jpeg'
        elif image_type == 'png':
            mimetype ='image/png'
        else:
            print('不属于任何图片类型,mimetype被设置为空')
            mimetype = ''
        close(conn,cursor)
        return send_file(url,mimetype=mimetype)
    else:
        return jsonify({'status':'fail','message':'无返回图片'})