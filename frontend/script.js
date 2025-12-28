document.addEventListener('DOMContentLoaded', function() {
    // Initialize the map centered on Denmark
    const map = L.map('map').setView([56.0, 10.0], 7);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Fetch data from FastAPI backend
    async function fetchPoints() {
        try {
            const response = await fetch('http://localhost:8000/api/points');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const points = await response.json();
            return points;
        } catch (error) {
            console.error('Error fetching points:', error);
            document.getElementById('status').textContent = 'Error loading data';
            return [];
        }
    }

    // Display points on the map
    function displayPoints(points) {
        // Clear existing markers
        map.eachLayer(function(layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // Add new markers
        points.forEach(point => {
            const marker = L.marker([point.latitude, point.longitude]).addTo(map);
            marker.bindPopup(`
                <b>${point.name}</b><br>
                ${point.description || ''}<br>
                Latitude: ${point.latitude.toFixed(4)}<br>
                Longitude: ${point.longitude.toFixed(4)}
            `);
        });

        document.getElementById('status').textContent = `${points.length} points loaded`;
    }

    // Load initial data
    async function loadData() {
        document.getElementById('status').textContent = 'Loading data...';
        const points = await fetchPoints();
        displayPoints(points);
    }

    // Event listeners
    document.getElementById('refresh-btn').addEventListener('click', loadData);

    // Initial load
    loadData();
});
