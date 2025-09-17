import os
import sqlite3


def setup_database():
    """Initialize the database with required tables"""
    
    # Create database directory
    os.makedirs("data", exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect("data/solar_calculator.db")
    cursor = conn.cursor()
    # Create tables
    
    # User calculations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        latitude REAL,
        longitude REAL,
        budget REAL NOT NULL,
        daily_consumption_kwh REAL,
        system_cost REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        input_data TEXT,
        results TEXT
    )
    """)
    
    # Component feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS component_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component_type TEXT NOT NULL,
        component_model TEXT NOT NULL,
        rating INTEGER CHECK(rating >= 1 AND rating <= 5),
        feedback TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # System performance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_performance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_calculation_id INTEGER,
        actual_generation_kwh REAL,
        actual_consumption_kwh REAL,
        performance_ratio REAL,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_calculation_id) REFERENCES user_calculations (id)
    )
    """)
    
    # Commit changes and close
    conn.commit()
    conn.close()
    
    print("Database setup completed successfully!")

if __name__ == "__main__":
    setup_database()