import sqlite3
import os
import random

# Sample cities with their coordinates
CITIES = [
    {"name": "Copenhagen", "latitude": 55.6761, "longitude": 12.5683, "description": "Capital of Denmark"},
    {"name": "Aarhus", "latitude": 56.1629, "longitude": 10.2039, "description": "Second largest city in Denmark"},
    {"name": "Odense", "latitude": 55.4038, "longitude": 10.4024, "description": "Third largest city in Denmark"},
    {"name": "Aalborg", "latitude": 57.0488, "longitude": 9.9194, "description": "City in northern Denmark"},
    {"name": "Esbjerg", "latitude": 55.4708, "longitude": 8.4515, "description": "Port city in western Denmark"},
]

# Use the same database path as main.py
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def seed_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Clear existing data
        cursor.execute("DELETE FROM points")

        # Insert sample cities
        for city in CITIES:
            cursor.execute(
                "INSERT INTO points (name, latitude, longitude, description) VALUES (?, ?, ?, ?)",
                (city['name'], city['latitude'], city['longitude'], city['description'])
            )

        conn.commit()
        conn.close()
        print(f"Database seeded with sample cities at {DB_PATH}!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise

if __name__ == "__main__":
    seed_database()
