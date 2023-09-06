from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "This is my first route."

if __name__ == "__main__":
    app.run(debug=True)