from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import random

# ================= CONFIGURATION =================
# Update this to match your actual database credentials
DB_CONFIG = {
    "dbname": "hospital_db",
    "user": "postgres",
    "password": "password",  # <--- MAKE SURE THIS MATCHES YOUR INSTALLATION
    "host": "localhost"
}

# Initialize the API
app = FastAPI(
    title="OpsPulse Hospital Intelligence",
    description="Real-time analytics engine for hospital resource optimization.",
    version="1.0.0"
)

# Enable CORS (Allows external tools to talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= DATABASE HELPER =================
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        raise HTTPException(status_code=500, detail="Database Connection Failed")

# ================= ENDPOINTS =================

@app.get("/")
def health_check():
    """Heartbeat check to see if system is running."""
    return {
        "status": "online", 
        "system": "OpsPulse Hospital Engine", 
        "timestamp": datetime.now()
    }

@app.get("/kpi/occupancy")
def get_occupancy():
    """
    CRITICAL KPI: Calculates real-time bed occupancy percentage per department.
    Used for the Main Dashboard Overview.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Logic: Count ACTIVE admissions (where discharge_date is NULL) vs Total Beds
    query = """
    SELECT 
        d.name as department, 
        d.total_beds,
        COUNT(a.admission_id) as occupied_beds,
        ROUND((COUNT(a.admission_id)::decimal / d.total_beds) * 100, 1) as occupancy_rate
    FROM departments d
    LEFT JOIN admissions a ON d.dept_id = a.dept_id AND a.discharge_date IS NULL
    GROUP BY d.dept_id, d.name, d.total_beds
    ORDER BY occupancy_rate DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

@app.get("/kpi/bottlenecks")
def get_bottlenecks():
    """
    INTELLIGENCE LAYER: Identifies departments that are overloaded.
    This replaces manual analysis.
    """
    occupancy_data = get_occupancy()
    alerts = []
    
    for dept in occupancy_data:
        rate = dept['occupancy_rate']
        
        if rate >= 90:
            alerts.append({
                "severity": "CRITICAL",
                "department": dept['department'],
                "message": f"Capacity Critical ({rate}%). Divert ambulances immediately.",
                "action": "Initiate Code Yellow"
            })
        elif rate >= 75:
            alerts.append({
                "severity": "WARNING",
                "department": dept['department'],
                "message": f"High Load ({rate}%). Prepare overflow beds.",
                "action": "Review elective surgeries"
            })
            
    return {
        "alert_count": len(alerts),
        "status": "STABLE" if len(alerts) == 0 else "ATTENTION REQUIRED",
        "alerts": alerts
    }

@app.get("/kpi/alos")
def get_alos():
    """
    EFFICIENCY KPI: Average Length of Stay (ALOS) in days.
    Helps identify if doctors are keeping patients too long.
    """
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
    SELECT 
        d.name as department,
        ROUND(AVG(EXTRACT(DAY FROM (a.discharge_date - a.admission_date))), 1) as avg_stay_days
    FROM admissions a
    JOIN departments d ON a.dept_id = d.dept_id
    WHERE a.discharge_date IS NOT NULL
    GROUP BY d.name
    ORDER BY avg_stay_days DESC;
    """
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

# ================= THE "WINNING" DEMO FEATURE =================

@app.post("/demo/trigger_surge")
def trigger_surge_simulation():
    """
    MAGIC BUTTON: Simulates a sudden influx of 15 Emergency patients.
    Run this during your demo to make the dashboard turn RED instantly.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # 1. Find the 'Emergency' or 'General Medicine' department ID
        cur.execute("SELECT dept_id FROM departments WHERE name LIKE '%Emergency%' OR name LIKE '%General%' LIMIT 1")
        target_dept = cur.fetchone()[0]
        
        # 2. Find a doctor in that department
        cur.execute("SELECT doc_id FROM doctors WHERE dept_id = %s LIMIT 1", (target_dept,))
        target_doc = cur.fetchone()[0]
        
        # 3. Create 15 fake emergency patients instantly
        print("⚠️ TRIGGERING SURGE SIMULATION...")
        
        for i in range(15):
            # Create dummy patient
            cur.execute("""
                INSERT INTO patients (name, age, gender, city) 
                VALUES ('Emerg_Sim_Patient', 45, 'M', 'SimCity') 
                RETURNING patient_id
            """)
            new_pat_id = cur.fetchone()[0]
            
            # Admit them IMMEDIATELY (Active admission)
            cur.execute("""
                INSERT INTO admissions (patient_id, doc_id, dept_id, admission_date, admission_type, billing_amount)
                VALUES (%s, %s, %s, NOW(), 'Emergency', 0)
            """, (new_pat_id, target_doc, target_dept))
            
        conn.commit()
        conn.close()
        
        return {
            "status": "SIMULATION_COMPLETE", 
            "message": "⚠️ MASS CASUALTY EVENT SIMULATED: 15 New Critical Patients Admitted.",
            "impact": "Dashboard Occupancy should spike immediately."
        }
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Simulation Failed: {str(e)}")

# Run via terminal: uvicorn backend.main:app --reload