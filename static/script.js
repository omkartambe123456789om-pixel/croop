// ✅ Ask for location when page loads
window.onload = function () {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocation, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
};

function sendLocation(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lat: lat, lon: lon })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById("soil").innerHTML = "❌ Error fetching data";
            console.error(data.details || data.error);
            return;
        }

        document.getElementById("soil").innerHTML =
            `pH: ${data.soil.ph}, Moisture: ${data.soil.moisture}, Type: ${data.soil.type}`;

        document.getElementById("weather").innerHTML =
            `🌡️ ${data.weather.temperature}°C, ${data.weather.condition}`;

        document.getElementById("crop").innerHTML = data.crop;
        document.getElementById("fertilizer").innerHTML = data.fertilizer;
        document.getElementById("irrigation").innerHTML = data.irrigation;
    })
    .catch(err => {
        console.error("Fetch failed", err);
        document.getElementById("soil").innerHTML = "❌ Failed to connect to server";
    });
}

function showError(error) {
    console.error(error);
    alert("❌ Location access denied. Please enable GPS to use this app.");
}
