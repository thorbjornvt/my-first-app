from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
from typing import List, Optional

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup - use absolute path to ensure correct location
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')

def get_db_connection():
    # Ensure the database directory exists
    db_dir = os.path.dirname(DB_PATH)
    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    try:
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Pydantic models
class PointCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None

class PointResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print("Application started successfully")

@app.get("/api/points", response_model=List[PointResponse])
async def get_points():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM points")
    points = cursor.fetchall()
    conn.close()

    return [
        PointResponse(
            id=row['id'],
            name=row['name'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            description=row['description']
        ) for row in points
    ]

@app.post("/api/points", response_model=PointResponse)
async def create_point(point: PointCreate):
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO points (name, latitude, longitude, description) VALUES (?, ?, ?, ?)",
        (point.name, point.latitude, point.longitude, point.description)
    )
    conn.commit()
    point_id = cursor.lastrowid
    conn.close()

    return PointResponse(
        id=point_id,
        name=point.name,
        latitude=point.latitude,
        longitude=point.longitude,
        description=point.description
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
