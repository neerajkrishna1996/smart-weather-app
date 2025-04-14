const searchInput = document.getElementById('searchInput');
const suggestions = document.getElementById('suggestions');
const searchBtn = document.getElementById('searchBtn');
const locationBtn = document.getElementById('locationBtn');

const apiKey = 'YOUR_GEOAPIFY_API_KEY';  // Replace with your Geoapify API key

searchInput.addEventListener('input', async () => {
  const query = searchInput.value.trim();
  if (query.length < 2) {
    suggestions.innerHTML = '';
    return;
  }

  const response = await fetch(`https://api.geoapify.com/v1/geocode/autocomplete?text=${query}&limit=5&apiKey=${apiKey}`);
  const data = await response.json();

  suggestions.innerHTML = '';
  data.features.forEach(place => {
    const div = document.createElement('div');
    div.textContent = place.properties.formatted;
    div.classList.add('suggestion-item');
    div.addEventListener('click', () => {
      searchInput.value = place.properties.city || place.properties.name || place.properties.postcode;
      suggestions.innerHTML = '';
    });
    suggestions.appendChild(div);
  });
});

searchBtn.addEventListener('click', () => {
  const query = searchInput.value.trim();
  if (query !== '') {
    window.location.href = `/search?query=${encodeURIComponent(query)}`;
  }
});

locationBtn.addEventListener('click', () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      window.location.href = `/location?lat=${lat}&lon=${lon}`;
    }, () => {
      alert("Location access denied.");
    });
  } else {
    alert("Geolocation not supported by this browser.");
  }
});
