from flask import Flask 
from hw_01 import *

app = Flask(__name__)

@app.route("/mycsjoke", methods=["GET"])
def mymethod2():
    return "There are 10 types of people. Ha! ha, ha!"

@app.route("/heartrate/last", methods=["GET"])
def getRecentMostHeartRate():
    ret = get_hearrate()
    return ret

@app.route("/steps/last", methods=["GET"])
def getRecentMostStepsCount():
    ret = get_steps_lastknown()
    return ret

@app.route("/sleep/<date>", methods=["GET"])
def  getSleepByDate(date):
    ret = get_sleepByDate(date)
    return ret

@app.route("/activity/<date>", methods=["GET"])
def getActivityLevelsByDate(date):
    ret = get_activenessByDate(date)
    return ret


if __name__ == '__main__':
    app.run(debug=True)
    