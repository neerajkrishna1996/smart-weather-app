import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Step 1: Load data
df = pd.read_csv("weather.csv")
df.dropna(inplace=True)  # Remove rows with missing data

# Rename columns (change based on your dataset)
df.rename(columns={
    'Max TemperatureC': 'Temp',
    'Humidity': 'Humidity',
    'Wind SpeedKm/h': 'Wind',
    'Mean Sea Level PressurehPa': 'Pressure'
}, inplace=True)

# Features and label
X = df[['Humidity', 'Wind', 'Pressure']]
y = df['Temp']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the model to a file
joblib.dump(model, "weather_model.pkl")
print("✅ Model trained and saved as 'weather_model.pkl'")
