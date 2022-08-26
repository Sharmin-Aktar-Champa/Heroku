from flask import Flask

app = Flask(__name__)

@app.route("/mycsjoke", methods=["GET"])
def mymethod2():
    return "There are 10 types of people. Ha! ha, ha!"

if __name__ == '__main__':
    app.run(debug=True)
    