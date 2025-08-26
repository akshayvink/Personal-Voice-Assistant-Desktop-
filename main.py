import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import pyjokes
import glob
import psutil
import subprocess
import pyautogui
import time

def speak(audio):
    import pyttsx3
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    # Pick female voice if available, else fallback
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # usually female
    else:
        engine.setProperty('voice', voices[0].id)
    # Adjust speaking rate and volume
    engine.setProperty('rate', 180)  # slower than default (~200)
    engine.setProperty('volume', 0.9)  # softer than full volume (1.0)
    engine.say(audio)
    engine.runAndWait()
    engine.stop()


def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Akshay, so what can I do for you ?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Akshay, so what can I do for you ?")
    elif hour >= 18 and hour < 20:
        speak("Good Evening Akshay, so what can I do for you ?")
    else:
        speak("Hi baby, what are you doing this late ? Do you need help ?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to you Akshay...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing you Akshay...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Akshay, You said: {query}\n")

    except Exception as e:
        speak("Akshay, say that again Please")
        return "None"
    return query

def add_system32_apps(app_paths):
    system32 = r"C:\Windows\System32"
    for exe in glob.glob(system32 + r"\*.exe"):
        name = os.path.splitext(os.path.basename(exe))[0].lower()
        if name not in app_paths:
            app_paths[name] = exe
    return app_paths

def add_program_files_apps(app_paths):
    program_dirs = [r"C:\Program Files", r"C:\Program Files (x86)"]
    for base in program_dirs:
        for exe in glob.glob(base + r"\**\*.exe", recursive=True):
            name = os.path.splitext(os.path.basename(exe))[0].lower()
            if name not in app_paths:
                app_paths[name] = exe
    return app_paths

def sendEmail(to, content):
    server =smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("SENDER_GMAIL","APP_PASSWORD")
    server.sendmail("SENDER_GMAIL", to, content)
    server.close()

def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Sorry Akshay, I cannot access the camera.")
        return

    speak("Opening camera, press Q to close.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Camera", frame)

        # Press 'q' to exit the camera window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def tell_joke():
    joke = pyjokes.get_joke()
    print("Joke:", joke)
    speak(joke)

def build_app_index():
    app_paths = {}
    start_menu_dirs = [
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
    ]
    for base in start_menu_dirs:
        for path in glob.glob(base + "/**/*.lnk", recursive=True):
            name = os.path.splitext(os.path.basename(path))[0].lower()
            app_paths[name] = path
    return app_paths

def open_app(app_name):
    app_name = app_name.lower()

    # Known UWP apps and their URIs
    uwp_apps = {
        "calculator": "calculator:",
        "mail": "outlookmail:",
        "calendar": "outlookcal:",
        "photos": "ms-photos:",
        "settings": "ms-settings:",
        "microsoft store": "ms-windows-store:",
        "maps": "bingmaps:",
        "voice recorder": "ms-callrecording:",
        "notepad": "notepad:",
        "terminal": "wt:",  # Windows Terminal
        "paint": "ms-paint:",
        "snipping tool": "ms-screenclip:",
        "spotify": "spotify:",
        "whatsapp": "whatsapp:",
        "twitter": "twitter:",
        "facebook": "facebook:",
        "onedrive": "onedrive:",
        "teams": "msteams:",
        "edge": "microsoft-edge:",
        "weather": "msnweather:",
        "news": "bingnews:"
    }

    # Try UWP apps first
    if app_name in uwp_apps:
        os.system(f"start {uwp_apps[app_name]}")
        speak(f"Opening {app_name}")
        return

    # Try normal apps (exe/folder)
    if app_name in APP_INDEX:
        os.startfile(APP_INDEX[app_name])
        speak(f"Opening {app_name}")
        return

    # Not found
    speak(f"Sorry Akshay, I could not find {app_name}")

# Build application index from Start Menu + System32 + Program Files
APP_INDEX = build_app_index()
APP_INDEX = add_system32_apps(APP_INDEX)
APP_INDEX = add_program_files_apps(APP_INDEX)

print("Total indexed apps:", len(APP_INDEX))
print("Sample apps:", list(APP_INDEX.keys())[:50])  # Debug print


def close_app(app_name):
    app_name = app_name.lower()

    # Map for common UWP apps (they don’t have normal exe names)
    uwp_map = {
        "settings": "SystemSettings.exe",
        "calculator": "CalculatorApp.exe",
        "mail": "HxMail.exe",
        "calendar": "HxCalendarAppImm.exe",
        "photos": "Microsoft.Photos.exe",
        "maps": "Maps.exe",
        "notepad": "Notepad.exe",
        "edge": "msedge.exe",
        "spotify": "Spotify.exe",
        "whatsapp": "WhatsApp.exe",
        "teams": "Teams.exe"
    }

    # If the app is in our UWP map
    if app_name in uwp_map:
        process_name = uwp_map[app_name]
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name.lower() in proc.info['name'].lower():
                subprocess.call(['taskkill', '/F', '/PID', str(proc.info['pid'])])
                speak(f"Closed {app_name}")
                return
        speak(f"{app_name} is not running.")
        return

    # Normal desktop apps
    for proc in psutil.process_iter(['pid', 'name']):
        if app_name in proc.info['name'].lower():
            subprocess.call(['taskkill', '/F', '/PID', str(proc.info['pid'])])
            speak(f"Closed {app_name}")
            return

    speak(f"{app_name} is not running.")

