

import speech_recognition as sr
from googletrans import Translator
import requests
from PIL import Image
from io import BytesIO
import base64

# ============== CONFIG ====================
MONSTER_API_KEY = "PUT_YOUR_MONSTERAPI_KEY_HERE"   # <-- paste your key here
MODEL_ID = "dreamshaper"  # can be "realistic-vision" or other available models
# ==========================================

def listen_any_language():
    """Capture audio from mic in any language"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now... (any language)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        # Use Google speech API – automatic language detection
        text = recognizer.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
    except sr.RequestError as e:
        print("⚠️ Speech Recognition error:", e)
    return None

def translate_to_english(text):
    """Translate recognized text to English (MonsterAPI prompt works best in English)"""
    translator = Translator()
    try:
        result = translator.translate(text, dest='en')
        print(f"🌐 Translated to English: {result.text}")
        return result.text
    except Exception as e:
        print("⚠️ Translation error:", e)
        return text

def generate_image_monsterapi(prompt):
    """Send text prompt to MonsterAPI and get back an image"""
    print("🧠 Generating image for:", prompt)
    url = "https://api.monsterapi.ai/v1/generate"
    headers = {
        "Authorization": f"Bearer {MONSTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "prompt": prompt,
        "negative_prompt": "",
        "width": 512,
        "height": 512,
        "samples": 1,
        "num_inference_steps": 30,
        "guidance_scale": 7.5
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=60)
        res.raise_for_status()
        data = res.json()
        if "output" in data:
            image_base64 = data["output"][0]
            image_bytes = base64.b64decode(image_base64)
            img = Image.open(BytesIO(image_bytes))
            img.save("generated_image.png")
            print("✅ Image saved as generated_image.png")
            img.show()
        else:
            print("⚠️ Unexpected API response:", data)
    except Exception as e:
        print("❌ Error generating image:", e)

def main():
    print("🎨 Speech-to-Image Generator (MonsterAPI)\n")
    text = listen_any_language()
    if not text:
        print("No speech detected. Exiting.")
        return
    english_prompt = translate_to_english(text)
    generate_image_monsterapi(english_prompt)

if __name__ == "__main__":
    main()