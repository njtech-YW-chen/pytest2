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
    return render_template('car_running.html')


if __name__ == '__main__':
    app.run(debug=True)