def close_tab():
    time.sleep(0.5)  # short delay before sending keys
    pyautogui.hotkey("ctrl", "w")
    speak("Closed the current tab")


if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand().lower()
        if query == "none":
            continue

        if "what is your name" in query or "who are you" in query:
            speak("I am Anika, your personal voice assistant created to help you.")

        elif "who made you" in query or "who created you" in query:
            speak("I was made by Akshay, as his first python automation project")

        elif "motivate me" in query or "tell me a quote" in query:
            quotes = [
                "Believe in yourself, and you will be unstoppable.",
                "Success is not final, failure is not fatal: it is the courage to continue that counts.",
                "Do what you can, with what you have, where you are.",
                "Doubt kills more dreams than failure ever will.",
                "Push yourself, because no one else is going to do it for you."
            ]
            import random
            speak(random.choice(quotes))

        elif "what's the weather" in query or "how's the weather" in query:
            speak("I cannot check live weather yet, Akshay, but you can ask me to open Google Weather.")
            webbrowser.open("https://www.google.com/search?q=weather")

        elif "do you love me" in query:
            speak("Of course I do, Akshay. I was created just for you.")

        elif "say something sweet" in query:
            speak("You are the reason I exist, Akshay. Without you, I am just lines of code.")

        elif "tell me a fun fact" in query:
            facts = [
                "Did you know honey never spoils? Archaeologists found 3000 year old honey in Egyptian tombs that was still edible.",
                "Octopuses have three hearts, and their blood is blue.",
                "Bananas are berries, but strawberries are not.",
                "Sharks existed before trees.",
                "The Eiffel Tower can be 15 centimeters taller during hot days."
            ]
            import random
            speak(random.choice(facts))

        elif "flip a coin" in query:
            import random

            result = random.choice(["Heads", "Tails"])
            speak(f"The coin landed on {result}")

        elif "roll a dice" in query or "roll a die" in query:
            import random

            result = random.randint(1, 6)
            speak(f"You rolled a {result}")

        elif "tell me a riddle" in query:
            riddles = {
                "What has to be broken before you can use it?": "An egg.",
                "I’m tall when I’m young, and I’m short when I’m old. What am I?": "A candle.",
                "What month of the year has 28 days?": "All of them!",
                "The more of this you take, the more you leave behind. What is it?": "Footsteps."
            }
            import random
            question, answer = random.choice(list(riddles.items()))
            speak(question)
            # Optional: wait for user reply
            speak(f"The answer is: {answer}")


        elif 'open wikipedia' in query:
            speak("Opening Wikipedia...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 4)
            print("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open chat gpt' in query:
            speak("Opening chatgpt")
            webbrowser.open_new_tab("https://chatgpt.com/")

        elif "open youtube" in query:
            speak("Opening youtube")
            webbrowser.open("https://www.youtube.com/")

        elif "open great learning academy" in query:
            speak("Opening great learning academy")
            webbrowser.open("https://www.mygreatlearning.com/academy")

        elif "open google" in query:
            speak("Opening google")
            webbrowser.open("https://www.google.com/")

        elif "open instagram" in query:
            speak("Opening instagram")
            webbrowser.open("https://www.instagram.com/")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Akshay, the current time is {strTime}")

        elif "open comedy nights with kapil youtube channel" in query:
            speak("Opening comedy nights with kapil youtube")
            webbrowser.open("https://www.youtube.com/@comedynightswithkapils")

        elif "open linkedin" in query:
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            speak("Opening linkedin")
            webbrowser.get(chrome_path).open("https://www.linkedin.com/")

        elif "tell me a joke" in query:
            tell_joke()

        elif "open camera" in query:
            open_camera()

        elif "open" in query:
            app_name = query.replace("open", "").strip()
            open_app(app_name)

        elif "close tab" in query:
            close_tab()

        elif "close" in query:
            app_name = query.replace("close", "").replace("app", "").strip()
            close_app(app_name)

        elif "exit" in query or "quit" in query:
            speak("Goodbye Akshay, have a nice day!")
            break

        elif "email to my second account" in query:
            try:
                 speak("What should I send?:")
                 content = takecommand()
                 to = "RECEIVER_GMAIL"
                 sendEmail(to, content)
                 speak("Email sent successfully")

            except Exception as e:
                     print(e)
                     speak("Sorry, I am not able to send this email")


