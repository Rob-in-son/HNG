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
    user_data["status_code"] = 200
    
    dictionary= user_data
    unordered_dict = json.dumps(dictionary)

    #placeholder = '_'*(len(unordered_dict)-2)  # Create a placeholder, -2 due to ""
    #ordered_dict = jsonify(placeholder)  # This needs to be the same length as the response
    #ordered_dict.unordered_dict[0] = unordered_dict + '\n' +  # Replace with the actual response
    
    return user_data


if __name__ == "__main__":
    app.run(debug=True)