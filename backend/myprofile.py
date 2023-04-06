from flask import Blueprint, request, jsonify, render_template 
from flask_cors import CORS 
import mysql.connector 
myprofile_app = Blueprint('myprofile_app', __name__, static_folder='dist', static_url_path='')
CORS(myprofile_app)

config = { 
    'user': 'root', 
    'password': 'superbl', 
    'host': 'localhost', 
    'database': 'userinfo', 
    'port': '3306', 
    'charset': 'utf8mb4'  
}
#用户信息更新在此文件中
@myprofile_app.route('/')
def index():
    return render_template('dist/index.html')

def connect():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return conn, cursor

def close(conn, cursor):
    cursor.close()
    conn.close()


@myprofile_app.route('/myprofile', methods=['POST'])
def myprofile():
    data = request.get_json()
    username = data['username']
    if not username:
        return jsonify({'status': 'fail', 'message': 'myprofile中无用户名'})
    else:
        conn, cursor = connect()
        sql = "SELECT text, created_at FROM image_and_text WHERE user_id=%s"
        cursor.execute(sql, (username,))
        results = cursor.fetchall()
        data = []
        for result in results:
            text = result[0]
            created_at = result[1]
            item = {'text': text, 'created_at': created_at}
            data.append(item)
        close(conn, cursor)
        return jsonify(data)


#用户信息更新，用户描述更新在此路由中
@myprofile_app.route('/updateinfo',methods=['post'])
def updateinfo():
    data = request.get_json()
    username = data['username']
    newpassword = data['newpassword']
    conn,cursor = connect()
    sql = "UPDATE users SET password=%s WHERE username=%s"
    cursor.execute(sql,(newpassword,username,))
    conn.commit()
    sql = "SELECT password FROM users WHERE username=%s"
    result = cursor.fetchone()
    cursor.execute(sql,(username,))
    if result is not None:
        pwnow = result[0]
        pwnow = str(pwnow)
        close(conn,cursor)
        if pwnow == newpassword:
            return jsonify({'status':'true','message':'密码更改成功'})
        else:
            return jsonify({'status':'fail','message':'密码更改失败'})
    else:
        close(conn,cursor)
        return jsonify({'status':'fail','message':'updateinfo数据库取出结果失败'})



#更改账户信息
@myprofile_app.route('/updatedesc',methods=['post'])
def updatedesc():
    data = request.get_json()
    desc = data['desc']
    username = data['username']
    if not desc:
        return jsonify({'status':'fail','message':'后端未获取到desc'})
    else:
        conn,cursor = connect()
        sql = "UPDATE users SET description=%s WHERE username=%s"
        cursor.execute(sql,(desc,username,))
        conn.commit()
        sql = "SELECT description FROM users WHERE username=%s"
        cursor.execute(sql,(username,))
        result = cursor.fetchone()
        close(conn,cursor)
        if result is not None:
            updatedesc = result[0]
            updatedesc = str(updatedesc)
            if updatedesc == desc:
                return jsonify({'status':'success','message':'更改描述成功！'})
            else:
                return jsonify({'status':'fail','message':'更改失败！'})
        else:
            return jsonify({'status':'fail','message':'数据库未获取内容'})



        


      
    
    