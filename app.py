from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="classmysql.engr.oregonstate.edu",
    user="cs340_diaztr",
    password="7663",
    database="cs340_diaztr",
    autocommit=True
)

# Enable dictionary mode for easy access to query results
cursor = db.cursor(dictionary=True)

print("Available Routes:")
print(app.url_map)

# ================== HYDRANT ==================
@app.route('/add_hydrant', methods=['POST'])
def add_hydrant():
    print("🚀 Received POST request to add hydrant")

    region = request.form.get('region')
    flow_rate = request.form.get('flow_rate')
    operational = request.form.get('operational')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')

    print(f"🛠 Received form data: region={region}, flow_rate={flow_rate}, operational={operational}, longitude={longitude}, latitude={latitude}")

    if not region or not flow_rate or not longitude or not latitude:
        print("❌ Missing form data!")
        return "Error: Missing form data", 400

    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat) VALUES (%s, %s, %s, %s, %s)",
            (region, flow_rate, int(operational), longitude, latitude)
        )
        db.commit()
        print("✅ Hydrant added successfully")
    except Exception as e:
        print(f"❌ Error adding hydrant: {e}")
        return "Error adding hydrant", 500

    return redirect(url_for('show_hydrants'))

# ================== EDIT HYDRANT ==================
@app.route('/edit_hydrant/<int:id>', methods=['POST'])
def edit_hydrant(id):
    region = request.form.get('region')
    flow_rate = request.form.get('flow_rate')
    operational = request.form.get('operational')
    longitude = request.form.get('longitude')
    latitude = request.form.get('latitude')

    if operational is None:
        operational = 0
    else:
        operational = int(operational)

    cursor = db.cursor()

    # Debugging: Print values before updating
    print(f"Updating hydrant {id} with values: {region}, {flow_rate}, {operational}, {longitude}, {latitude}")

    # Check if the hydrant exists
    cursor.execute("SELECT COUNT(*) FROM Hydrants WHERE hydrant_id = %s", (id,))
    exists = cursor.fetchone()[0]

    if exists == 0:
        return "Error: Hydrant does not exist.", 400

    # Check if the region ID is valid
    cursor.execute("SELECT COUNT(*) FROM Regions WHERE region_id = %s", (region,))
    region_exists = cursor.fetchone()[0]

    if region_exists == 0:
        return "Error: Region ID does not exist. Please choose a valid region.", 400

    # Perform update
    cursor.execute(
        "UPDATE Hydrants SET region_id=%s, flow_rate=%s, is_operational=%s, gps_long=%s, gps_lat=%s WHERE hydrant_id=%s",
        (region, flow_rate, operational, longitude, latitude, id)
    )
    db.commit()

    print("Hydrant update committed successfully")

    return redirect(url_for('show_hydrants'))

# ================== DELETE HYDRANT ==================
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

@app.route('/test_db')
def test_db():
    try:
        cursor.execute("SELECT 'MySQL is working for cs340_diaztr!' AS message")
        result = cursor.fetchone()
        return f"MySQL Results: {result['message']}"
    except Exception as e:
        return f"Database Connection Error: {e}"

# ================== SHOW HYDRANT ==================
@app.route('/hydrants')
def show_hydrants():
    cursor = db.cursor(dictionary=True)

    # Fetch hydrants
    cursor.execute("SELECT hydrant_id, region_id AS region, flow_rate, is_operational, gps_long AS longitude, gps_lat AS latitude FROM Hydrants")
    hydrants = cursor.fetchall()

    # Fetch available regions for the dropdown
    cursor.execute("SELECT region_id FROM Regions")
    regions = cursor.fetchall()

    cursor.close()

    return render_template("hydrants.html", hydrants=hydrants, regions=regions)


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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5892)
