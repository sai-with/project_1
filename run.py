from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# 추천 페이지





if __name__ == "__main__":
    app.run(debug=True)