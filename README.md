# StudyAI – Personalized Student System

A command-line study planning application that stores student profiles and uses their subjects, marks, available study hours, preferred study time, and upcoming exam to support study planning. An optional Gemini-powered chat assistant can answer study questions using that profile context.

## Features

- Create, open, list, update, and delete student profiles.
- Store student data locally in `students_data.json`.
- Analyze marks to identify strongest and weakest subjects and flag subjects for improvement.
- Generate daily and weekly study timetables that allocate more time to lower-mark subjects.
- Ask the StudyAI chatbot for study, revision, exam preparation, and time-management guidance.
- Save chat history locally in `studyai_chats.json`.
- Migrate some older student and chat data formats when loading.

## Technology

- Python 3
- Python standard library: `os`, `json`, and `datetime`
- Optional Gemini integration through the `google-genai` package

## Requirements

- Python 3.9 or later recommended.
- Internet access and a valid Gemini API key to use the chatbot.
- The rest of the application runs locally and does not require third-party packages.

## Install and run

1. Install Python 3 if it is not already installed.
2. Save `MYFINALPROJECTFILE.py` in a folder where the program can create its data files.
3. (Optional, for chatbot) Install the Gemini client:

   ```bash
   python -m pip install google-genai
   ```

4. (Optional, for chatbot) Set `GEMINI_API_KEY` in your environment before starting the program. For PowerShell:

   ```powershell
   $env:GEMINI_API_KEY = "your_api_key_here"
   ```

   For Command Prompt:

   ```bat
   set GEMINI_API_KEY=your_api_key_here
   ```

5. Run the program from its folder:

   ```bash
   python MYFINALPROJECTFILE.py
   ```

6. Choose **1. Create New Student** and follow the prompts. Then choose **7** or **8** for timetables and **9** for the optional chatbot.

Student and chat JSON files are created beside the Python script. Keep them if you want to retain data between runs. Do not commit personal student records or API keys to a public repository.

## Testing instructions

The project currently has no automated test suite. You can check its core features manually:

1. Start the program and create a profile with a name, unique registration number, positive study hours, preferred time, at least one subject, and marks from 0 to 100.
2. Exit and start it again; confirm the profile loads.
3. Open the profile and try **Student Profile**, **Update Profile**, **Subject Analysis**, **Generate Timetable**, and **Weekly Timetable**.
4. Confirm lower-mark subjects receive more allocated time and the subject status reflects its mark.
5. If Gemini is configured, select **Gemini Study Chatbot**, ask a study question, then use **Recent Chats** to check saved history.
6. Try invalid numeric input and a duplicate registration number, and check that the program responds without creating an invalid profile.
7. Delete a test profile only after confirming it is the one you created for testing.

## Project files

- `MYFINALPROJECTFILE.py` – application source code.
- `students_data.json` – created at runtime for student profiles.
- `studyai_chats.json` – created at runtime for chat history.
- `README.md` – project overview and usage instructions.
- `statement.md` – problem statement, scope, target users, and high-level features.

## Limitations

This is a terminal-based application with local JSON storage. It does not provide a graphical interface, multi-device synchronization, or encrypted storage. The chatbot requires a working Gemini API key, network access, and an available model configured in the source code.
