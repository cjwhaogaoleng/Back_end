from model.model import app,db
from calculate.cal import cal_api
app.register_blueprint(cal_api)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)