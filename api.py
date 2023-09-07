from flask import Flask, request, json, jsonify
import datetime
from collections import OrderedDict

app = Flask(__name__)

@app.route("/get_user/")
def get_user():
    #current_day
    day = datetime.datetime.now()
    current_day = (day.strftime("%A"))

    #Current_utc_time
    utc_time_value = datetime.datetime.utcnow()
    utc_time = utc_time_value.strftime("%Y-%m-%dT%H:%M:%SZ")
     
    #user_data_dictionary
    user_data = {}
    
    #Get slack_name and track
    slack_name = request.args.get("slack_name")
    if slack_name:
      user_data["slack_name"] = slack_name

    track = request.args.get("track")

    if track:
      user_data["track"] = track

    user_data["current_day"] = current_day
    user_data["utc_time"] = utc_time
    user_data["github_file_url"] = "https://github.com/Rob-in-son/HNG/blob/main/api.py"
    user_data["github_repo_url"] = "https://github.com/Rob-in-son/HNG.git"

    user_data["status_code"] = 200

    return user_data

if __name__ == "__main__":
    app.run(debug=True)