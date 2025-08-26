## 🎙️ Personal Voice Assistant – Anika

- A Python-based desktop voice assistant for Windows.
- It listens to your voice commands and can perform tasks like opening apps, browsing the web, sending emails, telling jokes, reading system information, and more.

## 🚀 Features

- Speech recognition (understand your voice)
- Text-to-speech responses
- Open/close applications and websites
- Search Wikipedia & Google
- Send emails (via Gmail App Passwords)
- Tell jokes, date, and time

## 🛠️ Installation

Clone the repo:
- git clone https://github.com/akshayvink/Personal-Voice-Assistant-Desktop.git
- cd Personal-Voice-Assistant-Desktop


## Install required libraries:

pip install pyttsx3 speechrecognition wikipedia opencv-python pyjokes psutil

## 📧 Email Setup

If you want to use the email feature, Gmail requires an App Password:
Go to your Google Account → Security.
Enable 2-Step Verification.
Under App Passwords, generate one (choose "Other" → type voice-assistant).
Use that password in your script instead of your real Gmail password.

## ▶️ Usage
Run the assistant with:
python pythonautomation1.py


Then speak commands like:
“Open YouTube"
“Send email”
“Tell me a joke”
“What’s the time?”

## 📂 Project Structure
Personal-Voice-Assistant-Desktop/
│── pythonautomation1.py   # Main assistant script
│── README.md              # Documentation

## ⚠️ Notes
Works best on Windows.
Make sure your microphone is set up properly.
Do not upload your real email password to GitHub. Use app passwords.