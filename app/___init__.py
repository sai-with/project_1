from flask import Flask, render_template
import sqlite3

app = Flask(__name__)



def get_trips():
    conn = sqlite3.connect("view/trip.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trips")  # trips 테이블에서 데이터를 가져옵니다.
    trips = cursor.fetchall()
    conn.close()
    return trips

@app.route("/")
def index():
    trips = get_trips()
    return render_template("index.html", trips=trips)

if __name__ == "__main__":
    app.run(debug=True)