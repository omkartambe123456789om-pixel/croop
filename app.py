import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔑 Replace with your real OpenWeather key
OPENWEATHER_KEY = "176134a0d234105b21107fa60e628c2f"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        lat = data.get("lat")
        lon = data.get("lon")

        # ✅ Weather API
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric"
        weather_res = requests.get(weather_url).json()

        if "main" not in weather_res:
            return jsonify({"error": "Weather API failed", "details": weather_res})

        temp = weather_res["main"]["temp"]
        desc = weather_res["weather"][0]["description"]

        # ✅ Dummy soil data (replace later with real ML model)
        soil = {
            "ph": 6.5,
            "moisture": "Medium",
            "type": "Loamy"
        }

        # ✅ Simple recommendations
        if temp > 30:
            crop = "Rice"
            irrigation = "Water daily"
            fertilizer = "NPK 20-20-20"
        else:
            crop = "Wheat"
            irrigation = "Water every 3 days"
            fertilizer = "Urea"

        result = {
            "soil": soil,
            "crop": crop,
            "fertilizer": fertilizer,
            "irrigation": irrigation,
            "weather": {
                "temperature": temp,
                "condition": desc
            }
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
