import os
import json
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(BASE_DIR, 'students_data.json')
CHAT_FILE = os.path.join(BASE_DIR, 'studyai_chats.json')
students = {}
chat_history = {}
current_student_id = None

def load_students():
    global students
    if not os.path.exists(STUDENTS_FILE):
        students = {}
        return
    try:
        with open(STUDENTS_FILE, 'r', encoding='utf-8') as file:
            students = json.load(file)
        data_changed = False
        for registration, student in students.items():
            if not isinstance(student, dict):
                continue
            if 'student_name' not in student and 'name' in student:
                student['student_name'] = student['name']
                data_changed = True
            if 'registration_no' not in student:
                student['registration_no'] = registration
                data_changed = True
        if data_changed:
            with open(STUDENTS_FILE, 'w', encoding='utf-8') as file:
                json.dump(students, file, indent=4, ensure_ascii=False)
            print('Old student data converted successfully.')
    except Exception as error:
        print('Error loading students:', error)
        students = {}

def save_students():
    try:
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        print('Error saving students:', error)
        return False

def load_chats():
    global chat_history
    if not os.path.exists(CHAT_FILE):
        chat_history = {}
        return
    try:
        with open(CHAT_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if isinstance(data, dict):
            chat_history = data
        elif isinstance(data, list):
            chat_history = {}
            for chat in data:
                if not isinstance(chat, dict):
                    continue
                registration = chat.get('registration_no')
                if registration:
                    if registration not in chat_history:
                        chat_history[registration] = []
                    chat_history[registration].append(chat)
            save_chats()
        else:
            chat_history = {}
    except Exception as error:
        print('Error loading chat history:', error)
        chat_history = {}

def save_chats():
    global chat_history
    try:
        if not isinstance(chat_history, dict):
            chat_history = {}
        with open(CHAT_FILE, 'w', encoding='utf-8') as file:
            json.dump(chat_history, file, indent=4, ensure_ascii=False)
    except Exception as error:
        print('Error saving chat history:', error)

def create_student():
    print('\n')
    print('=' * 60)
    print('             CREATE NEW STUDENT')
    print('=' * 60)
    name = input('Enter student name: ').strip()
    registration_no = input('Enter registration number: ').strip()
    if not name:
        print('\nStudent name cannot be empty.')
        return
    if not registration_no:
        print('\nRegistration number cannot be empty.')
        return
    if registration_no in students:
        print('\nStudent already exists!')
        print("Please use 'Open Existing Student'.")
        return
    while True:
        study_hours = input('Enter available study hours per day: ').strip()
        try:
            study_hours_number = float(study_hours)
            if study_hours_number <= 0:
                print('Study hours must be greater than 0.')
                continue
            break
        except ValueError:
            print('Please enter a valid number.')
    print('\nPreferred Study Time:')
    print('1. Morning')
    print('2. Afternoon')
    print('3. Evening')
    print('4. Night')
    while True:
        choice = input('Choose option: ').strip()
        if choice == '1':
            preferred_time = 'Morning'
            break
        elif choice == '2':
            preferred_time = 'Afternoon'
            break
        elif choice == '3':
            preferred_time = 'Evening'
            break
        elif choice == '4':
            preferred_time = 'Night'
            break
        else:
            print('Please choose 1, 2, 3 or 4.')
    upcoming_exam = input('\nEnter upcoming exam/subject: ').strip()
    print('\n')
    print('Enter subject details.')
    while True:
        try:
            number_of_subjects = int(input('How many subjects? '))
            if number_of_subjects <= 0:
                print('Enter at least one subject.')
                continue
            break
        except ValueError:
            print('Please enter a valid number.')
    subjects = []
    marks = []
    for i in range(number_of_subjects):
        print(f'\nSubject {i + 1}')
        subject = input('Subject name: ').strip()
        while not subject:
            print('Subject name cannot be empty.')
            subject = input('Subject name: ').strip()
        while True:
            try:
                mark = float(input(f'Marks in {subject} (0-100): '))
                if mark < 0 or mark > 100:
                    print('Marks must be between 0 and 100.')
                    continue
                break
            except ValueError:
                print('Please enter a valid number.')
        subjects.append(subject)
        marks.append(mark)
    students[registration_no] = {'student_name': name, 'registration_no': registration_no, 'study_hours': study_hours_number, 'preferred_time': preferred_time, 'upcoming_exam': upcoming_exam, 'subjects': subjects, 'marks': marks, 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    save_students()
    if registration_no not in chat_history:
        chat_history[registration_no] = []
        save_chats()
    print('\n')
    print('=' * 60)
    print('       STUDENT PROFILE CREATED')
    print('=' * 60)
    print(f'Name: {name}')
    print(f'Registration No.: {registration_no}')
    print('Profile saved permanently.')

def show_all_students():
    print('\n')
    print('=' * 60)
    print('                 ALL STUDENTS')
    print('=' * 60)
    if not students:
        print('No student profiles found.')
        return
    count = 1
    for registration_no, student in students.items():
        print(f"\n{count}. {student.get('student_name', 'Unknown')}")
        print(f'   Registration: {registration_no}')
        print(f"   Subjects: {len(student.get('subjects', []))}")
        count += 1

def open_student():
    global current_student_id
    if not students:
        print('\nNo student profiles available.')
        return False
    print('\n')
    print('=' * 60)
    print('              OPEN STUDENT')
    print('=' * 60)
    show_all_students()
    registration_no = input('\nEnter registration number: ').strip()
    if registration_no not in students:
        print('\nStudent not found.')
        return False
    current_student_id = registration_no
    student = students[current_student_id]
    print('\n')
    print(f"Welcome back, {student['student_name']}!")
    print('Your profile has been loaded.')
    return True

def get_current_student():
    if current_student_id is None:
        return None
    return students.get(current_student_id)

def show_profile():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    print('\n')
    print('=' * 60)
    print('                 STUDENT PROFILE')
    print('=' * 60)
    print(f"\nName              : {student['student_name']}")
    print(f"Registration No.  : {student['registration_no']}")
    print(f"Study Hours       : {student['study_hours']}")
    print(f"Preferred Time    : {student['preferred_time']}")
    print(f"Upcoming Exam     : {student['upcoming_exam']}")
    print('\nSubjects and Marks:')
    for subject, mark in zip(student['subjects'], student['marks']):
        print(f'  {subject:<25} {mark:.0f}/100')

def update_profile():
    global current_student_id
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    print('\n')
    print('=' * 60)
    print('                UPDATE PROFILE')
    print('=' * 60)
    print('\nPress Enter to keep the existing value.')
    new_name = input(f"\nName [{student['student_name']}]: ").strip()
    if new_name:
        student['student_name'] = new_name
    new_hours = input(f"Study hours [{student['study_hours']}]: ").strip()
    if new_hours:
        try:
            hours = float(new_hours)
            if hours > 0:
                student['study_hours'] = hours
        except ValueError:
            print('Invalid study hours. Old value kept.')
    print('\nPreferred Time:')
    print('1. Morning')
    print('2. Afternoon')
    print('3. Evening')
    print('4. Night')
    print('Press Enter to keep current.')
    time_choice = input('Choose: ').strip()
    time_values = {'1': 'Morning', '2': 'Afternoon', '3': 'Evening', '4': 'Night'}
    if time_choice in time_values:
        student['preferred_time'] = time_values[time_choice]
    new_exam = input(f"Upcoming exam [{student['upcoming_exam']}]: ").strip()
    if new_exam:
        student['upcoming_exam'] = new_exam
    print('\nCurrent subjects:')
    for i, (subject, mark) in enumerate(zip(student['subjects'], student['marks'])):
        print(f'{i + 1}. {subject} = {mark}')
    update_marks = input('\nDo you want to update marks? (yes/no): ').lower().strip()
    if update_marks == 'yes':
        for i in range(len(student['subjects'])):
            subject = student['subjects'][i]
            old_mark = student['marks'][i]
            while True:
                new_mark = input(f'{subject} [{old_mark}]: ').strip()
                if not new_mark:
                    break
                try:
                    number = float(new_mark)
                    if 0 <= number <= 100:
                        student['marks'][i] = number
                        break
                    else:
                        print('Marks must be between 0 and 100.')
                except ValueError:
                    print('Enter a valid number.')
    student['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_students()
    print('\nProfile updated successfully.')

def delete_student():
    global current_student_id
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    print('\n')
    print('=' * 60)
    print('                DELETE STUDENT')
    print('=' * 60)
    name = student['student_name']
    registration = student['registration_no']
    confirm = input(f'\nDelete {name} ({registration})? (yes/no): ').lower().strip()
    if confirm != 'yes':
        print('Student was not deleted.')
        return
    del students[current_student_id]
    if current_student_id in chat_history:
        del chat_history[current_student_id]
    save_students()
    save_chats()
    current_student_id = None
    print('\nStudent profile deleted.')

def subject_analysis():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    subjects = student['subjects']
    marks = student['marks']
    print('\n')
    print('=' * 60)
    print('              SUBJECT ANALYSIS')
    print('=' * 60)
    if not subjects:
        print('No subjects available.')
        return
    weakest_index = marks.index(min(marks))
    weakest_subject = subjects[weakest_index]
    weakest_mark = marks[weakest_index]
    strongest_index = marks.index(max(marks))
    strongest_subject = subjects[strongest_index]
    strongest_mark = marks[strongest_index]
    for subject, mark in sorted(zip(subjects, marks), key=lambda x: x[1]):
        if mark < 50:
            status = 'Critical'
        elif mark < 75:
            status = 'Needs Improvement'
        else:
            status = 'Good'
        print(f'\n{subject}')
        print(f'Marks  : {mark:.0f}/100')
        print(f'Status : {status}')
    print('\n')
    print('-' * 60)
    print(f'Weakest Subject   : {weakest_subject} ({weakest_mark:.0f})')
    print(f'Strongest Subject : {strongest_subject} ({strongest_mark:.0f})')

def generate_timetable():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    subjects = student['subjects']
    marks = student['marks']
    study_hours = student['study_hours']
    preferred_time = student['preferred_time']
    if not subjects:
        print('\nNo subjects found.')
        return
    weights = []
    for mark in marks:
        weight = 101 - mark
        weights.append(weight)
    total_weight = sum(weights)
    allocated_hours = []
    for weight in weights:
        hours = study_hours * weight / total_weight
        allocated_hours.append(hours)
    print('\n')
    print('=' * 70)
    print('              PERSONALIZED TIMETABLE')
    print('=' * 70)
    print(f'\nPreferred Time: {preferred_time}')
    print(f'Total Study Time: {study_hours} hours/day')
    timetable_data = list(zip(subjects, marks, allocated_hours))
    timetable_data.sort(key=lambda x: x[1])
    print('\n')
    print(f"{'Subject':<25}{'Marks':<12}{'Study Time':<15}")
    print('-' * 55)
    for subject, mark, hours in timetable_data:
        print(f'{subject:<25}{mark:<12.0f}{hours:.2f} hours')
    print('\n')
    print('Lower-mark subjects receive more study time.')

def weekly_timetable():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    subjects = student['subjects']
    marks = student['marks']
    study_hours = student['study_hours']
    preferred_time = student['preferred_time']
    if not subjects:
        return
    weights = [101 - mark for mark in marks]
    total_weight = sum(weights)
    time_allocation = [study_hours * weight / total_weight for weight in weights]
    data = list(zip(subjects, marks, time_allocation))
    data.sort(key=lambda x: x[1])
    print('\n')
    print('=' * 70)
    print('                 WEEKLY TIMETABLE')
    print('=' * 70)
    print(f'Preferred Study Time: {preferred_time}')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day_index, day in enumerate(days):
        print('\n')
        print(f'---------------- {day} ----------------')
        rotation = day_index % len(data)
        rotated_data = data[rotation:] + data[:rotation]
        for subject, mark, hours in rotated_data:
            if mark < 50:
                activity = 'Concepts + Practice'
            elif mark < 75:
                activity = 'Practice + Revision'
            else:
                activity = 'Revision + Questions'
            print(f'{subject:<25}{hours:.2f} hrs   {activity}')

def show_recent_chats():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    registration = student['registration_no']
    chats = chat_history.get(registration, [])
    print('\n')
    print('=' * 60)
    print('                 RECENT CHATS')
    print('=' * 60)
    if not chats:
        print('No chats found.')
        return
    for i, chat in enumerate(chats, start=1):
        print(f"\n{i}. {chat.get('title', 'Chat')}")
        print(f"   Date: {chat.get('created_at', '')}")
        messages = chat.get('messages', [])
        print(f'   Messages: {len(messages)}')

def save_message(role, message):
    student = get_current_student()
    if student is None:
        return
    registration = student['registration_no']
    if registration not in chat_history:
        chat_history[registration] = []
    if not chat_history[registration]:
        chat_history[registration].append({'title': 'New Study Chat', 'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'messages': []})
    current_chat = chat_history[registration][-1]
    current_chat['messages'].append({'role': role, 'message': message, 'time': datetime.now().strftime('%H:%M:%S')})
    save_chats()

def run_chatbot():
    student = get_current_student()
    if student is None:
        print('\nPlease open a student profile first.')
        return
    try:
        from google import genai
    except ImportError:
        print('\nGemini library is not installed.')
        print('Install it using:')
        print('pip install google-genai')
        return
    API_KEY = os.getenv('GEMINI_API_KEY', '').strip()
    if not API_KEY:
        print('\nGemini API key not found.')
        print('Set the GEMINI_API_KEY environment variable and run the program again.')
        return
    try:
        client = genai.Client(api_key=API_KEY)
        chat = client.chats.create(model='gemini-3-flash-preview')
    except Exception as error:
        print('\nGemini connection error:')
        print(error)
        return
    print('\n')
    print('=' * 70)
    print('                 STUDYAI CHATBOT')
    print('=' * 70)
    print(f"Student: {student['student_name']}")
    print("Type 'exit' to leave the chatbot.")
    print("Type 'history' to see recent chats.")
    while True:
        question = input('\nYou: ').strip()
        if not question:
            continue
        if question.lower() == 'exit':
            print('\nLeaving chatbot...')
            break
        if question.lower() == 'history':
            show_recent_chats()
            continue
        save_message('user', question)
        subjects_text = ', '.join(student['subjects'])
        marks_text = ', '.join((f'{subject}: {mark}' for subject, mark in zip(student['subjects'], student['marks'])))
        prompt = f"\n\nYou are StudyAI, a personalized AI study assistant.\n\nHelp the student with:\n\n- Study planning\n- Time management\n- Timetable generation\n- Exam preparation\n- Revision\n- Weak subject improvement\n- Daily study planning\n\nGive simple and practical answers.\n\nSTUDENT INFORMATION:\n\nName:\n{student['student_name']}\n\nRegistration Number:\n{student['registration_no']}\n\nSubjects:\n{subjects_text}\n\nMarks:\n{marks_text}\n\nDaily Study Hours:\n{student['study_hours']}\n\nPreferred Study Time:\n{student['preferred_time']}\n\nUpcoming Exam:\n{student['upcoming_exam']}\n\nSTUDENT QUESTION:\n\n{question}\n\nAnswer according to the student's information.\n"
        try:
            response = chat.send_message(prompt)
            answer = response.text
            print(f'\nStudyAI: {answer}')
            save_message('assistant', answer)
        except Exception as error:
            print('\nGemini error:')
            print(error)

def main_menu():
    while True:
        print('\n\n')
        print('=' * 70)
        print('       STUDYAI - PERSONALIZED STUDENT SYSTEM')
        print('=' * 70)
        student = get_current_student()
        if student:
            print(f"\nCurrent Student: {student['student_name']}")
            print(f"Registration: {student['registration_no']}")
        else:
            print('\nNo student selected.')
        print('\n')
        print('1. Create New Student')
        print('2. Open Existing Student')
        print('3. Show All Students')
        print('4. Student Profile')
        print('5. Update Profile')
        print('6. Subject Analysis')
        print('7. Generate Timetable')
        print('8. Weekly Timetable')
        print('9. Gemini Study Chatbot')
        print('10. Recent Chats')
        print('11. Delete Current Student')
        print('12. Exit')
        choice = input('\nEnter your choice: ').strip()
        if choice == '1':
            create_student()
        elif choice == '2':
            open_student()
        elif choice == '3':
            show_all_students()
        elif choice == '4':
            show_profile()
        elif choice == '5':
            update_profile()
        elif choice == '6':
            subject_analysis()
        elif choice == '7':
            generate_timetable()
        elif choice == '8':
            weekly_timetable()
        elif choice == '9':
            run_chatbot()
        elif choice == '10':
            show_recent_chats()
        elif choice == '11':
            delete_student()
        elif choice == '12':
            print('\nThank you for using StudyAI!')
            break
        else:
            print('\nInvalid choice.')
            print('Please choose a number from 1 to 12.')
load_students()
load_chats()
print('\n' + '=' * 70)
print('       STUDYAI - PERSONALIZED STUDENT SYSTEM')
print('=' * 70)
if students:
    print(f'\n{len(students)} student profile(s) found.')
    print('Your previous data has been loaded.')
    first_student = list(students.keys())[0]
    current_student_id = first_student
    print(f"\nWelcome back, {students[first_student]['student_name']}!")
else:
    print('\nNo saved student profiles found.')
    print('Create your first student profile from the menu.')
main_menu()
