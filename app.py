from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, static_folder="static", static_url_path="/static")

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
    
app = Flask(__name__)

# Enable dictionary mode for easy access to query results
# conn = get_db_connection()
# cursor = conn.cursor(dictionary=True)

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

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Hydrants (region_id, flow_rate, is_operational, gps_long, gps_lat) VALUES (%s, %s, %s, %s, %s)",
            (region, flow_rate, int(operational), longitude, latitude)
        )
        conn.commit()
        print("✅ Hydrant added successfully")
    except Exception as e:
        print(f"❌ Error adding hydrant: {e}")
        return "Error adding hydrant", 500
    finally:
        cursor.close()
        conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor()

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
    conn.commit()

    print("Hydrant update committed successfully")

    return redirect(url_for('show_hydrants'))

# ================== DELETE HYDRANT ==================
# Route to delete a hydrant
@app.route('/delete_hydrant/<int:id>', methods=['POST'])
def delete_hydrant(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Hydrants WHERE hydrant_id = %s", (id,))
    conn.commit()
    return redirect(url_for('show_hydrants'))

# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_db')
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 'MySQL is working for cs340_diaztr!' AS message")
        result = cursor.fetchone()
        return f"MySQL Results: {result['message']}"
    except Exception as e:
        return f"Database Connection Error: {e}"

# ================== SHOW HYDRANT ==================
@app.route('/hydrants')
def show_hydrants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Regions")
    regions = cursor.fetchall()
    cursor.close()
    conn.close()
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Inspections")
    inspections = cursor.fetchall()
    cursor.close()
    conn.close()
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


@app.route('/workers')
def workers():
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

    return render_template('workers.html', workers=workers, regions=regions)

# ================== SHOW WORKERS ==================
@app.route('/workers')
def show_workers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Workers")
    workers = cursor.fetchall()
    cursor.close()
    conn.close()
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
@app.route('/add_worker', methods=['POST'])
def add_worker():
    region_id = request.form['region']
    name = request.form['name']
    salary = request.form['salary']
    assigned_date = request.form['assigned_date']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the new worker directly
        cursor.execute("""
            INSERT INTO Workers (region_id, name, salary, assigned_date)
            VALUES (%s, %s, %s, %s)
        """, (region_id, name, salary, assigned_date))
        conn.commit()
    except Exception as e:
        print("Error adding worker:", e)
        return "Error adding worker", 500
    finally:
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

@app.route("/maintenance")
def maintenance():
    return redirect(url_for("list_maintenance"))

# ================== SHOW MAINTENANCE ==================
@app.route('/maintenance')
def show_maintenance():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Maintenance_Logs")
    maintenance = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('maintenance.html', maintenance=maintenance)

# ================== LIST MAINTENANCE ==================
# List Maintenance Records
@app.route('/list_maintenance')
def list_maintenance():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Maintenance_Logs")
    maint_logs = cursor.fetchall()

    cursor.execute("SELECT hydrant_id FROM Hydrants ORDER BY hydrant_id ASC")
    hydrants = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("maintenance.html", maint_logs=maint_logs, hydrants=hydrants)

# ================== ADD MAINTENANCE ==================
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

# ================== EDIT MAINTENANCE ==================
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

# ================== DELETE MAINTENANCE ==================
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

# ================== SHOW HYDRANT INSPECTIONS ==================
# ----------------------------------------------------------------
# READ: Display all hydrant inspection records
# ----------------------------------------------------------------
@app.route('/hydrants_inspections')
def show_hydrants_inspections():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch hydrant inspections
    cursor.execute("SELECT * FROM Hydrants_Inspections")
    hydrants_inspections = cursor.fetchall()

    # Fetch hydrants and sort by hydrant_id
    cursor.execute("SELECT hydrant_id FROM Hydrants ORDER BY hydrant_id ASC")
    hydrants = cursor.fetchall()

    # Fetch inspections and sort by inspection_id
    cursor.execute("SELECT inspection_id, inspection_date FROM Inspections ORDER BY inspection_id ASC")
    inspections = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("hydrants_inspections.html", hydrants_inspections=hydrants_inspections, hydrants=hydrants, inspections=inspections)

# ================== ADD HYDRANT INSPECTIONS ==================
# ----------------------------------------------------------------
# CREATE: Add a new hydrant inspection record
# ----------------------------------------------------------------
@app.route('/add_hydrant_inspection', methods=['POST'])
def add_hydrant_inspection():
    hydrant_id = request.form.get('hydrant_id')
    inspection_id = request.form.get('inspection_id')
    
    if not hydrant_id or not inspection_id:
        return "Error: Missing form data", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Hydrants_Inspections (hydrant_id, inspection_id) VALUES (%s, %s)",
            (hydrant_id, inspection_id)
        )
        conn.commit()
    except Exception as e:
        print("Error adding hydrant inspection:", e)
        return "Error adding hydrant inspection", 500
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('show_hydrants_inspections'))

