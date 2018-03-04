from flask import Flask, render_template

app = Flask(__name__)

cats = ["Soccer", "Basketball", "Baseball", "Frisbee", "Snowboarding", "Rock Climbing", "Football", "Skating", "Hockey"]


@app.route('/')
def dashboard():
    return render_template('dashboard.html', categories=cats)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
