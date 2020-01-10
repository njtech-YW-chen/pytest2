from flask import Flask, render_template, request,url_for
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)


@app.route('/')
def home():
    #模板 转入新页面
    return render_template('home2.html')


@app.route('/predict', methods=['POST'])
def predict():
    df = pd.read_excel("C:/Users/cywti/Desktop/paper/decison.xlsx")
    #df = pd.read_csv("spam.csv", encoding="latin-1")
    data = df.head()

    X = df[['车道数', '公路等级', '桥梁预期寿命','道路运输环境', '风荷载等级', '工期', '绿色要求', '预计交通流量', '资金投入', '是否加宽']]
    Y = df[['选择形式']]
    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.2)

    # 建模实例化
    clf = tree.DecisionTreeClassifier(criterion='entropy'
                                      ,random_state=30
                                      ,splitter='random'
                                      ,max_depth=3
                                      ,min_samples_leaf=2
                                      ,min_samples_split=2
                                      )
    clf = clf.fit(Xtrain, Ytrain)
    score = clf.score(Xtest, Ytest)
    if request.method == 'POST':
        print('——预测——')
        #####表格信息采集
        jilu=[]
        for i in range(10):
            c=request.form['message'+str(i+1)]
            jilu.append(c)

        print(jilu)
        print('————')
        print(request.headers)
        print(request.json)
        print(request.data)
        jilu=jilu

        my_prediction=clf.predict([jilu])
        print(my_prediction)
        jieguo=my_prediction
        #jieguo为home.html 中text的name
        #jieguo=request.form['jieguo']
        print(jieguo)

        xuanze=['I-1型横截面','I-2型横截面','II-1型横截面','II-2型横截面','III-1型横截面','III-2型横截面']

        print('进入本次审查范围')
        i=jieguo[0]
        xianshi = '针对本次预测所选合适的桥型为'+xuanze[i]
        print(xianshi)


    #传入函数进入下一个页面
    return render_template('home2.html',Data=xianshi)
    #return render_template('result.html', prediction=my_prediction)


@app.route('/turn', methods=['POST'])
def turn():
    return render_template('phsi_stl.html')



if __name__ == '__main__':
    app.run(debug=True)
