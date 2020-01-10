from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_script import Manager,prompt_bool
from flask import Flask, render_template, request,url_for,jsonify
from werkzeug.utils import secure_filename
import time
import  os
import datetime


app4 = Flask(__name__)

#127.0.0.1表示本机
app4.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app4.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app4.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app4.config['SQLALCHEMY_DATABASE_URI']="mysql://root:123456@localhost/weblearning"

db = SQLAlchemy(app4)

#定义模型,必须继承自db.Model
class User(db.Model):
    #指定表名
    __tablename='user'
    id=db.Column(db.Integer,primary_key=True)
    #unique为唯一字段，即不能重复
    chedao=db.Column(db.String(30))
    level= db.Column(db.String(30))
    year=db.Column(db.String(30))
    environment=db.Column(db.String(30))
    kangzhen=db.Column(db.String(30))
    gongqi=db.Column(db.String(30))
    huanjing=db.Column(db.String(30))
    jiaotongliang=db.Column(db.String(30))
    zijin=db.Column(db.String(30))
    jiakuan=db.Column(db.String(30))
    xuanze=db.Column(db.String(30))
    #录入时间.default=datetime.datetime.now
    time=db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)


#删除数据表
def drop():
    db.drop_all()
    return '数据表删除成功'

def create():
    db.create_all()
    return '数据库创建成功'

@app4.route('/')
def pingjia():

    return render_template('pingjia.html')


@app4.route('/insert', methods=['POST'])
def insert():
    print('————')
    if request.method == 'POST':
        xuanze=[]
        for i in range(11):
            J=request.form['q'+str(i+1)]
            xuanze.append(J)
        print(xuanze)

        shuju = User(chedao=str(xuanze[0]),level=str(xuanze[1]),year=str(xuanze[2])
                     ,environment=str(xuanze[3]),kangzhen=str(xuanze[4]),gongqi=str(xuanze[5])
                     ,huanjing=str(xuanze[6]),jiaotongliang=str(xuanze[7]),zijin=str(xuanze[8])
                     ,jiakuan=str(xuanze[9]),xuanze=str(xuanze[10])
                     )
        # 更新时间
        User.query.filter(db.cast(User.time, db.DATE) == db.cast(User.time, db.DATE)).all()
        db.session.add(shuju)

    #db.session.commit()
    #添加多条数据
    #db.session.add_all([,,,])
    return '数据已存入数据库'


if __name__ == '__main__':
    app4.run(debug= True )