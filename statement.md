# StudyAI Project Statement

## Problem statement

Students often need to organize study time across several subjects while accounting for their current performance, daily availability, preferred study period, and upcoming exams. Without a simple way to keep this information together, it can be difficult to decide which subjects need more attention and to maintain a consistent revision plan.

StudyAI addresses this need with a command-line application that keeps a student profile, summarizes marks, and produces study-time allocations weighted toward lower-mark subjects. It also offers an optional AI chat assistant for study-related questions.

## Project scope

The project covers local student-profile management, subject and mark tracking, basic performance analysis, daily and weekly timetable generation, and optional Gemini-based study chat with locally saved chat history. Profile and chat data are stored as JSON files in the application folder.

The project is intended as an educational prototype. It does not include a graphical interface, cloud storage, multi-user authentication, timetable calendar integration, automatic exam-date planning, or encrypted storage. The chatbot depends on an external Gemini service and requires internet access and a valid API key.

## Target users

- Students who want a basic way to organize subject marks and study hours.
- Learners preparing for upcoming exams who want a simple, mark-informed study plan.
- Students practicing Python application development and local JSON persistence.

## High-level features

1. Create, open, view, edit, and delete student profiles.
2. Record available daily study hours, preferred study time, upcoming exam, subjects, and marks.
3. Categorize subject performance and identify strongest and weakest subjects.
4. Allocate more study time to subjects with lower marks.
5. Display daily subject allocations and a rotating seven-day study timetable.
6. Optionally ask a Gemini-powered assistant for study guidance using the student's profile context.
7. Save profile data and chat history locally between program runs.
