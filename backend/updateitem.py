from flask import Blueprint, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import mysql.connector
import os
app_root = os.path.dirname(os.path.abspath(__file__))
updateitem_app = Blueprint('updateitem_app', __name__, static_folder='dist', static_url_path='')
CORS(updateitem_app)
config = {
    'user': 'root',
    'password': 'superbl',
    'host': 'localhost',
    'database': 'userinfo',
    'port': '3306',
    'charset': 'utf8mb4'
}

@updateitem_app.route('/')
def index():
    return render_template('dist/index.html')


def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()


@updateitem_app.route('/deleteitem',methods=['post'])
def deleteitem():
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
        sqlurl = url
        url = os.path.join(app_root,url)
        if os.path.exists(url):
            os.remove(url)
            sql = "DELETE FROM image_and_text WHERE url =%s"
            cursor.execute(sql,(sqlurl,))
            conn.commit()
            close(conn,cursor)
            return jsonify({'status':'success','message':'删除成功！'})
        else:
            return jsonify({'status':'fail','message':'文件路径不存在'})
    else:
        return jsonify({'status':'fail','message':'数据库未查询到结果'})

@updateitem_app.route('/updateitem',methods=['post'])
def updateitem():
    data = request.get_json()
    text = data['text']
    username = data['username']
    created_at = data['created_at']
    date_obj = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S %Z')
    mysql_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')

    conn,cursor = connect()

    sql = "UPDATE image_and_text SET text=%s WHERE user_id=%s AND created_at=%s "
    cursor.execute(sql,(text,username,mysql_date_str,))
    conn.commit()
    sql = "SELECT text FROM image_and_text WHERE user_id=%s AND created_at=%s"
    cursor.execute(sql,(username,mysql_date_str,))
    result = cursor.fetchone()
    if result is not None:
        updatedtext = result[0]
        updatedtext = str(updatedtext)
        if updatedtext == text:
            return jsonify({'status':'success','message':'更改成功'})
        else:
            return jsonify({'status':'fail','message':'更改失败'})
    else:
        return jsonify({'status':'fail','message':'数据库未查询到该条印象'})
    

@updateitem_app.route('/gettext',methods=['post'])
def gettext():
    data = request.get_json()
    username = data['username']
    created_at = data['created_at']
    date_obj = datetime.strptime(created_at, '%a, %d %b %Y %H:%M:%S %Z')
    mysql_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    conn,cursor = connect()

    sql="SELECT text FROM image_and_text WHERE user_id=%s AND created_at=%s"
    cursor.execute(sql,(username,mysql_date_str,))
    result = cursor.fetchone()
    close(conn,cursor)
    if result is not None:
        text = result[0]
        return jsonify(text)
    else:
        return jsonify({'status':'fail','message':'未得到数据'})