from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure your MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'firehydrantsdb'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inspections')
def inspections():
    return render_template('inspections.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/regions')
def regions():
    return render_template('regions.html')

@app.route('/workers')
def workers():
    return render_template('workers.html')

@app.route('/workers_inspections')
def workers_inspections():
    return render_template('workers_inspections.html')

@app.route('/hydrants_inspections')
def hydrants_inspections():
    return render_template('hydrants_inspections.html')


@app.route('/hydrants', methods=['GET'])
def hydrants():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hydrants")
    rows = cur.fetchall()
    cur.close()
    return render_template('hydrants.html', hydrants=rows)

@app.route('/hydrants/add', methods=['POST'])
def add_hydrant():
    data = request.form
    region = data.get('region')
    flow_rate = data.get('flow_rate')
    operational = data.get('operational')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    cur = mysql.connection.cursor()
    sql = "INSERT INTO hydrants (region, flow_rate, operational, longitude, latitude) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(sql, (region, flow_rate, operational, longitude, latitude))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_hydrants'))

@app.route('/hydrants/update/<int:id>', methods=['POST'])
def update_hydrant(id):
    data = request.form
    region = data.get('region')
    flow_rate = data.get('flow_rate')
    operational = data.get('operational')
    longitude = data.get('longitude')
    latitude = data.get('latitude')
    cur = mysql.connection.cursor()
    sql = "UPDATE hydrants SET region=%s, flow_rate=%s, operational=%s, longitude=%s, latitude=%s WHERE id=%s"
    cur.execute(sql, (region, flow_rate, operational, longitude, latitude, id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_hydrants'))

@app.route('/hydrants/delete/<int:id>', methods=['POST'])
def delete_hydrant(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM hydrants WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('get_hydrants'))

if __name__ == '__main__':
    app.run(debug=True)
