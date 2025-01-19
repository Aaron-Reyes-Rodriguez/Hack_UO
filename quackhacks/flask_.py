from flask import Flask, render_template

schedule_app = Flask(__name__)

@schedule_app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    schedule_app.run(debug=True)