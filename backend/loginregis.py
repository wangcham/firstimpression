from flask import Blueprint, request, jsonify, render_template, session
from flask_cors import CORS
import mysql.connector
import os

loginregis_app = Blueprint('loginregis_app', __name__, static_folder='dist', static_url_path='')
CORS(loginregis_app,supports_credentials=True)

config = {
    'user': 'root',
    'password': 'superbl',
    'host': 'localhost',
    'database': 'userinfo',
    'port': '3306',
    'charset': 'utf8mb4'
}

@loginregis_app.route('/')
def index():
    return render_template('dist/index.html')


def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor


def close(conn, cursor):
    cursor.close()
    conn.close()


@loginregis_app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    username = data['username']
    password = data['password']
    avatar_url = os.path.join('usersavatar', 'default.png')

    conn, cursor = connect()

    sql = "SELECT * FROM users WHERE username=%s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()
    if result:
        close(conn, cursor)
        return jsonify({'status': 'fail', 'message': '该用户已经存在！'})

    sql = "INSERT INTO users (name, username, password, avatar_url) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (name, username, password, avatar_url))
    conn.commit()

    close(conn, cursor)

    return jsonify({'status': 'success', 'message': '注册成功！'})


@loginregis_app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn, cursor = connect()

    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, (username, password))
    result = cursor.fetchone()
    if result:
        session['username'] = username
        close(conn, cursor)
        return jsonify({'status': 'success', 'message': '登录成功！'})
    else:
        close(conn, cursor)
        return jsonify({'status': 'fail', 'message': '用户名或密码错误！'})


@loginregis_app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'status': 'success', 'message': '退出成功！'})


@loginregis_app.route('/check_login', methods=['GET'])
def check_login():
    if 'username' in session:
        return jsonify({'status': 'success', 'message': '已登录'})
    else:
        return jsonify({'status': 'fail', 'message': '未登录'})












