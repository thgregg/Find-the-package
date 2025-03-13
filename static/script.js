let map = L.map('map').setView([43.5775, 1.3766], 13);
let userMovedMap = false;

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let trajectory = L.polyline([], { color: 'red' }).addTo(map);
let marker = L.marker([43.5775, 1.3766]).addTo(map);

map.on('dragstart', function () {
    userMovedMap = true;
});

function updateData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                let positions = data.map(p => [p.lat, p.lon]);

                trajectory.setLatLngs(positions);
                let lastPosition = positions[positions.length - 1];
                marker.setLatLng(lastPosition);

                if (!userMovedMap) {
                    map.setView(lastPosition);
                }
            }
        });
}

setInterval(updateData, 5000);
updateData();
