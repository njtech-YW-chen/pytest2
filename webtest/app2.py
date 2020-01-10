from flask import Flask, render_template, request,url_for,jsonify
from sklearn.model_selection import cross_val_score
import base64
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import  os
from flask import send_from_directory
from werkzeug.utils import secure_filename
import time
import xlrd
import xlwt
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import random


app = Flask(__name__)
UPLOAD_FOLDER='upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))


#允许上传类型
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
#/后需添加内容

#函数区
#allowed_file判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

####遍历查询函数
def bianli(a,b):
    index=[]
    for i in range(len(a)):
        if a[i] == b[i]:
            index.append(i)
        else:
            continue
    return index

#####随机选出5个置信ID
def xuanze(a):
    list=range(0,len(I))
    xin = random.sample(I,5)
    return xin

#####集成遍历
def jcbianli(a,b,c):
    index1=[]
    index2=[]
    index3=[]
    for i in range(len(a)):
        if a[i]==b[i] and b[i]==c[i]:
            index1.append(i)
        elif a[i] != b[i] and b[i]!=c[i] and c[i] != a[i]:
            index3.append(i)
        else:
            index2.append(i)

    return index1,index2,index3

#####输出值
def out_data(a,b,c):
    index=[]
    for i in range(len(a)):
        if a[i] == b[i] and b[i] == c[i]:
            index.append(a[i])
        elif a[i] != b[i] and b[i] != c[i] and c[i] != a[i]:
            index.append(0)
        else:
            if a[i] == b[i]:
                index.append(a[i])
            elif a[i] == c[i]:
                index.append(a[i])
            else:
                index.append(b[i])
    return index




@app.route('/')
def home():
    #模板 转入新页面
    return render_template('excel_training.html')

@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    print('——上传文件——')
    print(f)
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname=secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        print('时间')
        print(unix_time)

        ZH=str(unix_time)
        global E
        E = ZH
        ZH=ZH.encode()
        new_filename = ZH + '.'.encode() + ext.encode()  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename.decode()))  # 保存文件到upload目录
        print('文件地址')
        print(file_dir)
        print('new_filename')
        #定义全局变量
        global D
        D=file_dir
        global C
        C=ext
        token = base64.b64encode(new_filename)
        return jsonify({"errno": 0, "errmsg": "上传成功"})

    else:
        #errno为最后一次错误代码
        #停留在本页面

        #return render_template('car_running.html')
        return jsonify({"errno": 1001, "errmsg": "上传失败"})


