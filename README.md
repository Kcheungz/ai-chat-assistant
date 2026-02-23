StudyAssistant – Desktop AI Study Tool

StudyAssistant is a Windows desktop application built with Python and Tkinter that uses the OpenAI API to generate structured explanations and quiz-style study questions.

The project demonstrates modular application design, secure credential handling, API integration, and packaging a Python GUI into a distributable Windows executable.

Overview

StudyAssistant allows users to:

• Generate structured explanations for technical or academic topics
• Create multiple-choice quiz questions with correct answers and rationales
• Securely store their own OpenAI API key locally

The application is packaged as a standalone .exe using PyInstaller and requires no Python installation for end users.

Key Technical Highlights

• Modular architecture (services, models, prompts, API client separation)
• Structured API request handling and JSON response parsing
• Secure credential storage using Windows Credential Manager (via keyring)
• Tkinter-based desktop GUI
• Packaged as a single-file Windows executable

This project demonstrates clean separation of concerns, proper packaging practices, and user-focused application design.

How It Works

On first launch, the application prompts the user to enter their OpenAI API key.

The key is stored securely in Windows Credential Manager and is not bundled with the application.

Subsequent launches use the stored key automatically.

Users can update or clear their key through:

Settings → Change API Key
Settings → Clear API Key

Features
Topic Explanation

Enter a topic and receive a structured, readable explanation.

Quiz Generation

Generate multiple-choice questions by:

Selecting number of questions

Choosing difficulty (easy, medium, hard)

Viewing correct answers with rationales

Running the Application

Download StudyAssistant.exe

Double-click to launch

Enter your OpenAI API key when prompted

Begin generating explanations or quizzes

Developer Notes
Running from Source

Create and activate a virtual environment:

python -m venv .venv
.venv\Scripts\activate

Install dependencies:

pip install -e .

Run locally:

python -m assistant.gui

Building the Windows Executable

Create a launcher file in the project root named run_gui.py:

from assistant.gui import App

if **name** == "**main**":
App().mainloop()

Build the executable:

pyinstaller --onefile --windowed -n StudyAssistant --paths src --collect-submodules assistant --collect-submodules keyring run_gui.py

The executable will be located in the dist folder.

Architecture Summary

src/assistant/
gui.py – Tkinter GUI interface
openai_client.py – Encapsulated OpenAI API wrapper
services/ – Business logic layer
models.py – Structured request/response models
prompts.py – Prompt templates
utils/ – Credential handling and error management

Security

• The application does not contain or ship with an API key
• Each user provides their own key
• Keys are stored securely via OS-level credential storage
• No secrets are committed to the repository

StudyAssistant demonstrates practical software engineering concepts including API integration, modular design, secure secret handling, and executable packaging for distribution.
