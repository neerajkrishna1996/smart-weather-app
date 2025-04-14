async function getWeather() {
    const input = document.getElementById('cityInput').value.trim();
    if (!input) return alert("Please enter city or pincode");

    const isPincode = /^\d+$/.test(input);

    const response = await fetch('/get_weather', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(isPincode ? { pincode: input } : { city: input })
    });

    const data = await response.json();
    displayWeather(data);
}

async function getLocation() {
    if (!navigator.geolocation) return alert("Geolocation not supported");

    navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        const response = await fetch('/location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lat: latitude, lon: longitude })
        });

        const data = await response.json();
        displayWeather(data);
    }, () => {
        alert("Unable to get location");
    });
}

function displayWeather(data) {
    const result = document.getElementById("weatherResult");
    if (data.error) {
        result.innerHTML = `<p>${data.error}</p>`;
        return;
    }

    const temp = data.main.temp;
    const humidity = data.main.humidity;
    const wind = data.wind.speed;
    const weather = data.weather[0].main;
    const description = data.weather[0].description;

    result.innerHTML = `
        <h2>${data.name}</h2>
        <p>Weather: ${weather} (${description})</p>
        <p>Temperature: ${temp} °C</p>
        <p>Humidity: ${humidity}%</p>
        <p>Wind Speed: ${wind} m/s</p>
    `;
}
