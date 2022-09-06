import requests, json, pprint
from flask import jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta

token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyMzhSRFQiLCJzdWIiOiJCNEYzNVEiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBycHJvIHJudXQgcnNsZSByYWN0IHJsb2MgcnJlcyByd2VpIHJociBydGVtIiwiZXhwIjoxNjkzNDg4MDQxLCJpYXQiOjE2NjE5NTIwNDF9.uk4UyLwyQeLjnoE6jxKPNCxfkzs0mFTq_09cfuyV74U"
TOKEN =  token

def print_jokes():
    resp = requests.get("https://v2.jokeapi.dev/joke/Programming?type=single")
    x = json.loads(resp.text)
    print(x["joke"])
    return None

def get_activity_steps(token=token):
    myheader = {"Authorization": "Bearer"+ " " + token}
    myurl = "https://api.fitbit.com/1/user/-/activities/steps/date/2022-08-16/7d.json"
    getSteps = requests.get(url=myurl, headers=myheader).json()
    pprint.pprint(getSteps)
    return None

def get_name(token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1/user/-/profile.json"
    getProfile = requests.get(url=myurl, headers=myheader).json()
    user = getProfile["user"]
    name = user["fullName"]
    return name

def get_time_offset(str_time):
    current = datetime.now()
    date = current.strftime("%Y-%m-%d")
    t = datetime.strptime(date + " " + str_time, "%Y-%m-%d %H:%M:%S")
    offset = relativedelta(current, t)
    offset = "{} hours {} minutes {} seconds ago".format(offset.hours, offset.minutes, offset.seconds)
    return offset

def get_hearrate(token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl  = "https://api.fitbit.com/1/user/-/activities/heart/date/today/1d/1min.json"
    resp  = requests.get(url=myurl, headers=myheader)
    if resp.status_code != 200:
        return resp.json()
    resp =  resp.json()
    heart_rate_log = resp['activities-heart-intraday']['dataset']
    recent_heart_rate = heart_rate_log[-1]
    current = datetime.now()
    date = current.strftime("%Y-%m-%d")
    t = datetime.strptime(date+" "+recent_heart_rate['time'], "%Y-%m-%d %H:%M:%S")
    offset = relativedelta(current, t)
    offset = "{} hours {} minutes {} seconds ago".format(offset.hours, offset.minutes, offset.seconds)
    heart_rate = recent_heart_rate['value']
    ret = {'heart-rate':heart_rate, 'time offset':offset}
    return jsonify(ret)

def get_steps(token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1/user/-/activities/date/today.json"
    resp = requests.get(url=myurl, headers=myheader).json()
    summary = resp['summary']
    steps = summary['steps']
    return  steps

def get_steps_lastknown():
    myheader = {"Authorization":"Bearer "+token}
    stepsurl = "https://api.fitbit.com/1/user/-/activities/steps/date/today/1d/1min.json"
    respSteps = requests.get(url=stepsurl, headers=myheader)
    if respSteps.status_code  != 200:
        return respSteps.json()
    respSteps = respSteps.json()
    steps_intraday = respSteps["activities-steps-intraday"]["dataset"]
    steps_lastknown = {}
    steps_lk = {"steps":"data not found", "time offset":"data not  found"}
    for item in reversed(steps_intraday):
        if item['value'] != 0:
            steps_lastknown = item
            break
    if steps_lastknown != {}:
        steps_lk =  {"steps":steps_lastknown['value'], "time offset":get_time_offset(steps_lastknown['time'])}
    distanceurl = "https://api.fitbit.com/1/user/-/activities/distance/date/today/1d/1min.json"
    respDistance = requests.get(url=distanceurl, headers=myheader)
    if respDistance.status_code != 200:
        return respDistance.json()
    respDistance = respDistance.json()
    distance_intraday = respDistance["activities-distance-intraday"]["dataset"]
    distance_lastknown = {}
    distance_lk = {"distance":"data not found", "time offset":"data not found"}
    for  item in reversed(distance_intraday):
        if item['value'] != 0:
            distance_lastknown = item
            break
    if distance_lastknown != {}:
        distance_lk = {"distance":distance_lastknown['value'], "time offset":get_time_offset(distance_lastknown['time'])}
    return jsonify({"steps last recorded":steps_lk, "distance last recorded":distance_lk})

def get_sleep(token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate=today&sort=desc&offset=0&limit=3"
    resp = requests.get(url=myurl, headers=myheader).json()
    sleep_log = resp['sleep']
    if sleep_log[0]['isMainSleep']==True:
        recent_main_sleep = sleep_log[0]
    elif sleep_log[1]['isMainSleep']==True:
        recent_main_sleep = sleep_log[1]
    else:
        recent_main_sleep = sleep_log[2] 
    return recent_main_sleep['minutesAsleep']

def get_sleepByDate(date, token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1.2/user/-/sleep/date/"+date+".json"
    resp = requests.get(url=myurl, headers=myheader)
    if resp.status_code != 200:
        return resp.json()
    resp =  resp.json()
    breakdown_by_stages = resp["summary"].get("stages", {"Error message":"data not found"})
    pprint.pprint(breakdown_by_stages)
    return jsonify(breakdown_by_stages)

def get_activeness(token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1/user/-/activities/date/today.json"
    resp = requests.get(url=myurl, headers=myheader).json()
    sedentary = resp['summary']['sedentaryMinutes']
    very_active = resp['summary']['veryActiveMinutes']
    active = resp['summary']['fairlyActiveMinutes']+resp['summary']['lightlyActiveMinutes']+resp['summary']['veryActiveMinutes']
    return sedentary, very_active, active


def get_activenessByDate(date, token=token):
    myheader = {"Authorization":"Bearer "+token}
    myurl = "https://api.fitbit.com/1/user/-/activities/date/"+date+".json"
    resp = requests.get(url=myurl, headers=myheader)
    if resp.status_code != 200:
        return resp.json()
    resp =  resp.json()
    sedentary = resp['summary']['sedentaryMinutes']
    very_active = resp['summary']['veryActiveMinutes']
    lightly_active = resp['summary']['lightlyActiveMinutes']
    ret =  {"very-active": very_active, "lightly-active": lightly_active, "sedentary": sedentary}
    return jsonify(ret)