# ================== EDIT HYDRANT INSPECTIONS ==================
# ----------------------------------------------------------------
# UPDATE: Edit an existing hydrant inspection record using composite keys
# ----------------------------------------------------------------
@app.route('/edit_hydrant_inspection/<string:hydrant_id>/<string:inspection_id>', methods=['GET', 'POST'])
def edit_hydrant_inspection(hydrant_id, inspection_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        new_hydrant_id = request.form.get('hydrant_id')
        new_inspection_id = request.form.get('inspection_id')
        
        if not new_hydrant_id or not new_inspection_id:
            return "Error: Missing form data", 400
        
        try:
            cursor.execute(
                "UPDATE Hydrants_Inspections SET hydrant_id = %s, inspection_id = %s WHERE hydrant_id = %s AND inspection_id = %s",
                (new_hydrant_id, new_inspection_id, hydrant_id, inspection_id)
            )
            conn.commit()
        except Exception as e:
            print("Error updating hydrant inspection:", e)
            return "Error updating hydrant inspection", 500
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('show_hydrants_inspections'))
    else:
        cursor.execute(
            "SELECT * FROM Hydrants_Inspections WHERE hydrant_id = %s AND inspection_id = %s",
            (hydrant_id, inspection_id)
        )
        inspection_record = cursor.fetchone()
        cursor.close()
        conn.close()
        if inspection_record is None:
            return "Hydrant inspection not found", 404
        return render_template('edit_hydrant_inspection.html', inspection=inspection_record)

# ================== DELETE HYDRANT INSPECTIONS ==================
# ----------------------------------------------------------------
# DELETE: Remove a hydrant inspection record using composite keys
# ----------------------------------------------------------------
@app.route('/delete_hydrant_inspection/<string:hydrant_id>/<string:inspection_id>', methods=['POST'])
def delete_hydrant_inspection(hydrant_id, inspection_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM Hydrants_Inspections WHERE hydrant_id = %s AND inspection_id = %s",
            (hydrant_id, inspection_id)
        )
        conn.commit()
    except Exception as e:
        print("Error deleting hydrant inspection:", e)
        return "Error deleting hydrant inspection", 500
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('show_hydrants_inspections'))

# ================== WORKER INSPECTIONS ==================
# @app.route("/worker_inspections")
# def worker_inspections():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     # Worker_Inspections
#     cursor.execute("""
#         SELECT wi.worker_id, w.name AS worker_name, wi.inspection_id, i.inspection_date
#         FROM Workers_Inspections wi
#         JOIN Workers w ON wi.worker_id = w.worker_id
#         JOIN Inspections i ON wi.inspection_id = i.inspection_id
#     """)
#     worker_inspections = cursor.fetchall()

#     # Workers
#     cursor.execute("SELECT * FROM Workers")
#     workers = cursor.fetchall()

#     # Inspections
#     cursor.execute("SELECT * FROM Inspections")
#     inspections = cursor.fetchall()

#     # Debug prints
#     print("=== DEBUG DATA ===")
#     print("workers:", workers)
#     print("inspections:", inspections)
#     print("worker_inspections:", worker_inspections)

#     cursor.close()
#     conn.close()

#     return render_template(
#         "workers_inspections.html",
#         worker_inspections=worker_inspections,
#         workers=workers,
#         inspections=inspections
#     )


# ================== SHOW WORKER INSPECTIONS ==================
# @app.route('/workers_inspections')
# def show_workers_inspections():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Workers_Inspections")
#     workers_inspections = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('workers_inspections.html', workers_inspections=workers_inspections)

# ================== LIST WORKER INSPECTIONS ==================
@app.route('/workers_inspections')
def list_worker_inspections():
    # print("list_worker_inspections route hit")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT wi.worker_id, wi.inspection_id,
               w.name AS worker_name,
               i.inspection_date
        FROM Workers_Inspections wi
        JOIN Workers w ON wi.worker_id = w.worker_id
        JOIN Inspections i ON wi.inspection_id = i.inspection_id
    """)
    worker_inspections = cursor.fetchall()
    # print("Fetched worker_inspections:", worker_inspections)

    cursor.execute("SELECT worker_id, name FROM Workers")
    workers = cursor.fetchall()

    cursor.execute("SELECT inspection_id, inspection_date FROM Inspections")
    inspections = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'workers_inspections.html',
        worker_inspections=worker_inspections,
        workers=workers,
        inspections=inspections
    )


# ================== ADD WORKER INSPECTIONS ==================
# 3. ADD: Create a new worker-inspection record
@app.route('/workers_inspections/add', methods=['POST'])
def add_worker_inspection():
    worker_id = request.form['worker_id']
    inspection_id = request.form['inspection_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Workers_Inspections (worker_id, inspection_id) VALUES (%s, %s)",
        (worker_id, inspection_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_worker_inspections'))

# ================== EDIT WORKER INSPECTIONS ==================
# 4. EDIT: Update an existing worker-inspection record
#    Since Workers_Inspections uses a composite key (worker_id, inspection_id),
#    we delete the old row and insert a new one with the updated IDs.
@app.route('/workers_inspections/edit', methods=['POST'])
def edit_worker_inspection():
    original_worker_id = request.form['original_worker_id']
    original_inspection_id = request.form['original_inspection_id']

    new_worker_id = request.form['worker_id']
    new_inspection_id = request.form['inspection_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the old record
    cursor.execute(
        "DELETE FROM Workers_Inspections WHERE worker_id = %s AND inspection_id = %s",
        (original_worker_id, original_inspection_id)
    )

    # Insert the new record
    cursor.execute(
        "INSERT INTO Workers_Inspections (worker_id, inspection_id) VALUES (%s, %s)",
        (new_worker_id, new_inspection_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_worker_inspections'))

# ================== DELETE WORKER INSPECTIONS ==================
# 5. DELETE: Remove a worker-inspection record
@app.route('/workers_inspections/delete', methods=['POST'])
def delete_worker_inspection():
    worker_id = request.form['worker_id']
    inspection_id = request.form['inspection_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM Workers_Inspections WHERE worker_id = %s AND inspection_id = %s",
        (worker_id, inspection_id)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('list_worker_inspections'))

@app.route('/')
def home():
    return render_template('home.html')  # Ensure 'home.html' exists

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5892)
