from flask import Flask,request,jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import sys
from model import configs
app = Flask(__name__)


cors = CORS(app)
# 加载配置文件
app.config.from_object(configs)
# db绑定app
db = SQLAlchemy(app)

class History(db.Model):
    __tablename__ = 'History'
    id = db.Column(db.Integer, primary_key=True)  # 设置主键, 默认自增
    number=db.Column(db.Integer)
    formula=db.Column(db.String(100))