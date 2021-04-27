from flask import Flask, render_template

import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="MyNewPassword",
    database="snakegame",
    auth_plugin="mysql_native_password"
)

cursor = db.cursor()
cursor.execute("SELECT * FROM scores ORDER BY score DESC")
result = cursor.fetchall()


@app.route('/', methods=['GET'])
def default():
    return render_template('index.html', scores=result)


@app.route('/list')
def list_all_scores():
    return {"scores": result}


if __name__ == "__main__":
    app.run(debug=True)
