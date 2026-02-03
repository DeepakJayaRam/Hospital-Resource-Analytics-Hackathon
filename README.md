This README is your project's "Sales Pitch." Judges often read this before they even look at your code. A clean, professional README can be the tie-breaker.

Create a file named **`README.md`** in your root folder and paste this **exact** markdown code.

---

# 🏥 OpsPulse: Hospital Resource Intelligence

### *Data-Driven Decisions. Better Patient Outcomes.*

---

## 🚨 The Problem

**Hospitals are data-rich but information-poor.**
Administrators struggle with:

1. **Invisible Bottlenecks:** Patients wait hours because bed availability is tracked on whiteboards, not real-time systems.
2. **Reactive Management:** Staffing decisions are made *after* a crisis hits, not predicted beforehand.
3. **Siloed Data:** Financial, clinical, and operational data exist in disconnected systems.

## 💡 The Solution: OpsPulse

**OpsPulse** is a real-time Central Command Dashboard that transforms static hospital logs into actionable intelligence. It ingests operational data, calculates critical KPIs (ALOS, Bed Occupancy), and uses an intelligent API layer to detect resource bottlenecks before they become critical.

---

## 🚀 Key Features (MVP)

* **Real-Time Occupancy Tracking:** Live visibility into bed status across all departments (Cardiology, ICU, Emergency).
* **Bottleneck Detection Engine:** Algorithms that auto-flag departments where Occupancy > 85% or ALOS exceeds standards.
* **Patient Outcome Analytics:** Correlation analysis between *Wait Times* and *Recovery Rates*.
* **Crisis Simulation Mode:** A built-in "Chaos Monkey" feature to simulate sudden patient surges for stress-testing.

---

## 🛠️ Tech Stack

* **Backend Intelligence:** Python, FastAPI (High-performance Async API)
* **Database:** PostgreSQL (Relational integrity for complex healthcare data)
* **Data Processing:** Pandas, SQLAlchemy
* **Visualization:** Microsoft Power BI / Apache Superset
* **Deployment:** Local On-Premise (Secure & Compliant)

---

## ⚙️ Installation & Setup

Follow these steps to deploy the OpsPulse engine locally.

### 1. Prerequisites

* Python 3.9+
* PostgreSQL (Running on `localhost:5432`)

### 2. Install Dependencies

```bash
pip install -r backend/requirements.txt

```

### 3. Initialize the System (Factory Reset)

We have built a single utility script that:

1. Wipes and Rebuilds the Database Schema.
2. Generates fresh Mock Data (Excel).
3. Loads data into PostgreSQL.

```bash
python reset_db.py

```

*Output: "✨ SYSTEM READY! You can now start the backend."*

### 4. Start the Intelligence Engine

```bash
uvicorn backend.main:app --reload

```

* The API will launch at: `http://127.0.0.1:8000`
* Interactive Documentation: `http://127.0.0.1:8000/docs`

---

## 📊 Dashboard Setup (Power BI)

1. Open **Power BI Desktop**.
2. Click **Get Data** -> **PostgreSQL Database**.
3. Server: `localhost` | Database: `hospital_db`.
4. Import tables: `admissions`, `departments`, `doctors`, `patients`.
5. *Optional:* Connect to the API endpoints (`/kpi/bottlenecks`) via Web Connector for live alerts.

---

## 🧪 Live Demo Scenario

**OpsPulse includes a "Crisis Trigger" for live demonstrations.**

1. **Status Quo:** The dashboard shows normal operations (Green indicators).
2. **The Trigger:** Send a POST request to the simulation endpoint:
```http
POST http://127.0.0.1:8000/demo/trigger_surge

```


3. **The Impact:**
* Simulates a mass casualty event (15+ Emergency admissions instantly).
* **Refresh the Dashboard:** See "Emergency Dept" occupancy spike to **Critical (Red)**.
* Demonstrates the system's real-time responsiveness.



---

## 📂 Project Structure

```
opspulse/
├── backend/
│   ├── main.py             # FastAPI Application (The Brain)
│   └── requirements.txt    # Dependencies
├── database/
│   ├── schema.sql          # Database Blueprint
│   ├── reset_db.py         # Master Setup Script
│   ├── generate_excel.py   # Data Generator
│   └── import_excel_to_db.py # ETL Pipeline
└── README.md               # You are here

```

---

### ⚖️ Compliance & Constraints

* ✅ **No Cloud SaaS:** 100% Localhost deployment.
* ✅ **Granularity:** Hourly timestamps on admissions.
* ✅ **Privacy:** No real patient data used (Faker library generation).
* ✅ **Stack:** Adheres to Python/SQL/BI Tool requirement.

---

### 👨‍💻 Team

* **Lead Architect:** Deepak Jaya Ram Yadav