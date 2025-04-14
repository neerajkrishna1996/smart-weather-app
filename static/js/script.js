// DOM Elements
const cityInput = document.getElementById("city");
const suggestionsBox = document.getElementById("suggestions");
const locationBtn = document.getElementById("locationBtn");
const weatherInfo = document.getElementById("weatherInfo");
const errorMsg = document.getElementById("error");

// Geoapify API Key (replace with yours)
const GEOAPIFY_KEY = "YOUR_GEOAPIFY_API_KEY";

// Autocomplete: Suggest city names while typing
cityInput.addEventListener("input", async () => {
  const query = cityInput.value;
  if (query.length < 2) {
    suggestionsBox.style.display = "none";
    return;
  }

  const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${query}&limit=5&apiKey=${GEOAPIFY_KEY}`;
  const res = await fetch(url);
  const data = await res.json();

  suggestionsBox.innerHTML = "";
  data.features.forEach((feature) => {
    const suggestion = document.createElement("div");
    suggestion.textContent = feature.properties.formatted;
    suggestion.addEventListener("click", () => {
      cityInput.value = feature.properties.formatted;
      suggestionsBox.style.display = "none";
    });
    suggestionsBox.appendChild(suggestion);
  });
  suggestionsBox.style.display = "block";
});

// Search on Enter key
cityInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    fetchWeather(cityInput.value);
  }
});

// Search button click
document.getElementById("searchBtn").addEventListener("click", () => {
  fetchWeather(cityInput.value);
});

// Use my location button
locationBtn.addEventListener("click", () => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const { latitude, longitude } = position.coords;
      try {
        const res = await fetch(`/get_weather_by_coords?lat=${latitude}&lon=${longitude}`);
        const data = await res.json();
        displayWeather(data);
      } catch (err) {
        showError("Failed to fetch weather by location.");
      }
    });
  } else {
    showError("Geolocation is not supported by your browser.");
  }
});

// Fetch weather by city name or pincode
async function fetchWeather(query) {
  if (!query) return showError("Please enter a city or pincode");
  try {
    const res = await fetch(`/get_weather?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    displayWeather(data);
  } catch (err) {
    showError("Failed to fetch weather. Try again.");
  }
}

// Display weather data
function displayWeather(data) {
  if (data.error) return showError(data.error);

  errorMsg.style.display = "none";
  suggestionsBox.style.display = "none";

  const {
    city,
    temperature,
    humidity,
    wind_speed,
    precipitation,
    weather_summary,
    icon
  } = data;

  weatherInfo.innerHTML = `
    <div class="weather-card">
      <h2>${city}</h2>
      <img src="https://openweathermap.org/img/wn/${icon}@2x.png" alt="weather icon" />
      <p><strong>${weather_summary}</strong></p>
      <p>🌡️ Temperature: ${temperature} °C</p>
      <p>💧 Humidity: ${humidity}%</p>
      <p>🌬️ Wind Speed: ${wind_speed} m/s</p>
      <p>🌧️ Precipitation Chance: ${precipitation}%</p>
    </div>
  `;
}

// Show error message
function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.style.display = "block";
}