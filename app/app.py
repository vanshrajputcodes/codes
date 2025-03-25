from flask import Flask, render_template, request, jsonify
import requests
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)
API_KEY = "6a699ef89cdea5e2ee7056efcd50fe39"  # Replace with your actual API key

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") != 200:
        return "City not found!"
    weather = response["weather"][0]["description"].capitalize()
    temp = response["main"]["temp"]
    return f"Weather in {city}: {weather}, Temperature: {temp}°C"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_weather", methods=["POST"])
def fetch_weather():
    city = request.form["city"]
    weather_info = get_weather(city)
    engine.say(weather_info)
    engine.runAndWait()
    return jsonify({"weather": weather_info})

@app.route("/voice_input", methods=["POST"])
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        engine.say("Please say the city name")
        engine.runAndWait()
        try:
            audio = recognizer.listen(source)
            city = recognizer.recognize_google(audio)
            weather_info = get_weather(city)
            engine.say(weather_info)
            engine.runAndWait()
            return jsonify({"weather": weather_info, "city": city})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"})
        except sr.RequestError:
            return jsonify({"error": "Could not request results"})

if __name__ == "__main__":
    app.run(debug=True)
