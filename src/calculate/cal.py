from flask import Flask,request,jsonify
import re
import numpy as np
import math
from flask_sqlalchemy import SQLAlchemy
from model.model import app,db,History
from flask import Blueprint
cal_api = Blueprint('user_app', __name__)

@app.route('/get_result/',methods=['POST'])
def get_result():
    data = request.form.get("formula")
    dx = request.form.get("deg")
    fx=data
    data=data.replace("^","**")
    if dx=='yes':
        data=data.replace("atan(", "np.atan(np.pi/180*")
    else:
        data=data.replace("atan(", "np.atan(")
    if dx=='yes':
        data=data.replace("asin(", "np.asin(np.pi/180*")
    else:
        data=data.replace("asin(", "np.asin(")
    if dx=='yes':
        data=data.replace("acos(", "np.acos(np.pi/180*")
    else:
        data=data.replace("acos(", "np.acos(")
    if dx=='yes':
        data=data.replace("tan(", "np.tan(np.pi/180*")
    else:
        data=data.replace("tan(", "np.tan(")
    if dx=='yes':
        data=data.replace("sin(", "np.sin(np.pi/180*")
    else:
        data=data.replace("sin(", "np.sin(")
    if dx=='yes':
        data=data.replace("cos(", "np.cos(np.pi/180*")
    else:
        data=data.replace("cos(", "np.cos(")
    data=data.replace("π", "np.pi")
    data=data.replace("e", "np.exp(1)")
    data=re.sub("\|(\d+)\|",lambda x: "np.abs("+str(x.group(1))+")",data)
    data=data.replace("mod", "%")
    data=data.replace("log(", "np.log10(")
    data=data.replace("ln(", "np.log(")
    data=re.sub("(\d+)!",lambda x: "math.factorial("+str(x.group(1))+")",data)
    data=re.sub("√(\d+)",lambda x: "math.sqrt("+str(x.group(1))+")",data)
    data=re.sub("log(\d+)\((\d+)\)",lambda x: "np.log("+str(x.group(2))+")/np.log("+str(x.group(1))+")",data)
    f=0
    try:
        data=eval(data)
    except (ZeroDivisionError): 
        data=str('Error: 除零错误')
        f=1
    except NameError:
        data=str('Error: 请加上括号')
        f=1
    except SyntaxError:
        data=str('Error: 语法错误，请正确输入')
        f=1
    if f==0:
        if len(data>10):
            data=str('{:g}'.format(float(data)))
        new_history=History(number=data,formula=fx)
        db.session.add(new_history)
        db.session.commit()
    return jsonify({'result': data, 'message': 'success'})
        
@app.route('/read_history/',methods=['POST'])
def read_history():
    idd=request.form.get('id')
    h=History.query.get(idd)
    data={
        "number":h.number,
        "formula":h.formula
    }
    return jsonify({'result': data, 'message': 'success'})

@app.route('/read_all_history/',methods=['POST'])
def read_all_history():
    h=History.query.order_by(History.id)
    data=""
    for hh in h:
        data=data+str(hh.formula)+"="+str(hh.number)+","
    return jsonify({'result': data, 'message': 'success'})

@app.route('/delete_history/',methods=['POST'])
def delete_history():
    idd=request.form.get('id')
    h=History.query.get(idd)
    db.session.delete(h)
    db.session.commit()
    return jsonify({'result': 'success'})

@app.route('/delete_all_history/',methods=['POST'])
def delete_all_history():
    db.session.query(History).delete()
    db.session.commit()
