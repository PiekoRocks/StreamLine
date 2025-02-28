from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="classmysql.engr.oregonstate.edu",
    user="cs340_diaztr",
    password="7663",
    database="cs340_diaztr"
)

# Enable dictionary mode for easy access to query results
cursor = db.cursor(dictionary=True)


@app.route('/hydrants')
def show_hydrants():
    cursor.execute("SELECT * FROM Hydrants")
    hydrants = cursor.fetchall()
    return render_template('hydrants.html', hydrants=hydrants)


# Route to add a new hydrant
@app.route('/add_hydrant', methods=['POST'])
def add_hydrant():
    region = request.form['region']
    flow_rate = request.form['flow_rate']
    operational = request.form['operational']
    longitude = request.form['longitude']
    latitude = request.form['latitude']

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat) VALUES (%s, %s, %s, %s, %s)",
        (region, flow_rate, operational, longitude, latitude)
    )
    db.commit()
    return redirect(url_for('show_hydrants'))

# Route to update a hydrant
@app.route('/edit_hydrant/<int:id>', methods=['POST'])
def edit_hydrant(id):
    region = request.form['region']
    flow_rate = request.form['flow_rate']
    operational = request.form['operational']
    longitude = request.form['longitude']
    latitude = request.form['latitude']

    cursor = db.cursor()
    cursor.execute(
        "UPDATE Hydrants SET region_id=%s, flow_rate=%s, is_operational=%s, gps_long=%s, gps_lat=%s WHERE hydrant_id=%s",
        (region, flow_rate, operational, longitude, latitude, id)
    )
    db.commit()
    return redirect(url_for('show_hydrants'))

# Route to delete a hydrant
@app.route('/delete_hydrant/<int:id>', methods=['POST'])
def delete_hydrant(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Hydrants WHERE hydrant_id = %s", (id,))
    db.commit()
    return redirect(url_for('show_hydrants'))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5200)

@app.route('/test_db')
def test_db():
    try:
        cursor.execute("SELECT 'MySQL is working for cs340_diaztr!' AS message")
        result = cursor.fetchone()
        return f"MySQL Results: {result['message']}"
    except Exception as e:
        return f"Database Connection Error: {e}"

@app.route('/hydrants')
def show_hydrants():
    cursor.execute("SELECT * FROM Hydrants")
    hydrants = cursor.fetchall()
    return render_template('hydrants.html', hydrants=hydrants)

@app.route('/regions')
def show_regions():
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    return render_template('regions.html', regions=regions)

@app.route('/inspections')
def show_inspections():
    cursor.execute("SELECT * FROM Inspections")
    inspections = cursor.fetchall()
    return render_template('inspections.html', inspections=inspections)

@app.route('/workers')
def show_workers():
    cursor.execute("SELECT * FROM Workers")
    workers = cursor.fetchall()
    return render_template('workers.html', workers=workers)

@app.route('/maintenance')
def show_maintenance():
    cursor.execute("SELECT * FROM Maintenance")
    maintenance = cursor.fetchall()
    return render_template('maintenance.html', maintenance=maintenance)

@app.route('/workers_inspections')
def show_workers_inspections():
    cursor.execute("SELECT * FROM Workers_Inspections")
    workers_inspections = cursor.fetchall()
    return render_template('workers_inspections.html', workers_inspections=workers_inspections)

@app.route('/hydrants_inspections')
def show_hydrants_inspections():
    cursor.execute("SELECT * FROM Hydrants_Inspections")
    hydrants_inspections = cursor.fetchall()
    return render_template('hydrants_inspections.html', hydrants_inspections=hydrants_inspections)

