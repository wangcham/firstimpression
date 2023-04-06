from flask import Flask,session
import os

from loginregis import loginregis_app
from upload import upload_app
from myprofile import myprofile_app
from getimage import getimage_app
from avatar import avatar_app
from updateitem import updateitem_app
from searchresult import searchresult_app


app = Flask(__name__, static_folder='dist', static_url_path='')
app.register_blueprint(loginregis_app)
app.register_blueprint(upload_app)
app.register_blueprint(myprofile_app)
app.register_blueprint(getimage_app)
app.register_blueprint(avatar_app)
app.register_blueprint(updateitem_app)
app.register_blueprint(searchresult_app)



app.config['SECRET_KEY'] = 'withorwithoutyou'
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("dist/" + path):
        return app.send_static_file(path)
    else:
        return app.send_static_file("index.html")

if __name__ == '__main__':
    app.run()
