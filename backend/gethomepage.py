from flask import Blueprint, request, jsonify, render_template 
from flask_cors import CORS 
import mysql.connector 
from flask import send_file
import os
import imghdr
from datetime import datetime
gethomepage_app = Blueprint('gethomepage_app', __name__, static_folder='dist', static_url_path='')
CORS(gethomepage_app)
app_root = os.path.dirname(os.path.abspath(__file__))
config = { 
    'user': 'root', 
    'password': 'superbl', 
    'host': 'localhost', 
    'database': 'userinfo', 
    'port': '3306', 
    'charset': 'utf8mb4'  
}

@gethomepage_app.route('/')
def index():
    return render_template('dist/index.html')

def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()

#获取impressions的tag里的卡片信息
@gethomepage_app.route('/get_homepage_cards',methods=['post'])
def get_homepage_cards():
    conn,cursor = connect()
    sql = "SELECT text,created_at,user_id FROM image_and_text ORDER BY id DESC"
    cursor.execute(sql)

    results = cursor.fetchall()
    data=[]
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


@gethomepage_app.route('/get_homepage_users',methods=['post'])
def get_homepage_users():
    conn,cursor = connect()
    sql = "SELECT username,description FROM users"
    cursor.execute(sql)

    results = cursor.fetchall()
    data = []
    for result in results:
        username = result[0]
        desc = result[1]
        item = {'username': username, 'desc': desc}
        data.append(item)
    close(conn,cursor)
    return jsonify(data)