#半监督学习预测模块
@app.route('/predict', methods=['POST'])
def predict():
    df = pd.read_excel('C:/Users/cywti/Desktop/pyfile/pytest/webtest/upload/'+str(E)+'.xlsx')
    print('半监督学习预测')
    data=df.head()
    X=df[['车道数','公路等级','桥梁预期寿命'
     ,'道路运输环境','风荷载等级','工期','绿色要求'
     ,'预计交通流量','资金投入','是否加宽'
       ]]
    Y = df[['选择形式']]
    xl = X[0:120]
    y1 = Y[0:120]
    y2 = Y[0:120]
    y3 = Y[0:120]
    T = 150
    ####记录论数
    n = 1
    ####初始值
    XX1 = df[['车道数', '是否加宽', '绿色要求', '桥梁预期寿命']]
    XX2 = df[['车道数', '公路等级', '预计交通流量', '工期']]
    XX3 = df[['车道数', '资金投入', '风荷载等级', '道路运输环境']]
    Xtrain1 = XX1[0:120]
    Xtrain2 = XX2[0:120]
    Xtrain3 = XX3[0:120]
    ####使用H1对未标记预测，得出6类结果
    Xnolable1 = XX1[120:]
    ####使用H2对未标记预测，得到6类结果
    Xnolable2 = XX2[120:]
    #####使用H3对未标记预测，得到6类结果
    Xnolable3 = XX3[120:]
    ######汇总随机
    ALL = [Xnolable1, Xnolable2, Xnolable3]
    changex = [Xtrain1, Xtrain2, Xtrain3]
    changey = [y1, y2, y3]

    for i in range(T):
        ####建造第一个分类器，只针对打分
        rfc1 = RandomForestClassifier(n_estimators=120
                                      , max_depth=13
                                      , random_state=0)
        H1 = rfc1.fit(changex[0], changey[0])
        ####建造第二个分类器，只针对数据
        rfc2 = RandomForestClassifier(n_estimators=120
                                      , max_depth=13
                                      , random_state=0)
        H2 = rfc2.fit(changex[1], changey[1])
        #####建造第三个分类起器
        rfc3 = RandomForestClassifier(n_estimators=120
                                      , max_depth=13
                                      , random_state=0)
        H3 = rfc3.fit(changex[2], changey[2])
        ######开始产生随机置子
        ###一下随机两个值
        list_fuzhu = [0, 1, 2]
        duoxuan = random.sample(list_fuzhu, 3)
        print(duoxuan)
        model_all = [H1, H2, H3]
        ######预测结果
        jieguo1 = model_all[duoxuan[0]].predict(ALL[duoxuan[0]])
        jieguo2 = model_all[duoxuan[1]].predict(ALL[duoxuan[1]])
        print(jieguo1)
        print(jieguo2)
        ####对结果进行遍历
        ID = bianli(jieguo1, jieguo2)
        print('_________________________-ID不存在？')
        print(ID)
        #由于在函数内，需将ID补充为全局变量
        global I
        I=ID
        ####对ID进行选择
        if len(ID) >= 5:
            xzID = xuanze(ID)
            print(xzID)
            #####此时默认有值
            ######把训练数据加入第三方分类器
            jgshuju = []
            ####输出结果数据
            for i in range(len(xzID)):
                jgshuju.append(jieguo1[xzID[i]])
            print(jgshuju)
            ####将结果添加到y1
            insertY = pd.DataFrame(jgshuju, columns=['选择形式'])
            above1 = changey[duoxuan[2]].loc[:len(changey[duoxuan[2]])]
            below1 = changey[duoxuan[2]].loc[len(changey[duoxuan[2]]) + 1:]
            newData2 = above1.append(insertY, ignore_index=True).append(below1, ignore_index=True)
            changey[duoxuan[2]] = newData2
            print(changey)
            #####输出前缀数据,values取值
            quanbu = ALL[duoxuan[2]].values
            qianshuju = []
            for i in range(len(xzID)):
                qianshuju.append(quanbu[xzID[i]])
            #####数据格式转成numpy
            print(qianshuju)
            print(np.array(qianshuju))
            plusshuju = np.array(qianshuju)
            #####添加到第三个数据下面
            #####取出列表
            biaotou = ALL[duoxuan[2]].columns.values.tolist()
            print(biaotou)
            ###插入行内容
            insertRow = pd.DataFrame(plusshuju, columns=biaotou)
            above = changex[duoxuan[2]].loc[:len(changex[duoxuan[2]])]
            below = changex[duoxuan[2]].loc[len(changex[duoxuan[2]]) + 1:]
            newData = above.append(insertRow, ignore_index=True).append(below, ignore_index=True)
            changex[duoxuan[2]] = newData
            print(changex[duoxuan[2]])
            ####删除未标签的点
            ####删除前置行数
            print(xzID)
            xzgID = []
            if n <= 1:
                for i in range(len(xzgID)):
                    xzgID.append(xzID[i] + 120)
            else:
                xzgID = xzID
            print('______________________')
            print(xzgID)
            print(Xnolable1)
            Xnolable1 = Xnolable1.drop(index=xzgID)
            Xnolable2 = Xnolable2.drop(index=xzgID)
            Xnolable3 = Xnolable3.drop(index=xzgID)
            print('_________________检查1')
            print(Xnolable1)
            # 对ID重新生成?????
            Xnolable1.reset_index(drop=True, inplace=True)
            Xnolable2.reset_index(drop=True, inplace=True)
            Xnolable3.reset_index(drop=True, inplace=True)
            print('_________________检查2')
            print(Xnolable1)
            ALL = [Xnolable1, Xnolable2, Xnolable3]
            n = n + 1
            print('_______________第一种运行解结束')
        elif len(ID) < 5 and len(ID) > 0:
            #####对于小于5的加入计算
            xzID = ID
            print(xzID)
            jgshuju = []
            ####输出结果数据
            for i in range(len(xzID)):
                jgshuju.append(jieguo1[xzID[i]])
            print(jgshuju)
            ####将结果添加到y1
            insertY = pd.DataFrame(jgshuju, columns=['选择形式'])
            above1 = changey[duoxuan[2]].loc[:len(changey[duoxuan[2]])]
            below1 = changey[duoxuan[2]].loc[len(changey[duoxuan[2]]) + 1:]
            newData2 = above1.append(insertY, ignore_index=True).append(below1, ignore_index=True)
            changey[duoxuan[2]] = newData2
            print(changey)
            #####输出前缀数据,values取值
            quanbu = ALL[duoxuan[2]].values
            qianshuju = []
            for i in range(len(xzID)):
                qianshuju.append(quanbu[xzID[i]])
            #####数据格式转成numpy
            print(qianshuju)
            print(np.array(qianshuju))
            plusshuju = np.array(qianshuju)
            #####添加到第三个数据下面
            #####取出列表
            biaotou = ALL[duoxuan[2]].columns.values.tolist()
            print(biaotou)
            ###插入行内容
            insertRow = pd.DataFrame(plusshuju, columns=biaotou)
            above = changex[duoxuan[2]].loc[:len(changex[duoxuan[2]])]
            below = changex[duoxuan[2]].loc[len(changex[duoxuan[2]]) + 1:]
            newData = above.append(insertRow, ignore_index=True).append(below, ignore_index=True)
            changex[duoxuan[2]] = newData
            print(changex[duoxuan[2]])
            ####删除未标签的点
            ####删除前置行数
            print(xzID)
            xzgID = []
            if n <= 1:
                for i in range(len(xzgID)):
                    xzgID.append(xzID[i] + 120)
            else:
                xzgID = xzID
            print('______________________')
            print(xzgID)
            print(Xnolable1)
            Xnolable1 = Xnolable1.drop(index=xzgID)
            Xnolable2 = Xnolable2.drop(index=xzgID)
            Xnolable3 = Xnolable3.drop(index=xzgID)
            print('_________________检查1')
            print(Xnolable1)
            # 对ID重新生成
            Xnolable1.reset_index(drop=True, inplace=True)
            Xnolable2.reset_index(drop=True, inplace=True)
            Xnolable3.reset_index(drop=True, inplace=True)
            print('_________________检查2')
            print(Xnolable1)
            ALL = [Xnolable1, Xnolable2, Xnolable3]
            n = n + 1
            print('_______________第二种运行解结束')
        else:
            n = n + 1
            print('_______________第三种运行解结束')

    ####使用H1对未标记预测，得出6类结果
    Xtest1 = XX1[120:]
    ####使用H2对未标记预测，得到6类结果
    Xtest2 = XX2[120:]
    #####使用H3对未标记预测，得到6类结果
    Xtest3 = XX3[120:]
    #####预测结果
    R1 = H1.predict(Xtest1)
    R2 = H2.predict(Xtest2)
    R3 = H3.predict(Xtest3)
    print(R1)
    print(R2)
    print(R3)
    #########集成判断
    [z1, z2, z3] = jcbianli(R1, R2, R3)
    print(z1, z2, z3)
    print('准确率：%s' % ((len(z1) + len(z2)) / 150))
    #####输出问题值,排序
    # Z=z1+z2
    # Z.sort()
    out = out_data(R1, R2, R3)
    print(out)
    print('_____运行完毕')

    return render_template('excel_training.html')


if __name__ == '__main__':
    app.run(debug=True)
