# Voice Assistant for Voice Commands
# Features: Weather, News, Reminders, Voice Commands

import speech_recognition as sr
import pyttsx3
import threading
import time
import requests
import datetime
import traceback
import sys

try:
    import pywhatkit
    HAS_PYWHATKIT = True
except Exception:
    HAS_PYWHATKIT = False

# -----------------------
# CONFIG
# -----------------------
OPENWEATHER_API_KEY = "PUT_YOUR_OPENWEATHER_KEY_HERE"
NEWSAPI_KEY = "PUT_YOUR_NEWSAPI_KEY_HERE"

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

recognizer = sr.Recognizer()

def listen(timeout=5, phrase_time_limit=8):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("🎤 Listening...")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        text = recognizer.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        return None

def get_weather(city):
    if OPENWEATHER_API_KEY.startswith("PUT_"):
        return "⚠️ Add your OpenWeatherMap API key!"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={OPENWEATHER_API_KEY}"
    r = requests.get(url)
    data = r.json()
    if r.status_code == 200:
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"🌤 Weather in {city}: {desc}, {temp}°C."
    return "❌ City not found!"

def get_news():
    if NEWSAPI_KEY.startswith("PUT_"):
        return "⚠️ Add your NewsAPI key!"
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWSAPI_KEY}"
    r = requests.get(url)
    articles = r.json().get("articles", [])
    top5 = articles[:5]
    return "\n".join([f"{i+1}. {a['title']}" for i, a in enumerate(top5)])

reminders = []

def reminder_worker():
    while True:
        now = time.time()
        for r in reminders.copy():
            if r[0] <= now:
                speak(f"⏰ Reminder: {r[1]}")
                reminders.remove(r)
        time.sleep(1)

def set_reminder(seconds, message):
    reminders.append((time.time()+seconds, message))
    speak(f"Reminder set for {seconds} seconds: {message}")

def handle_command(cmd):
    if "weather" in cmd:
        city = "Delhi"
        if "in" in cmd:
            city = cmd.split("in")[-1].strip()
        speak(get_weather(city))
    elif "news" in cmd:
        speak("📰 Fetching latest news...")
        speak(get_news())
    elif "remind" in cmd:
        set_reminder(10, "Your reminder message!")
    elif "time" in cmd:
        speak(datetime.datetime.now().strftime("%I:%M %p"))
    elif "exit" in cmd or "quit" in cmd:
        speak("👋 Goodbye Mizbaul!")
        sys.exit()
    else:
        speak("Sorry, I didn’t understand. Try saying 'weather', 'news', or 'time'.")

def start_assistant():
    speak("Hello Mizbaul! I’m your voice assistant. How can I help?")
    threading.Thread(target=reminder_worker, daemon=True).start()
    while True:
        text = listen() or input("Type command: ").lower()
        handle_command(text)

if __name__ == "__main__":
    start_assistant()