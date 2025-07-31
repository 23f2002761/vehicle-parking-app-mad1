# Vehicle Parking App

A Flask-based web application for managing parking lots, reservations, and users.  
Features include:

- **User Dashboard**: Reserve parking slots, view parking history.
- **Admin Dashboard**: Manage parking lots, slots, users, and reservations.

---

## ✅ Features

- Secure Login & Registration (hashed passwords)
- Role-based dashboards (Admin/User)
- Parking lot and slot management
- Reservation history & cost calculation
- Search functionality for Admin

---

## 🔧 Requirements

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/vehicle-parking-app.git
   cd vehicle-parking-app
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows:venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Run the Application

1. **Set environment variables**
   ```bash
   export FLASK_APP=main.py       # On Windows: set FLASK_APP=main.py
   export FLASK_ENV=development   # Enables debug mode
   ```
2. Initialize the database
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
3. Run the file using python main.py
