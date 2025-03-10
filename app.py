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

def get_db_connection():
    return mysql.connector.connect(
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

# ================== ADD HYDRANT ==================
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


# ================== SHOW REGION ==================
@app.route('/regions')
def show_regions():
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    return render_template('regions.html', regions=regions)

# ================== ADD REGION ==================
@app.route('/add_region', methods=['POST'])
def add_region():
    county_name = request.form['county_name']
    region_name = request.form['region_name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Regions (county_name, region_name) VALUES (%s, %s)", (county_name, region_name))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_regions'))

# ================== EDIT REGION ==================
@app.route('/edit_region/<int:region_id>', methods=['POST'])
def edit_region(region_id):
    county_name = request.form['county_name']
    region_name = request.form['region_name']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Regions SET county_name = %s, region_name = %s WHERE region_id = %s",
                   (county_name, region_name, region_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_regions'))

# ================== DELETE REGION ==================
@app.route('/delete_region/<int:region_id>', methods=['POST'])
def delete_region(region_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete region (Hydrants & Workers will be deleted via CASCADE)
    cursor.execute("DELETE FROM Regions WHERE region_id = %s", (region_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('list_regions'))

# ================== LIST REGION ==================
@app.route('/regions')
def list_regions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Ensures results are dictionaries, not tuples
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('regions.html', regions=regions)

# ================== SHOW INSPECTIONS ==================
@app.route('/inspections')
def show_inspections():
    cursor.execute("SELECT * FROM Inspections")
    inspections = cursor.fetchall()
    return render_template('inspections.html', inspections=inspections)

# ================== LIST INSPECTIONS ==================
# LIST: Display all inspections
@app.route('/inspections')
def list_inspections():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Inspections")
    inspections = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inspections.html', inspections=inspections)

# ================== ADD INSPECTIONS ==================
# ADD: Create a new inspection record
@app.route('/add_inspection', methods=['POST'])
def add_inspection():
    inspection_date = request.form['inspection_date']
    status = request.form['status']
    note = request.form['notes']
    # Map status to boolean: Passed => True (1), Failed => False (0)
    inspection_completed = 1 if status == "Passed" else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Inspections (inspection_date, inspection_completed, note) VALUES (%s, %s, %s)",
        (inspection_date, inspection_completed, note)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_inspections'))

# ================== EDIT INSPECTIONS ==================
# EDIT: Update an existing inspection record
@app.route('/edit_inspection/<int:inspection_id>', methods=['POST'])
def edit_inspection(inspection_id):
    inspection_date = request.form['inspection_date']
    status = request.form['status']
    note = request.form['notes']
    inspection_completed = 1 if status == "Passed" else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Inspections SET inspection_date = %s, inspection_completed = %s, note = %s WHERE inspection_id = %s",
        (inspection_date, inspection_completed, note, inspection_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_inspections'))

# ================== DELETE INSPECTIONS ==================
# DELETE: Remove an inspection record
@app.route('/delete_inspection/<int:inspection_id>', methods=['POST'])
def delete_inspection(inspection_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Inspections WHERE inspection_id = %s", (inspection_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_inspections'))

# ================== SHOW WORKERS ==================
@app.route('/workers')
def show_workers():
    cursor.execute("SELECT * FROM Workers")
    workers = cursor.fetchall()
    return render_template('workers.html', workers=workers)

# ================== LIST WORKERS ==================
@app.route('/workers')
def list_workers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch workers
    cursor.execute("SELECT * FROM Workers")
    workers = cursor.fetchall()
    
    # Fetch regions for the dropdown
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Debug print to see if regions data is fetched
    print("Regions fetched:", regions)
    
    return render_template('workers.html', workers=workers, regions=regions)

# ================== ADD WORKERS ==================
# Add Worker
@app.route('/add_worker', methods=['POST'])
def add_worker():
    region_id = request.form['region']
    name = request.form['name']
    salary = request.form['salary']
    assigned_date = request.form['assigned_date']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Workers (region_id, name, salary, assigned_date) VALUES (%s, %s, %s, %s)",
        (region_id, name, salary, assigned_date)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_workers'))

# ================== EDIT WORKERS ==================
# Edit Worker
@app.route('/edit_worker/<int:worker_id>', methods=['POST'])
def edit_worker(worker_id):
    region_id = request.form['region']
    name = request.form['name']
    salary = request.form['salary']
    assigned_date = request.form['assigned_date']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Workers SET region_id = %s, name = %s, salary = %s, assigned_date = %s WHERE worker_id = %s",
        (region_id, name, salary, assigned_date, worker_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_workers'))

# ================== DELETE WORKERS ==================
# Delete Worker
@app.route('/delete_worker/<int:worker_id>', methods=['POST'])
def delete_worker(worker_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Workers WHERE worker_id = %s", (worker_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_workers'))

@app.route('/maintenance')
def show_maintenance():
    cursor.execute("SELECT * FROM Maintenance_Logs")
    maintenance = cursor.fetchall()
    return render_template('maintenance.html', maintenance=maintenance)

# List Maintenance Records
@app.route('/maintenance')
def list_maintenance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Maintenance_Logs")
    maint_logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('maintenance.html', maint_logs=maint_logs)

# Add Maintenance Record
@app.route('/add_maintenance', methods=['POST'])
def add_maintenance():
    hydrant_id = request.form['hydrant_id']
    cost = request.form['cost']
    # The form sends "Yes" or "No" for "needed"
    needed = request.form['needed']
    needed_val = 1 if needed == "Yes" else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Maintenance_Logs (maint_hydrant_id, maint_cost, maint_needed) VALUES (%s, %s, %s)",
        (hydrant_id, cost, needed_val)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_maintenance'))

# Edit Maintenance Record
@app.route('/edit_maintenance/<int:maintenance_id>', methods=['POST'])
def edit_maintenance(maintenance_id):
    hydrant_id = request.form['hydrant_id']
    cost = request.form['cost']
    needed = request.form['needed']
    needed_val = 1 if needed == "Yes" else 0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Maintenance_Logs SET maint_hydrant_id = %s, maint_cost = %s, maint_needed = %s WHERE maintenance_id = %s",
        (hydrant_id, cost, needed_val, maintenance_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_maintenance'))

# Delete Maintenance Record
@app.route('/delete_maintenance/<int:maintenance_id>', methods=['POST'])
def delete_maintenance(maintenance_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Maintenance_Logs WHERE maintenance_id = %s", (maintenance_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('list_maintenance'))


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
