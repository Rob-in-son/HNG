from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route("/get_user/")
def get_user():

    day = datetime.datetime.now()
    current_day = (day.strftime("%A"))

    user_data = {
        "current_day" : current_day,
        "email" : "john.doe@example.com"
    }

    slack_name = request.args.get("slack_name")
    if slack_name:
        user_data["slack_name"] = slack_name

    track = request.args.get("track")
    if track:
        user_data["track"] = track

    return jsonify(user_data), 200

if __name__ == "__main__":
    app.run(debug=True)