# FastAPI Leaflet Map Application

A simple web application that displays geographic points on a Leaflet map, with data served from a FastAPI backend using SQLite database.

## Project Structure

```
my-first-app/
├── backend/              # FastAPI backend
│   ├── app/              # Application code
│   │   └── main.py       # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── seed_db.py        # Database seeding script
│   └── database.db       # SQLite database (created automatically)
├── frontend/             # Web frontend
│   ├── index.html        # Main HTML page
│   ├── style.css         # CSS styling
│   └── script.js         # JavaScript for map functionality
├── setup_and_run.sh      # Setup and run script
└── README.md             # This file
```

## Setup Instructions

### 1. Run the setup script

```bash
./setup_and_run.sh
```

This script will:
- Create a Python virtual environment in `backend/venv/`
- Activate the virtual environment
- Install required Python dependencies
- Seed the database with sample Danish cities
- Start the FastAPI server on `http://localhost:8000`

### 2. Alternative: Manual setup

If you prefer to set up manually:

```bash
# Create and activate virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Seed database
python seed_db.py

# Start FastAPI server
uvicorn app.main:app --reload
```

## Running the Application

### Backend
The FastAPI server runs on `http://localhost:8000` and provides these endpoints:

- `GET /api/points` - Retrieve all geographic points
- `POST /api/points` - Add a new geographic point

### Frontend
Open `frontend/index.html` in your web browser. The frontend will:

1. Load a Leaflet map centered on Denmark
2. Fetch data from the FastAPI backend
3. Display points as markers on the map
4. Show detailed information in popups when clicking markers

### API Testing
You can test the API directly:

```bash
# Get all points
curl http://localhost:8000/api/points

# Add a new point
curl -X POST http://localhost:8000/api/points \
  -H "Content-Type: application/json" \
  -d '{"name": "New City", "latitude": 55.0, "longitude": 10.0, "description": "Test location"}'
```

## Sample Data

The application includes sample data for major Danish cities:
- Copenhagen (Capital of Denmark)
- Aarhus (Second largest city)
- Odense (Third largest city)
- Aalborg (City in northern Denmark)
- Esbjerg (Port city in western Denmark)

## Technologies Used

- **Backend**: FastAPI, SQLite, Python
- **Frontend**: HTML5, CSS3, JavaScript, Leaflet.js
- **Mapping**: OpenStreetMap tiles via Leaflet

## Notes

- The virtual environment is created in the `backend/venv/` directory
- The SQLite database file is automatically created as `backend/database.db`
- CORS is enabled to allow frontend-backend communication
- The application uses environment variables for configuration (can be extended)
