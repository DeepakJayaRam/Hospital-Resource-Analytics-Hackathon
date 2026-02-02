import psycopg2
import subprocess
import os
import sys

# ---------------- CONFIGURATION ----------------
# Update with your actual database password!
DB_CONFIG = {
    "dbname": "hospital_db",
    "user": "postgres",
    "password": "password",  # <--- CHANGE THIS IF NEEDED
    "host": "localhost"
}
# -----------------------------------------------

def run_schema_reset():
    """Drops all tables and re-creates them using schema.sql"""
    print("\n[Step 1/3] Resetting Database Schema...")
    
    # Locate schema file (Checks 'database' folder first, then root)
    schema_path = "database/schema.sql"
    if not os.path.exists(schema_path):
        schema_path = "schema.sql"
        
    if not os.path.exists(schema_path):
        print(f"❌ Error: Could not find 'schema.sql'. Make sure it exists.")
        sys.exit(1)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        with open(schema_path, "r") as f:
            sql_commands = f.read()
            cur.execute(sql_commands)
            
        conn.commit()
        conn.close()
        print("✅ Tables dropped and recreated successfully.")
    except Exception as e:
        print(f"❌ Database Error: {e}")
        sys.exit(1)

def run_data_generation():
    """Runs the Excel generation script"""
    print("\n[Step 2/3] Generating Fresh Excel Data...")
    try:
        # Calls the script you created earlier
        subprocess.run([sys.executable, "generate_excel.py"], check=True)
        print("✅ 'hospital_data.xlsx' created.")
    except subprocess.CalledProcessError:
        print("❌ Error: generate_excel.py failed. Does the file exist?")
        sys.exit(1)

def run_data_import():
    """Runs the Import script to load Excel into DB"""
    print("\n[Step 3/3] Importing Data into PostgreSQL...")
    try:
        # Calls the bridge script
        subprocess.run([sys.executable, "import_excel_to_db.py"], check=True)
        print("✅ Data successfully loaded into Database.")
    except subprocess.CalledProcessError:
        print("❌ Error: import_excel_to_db.py failed.")
        sys.exit(1)

if __name__ == "__main__":
    print("==========================================")
    print("   🏥 OPSPULSE: DATABASE FACTORY RESET    ")
    print("==========================================")
    
    run_schema_reset()
    run_data_generation()
    run_data_import()
    
    print("\n✨ SYSTEM READY! You can now start the backend.")
    print("==========================================")