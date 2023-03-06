import json
import time
import openai
import speech_recognition as sr
from gtts import gTTS
import subprocess

r = sr.Recognizer()
with open("openaisecret.js") as f:
    secrets = json.load(f)
    api_key = secrets["api_key"]
    
with sr.Microphone() as source:
    print("Parla ora!")
    audio = r.listen(source)

openai.api_key = api_key

def get_response(messages:list):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=messages,
        temperature = 1.0 # 0.0 - 2.0
    )
    return response.choices[0].message

def get_textfromspeach():
    try:
        text = r.recognize_google(audio, language= 'it-IT')
        text = text.lower()     
    except sr.UnknownValueError:
        text = "Non dire nulla aspeta che ti chieda qualcosa"
    except sr.RequestError as e:
        text = "Non si è capito quello che ho detto chiedimi di ripetere"
    
    return text

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "Sei un assistente virtuale chiamata JARVIS e parli italiano."}
    ]
    try:
        while True:
            #user_input = input("\nAlan: ")
            #user_input = input(f"\nAlan: {get_textfromspeach()}") 
            with sr.Microphone() as source:
                print("Parla ora!")
                audio = r.listen(source)
            
            user_input = get_textfromspeach()
            print(f"\nAlan: {user_input}")
            
            messages.append({"role": "user", "content": user_input})
            new_message = get_response(messages=messages)
            print(f"\nJ.A.R.V.I.S.: {new_message['content']}")
            tts = gTTS(text=new_message['content'], lang='it', slow=False)
            
            tts.save("tts_output_audio.mp3")
            #time.sleep(1)
            subprocess.run(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", "--qt-start-minimized", "-I", "dummy", "C:\\TEMP\\mdh\\js\\tts_output_audio.mp3", "--play-and-exit", "-q", "--rate=1.3"])

            messages.append(new_message)
    except KeyboardInterrupt:
        print("\nA presto!")
        tts = gTTS(text="A Presto!", lang='it')
        tts.save("tts_output_audio.mp3")
        subprocess.run(["C:\\Program Files\\VideoLAN\\VLC\\vlc.exe", "--qt-start-minimized", "-I", "dummy", "C:\\TEMP\\mdh\\js\\tts_output_audio.mp3", "--play-and-exit", "-q", "--rate=1.3"])
