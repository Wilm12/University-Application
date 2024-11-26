# This is a university application app
# It minimises the time and effort of applying by filtering only the courses you qualify for
# The app gives the student options to either apply or check application status
# If the student selects to apply,the code will ask for input of student details
# The details also contain a student average which is the average the student got in matric
# A databse is created in a separate script which contains universities,faculties, courses and an  required average for each course
# Student average is used to check if the student has an average equal to greater than the required average in the database of university courses
# If the student qualifes for any course, the console will first print a list of universities containing those course.
# After selecting the university,the student is given a list of faculties in those universities,then courses
# A student then selects a course of their choice and a message is returned to them to notify them that they applied
# If a student does not qualify for any course due to their average,a message will be printed to notify them
# If the maximum capacity for the particular course has been reached and the student cannot continue with application,a message is printed
# If a student has applied and wants to check the application status,they selected option 2 and follow instructions to check
  
import sqlite3
# Create a table to save student information
def create_student_table():
    try:
        conn = sqlite3.connect("student_information.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS student_information(
                     i_d INTEGER PRIMARY KEY, name TEXT, surname TEXT, grade_average INTEGER)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating student table: {e}")
    finally: conn.close()
# Create a function to get information from the student
# Initiate a class named Student to get an indidual student informatioin with defined properties
# Get the input from the student and save that information within the table student_information
# Return the student ID to retrieve information about a particular student
def get_student_info():

    class Student:
        def __init__(self, i_d, name, surname, grade_average):
            self.i_d = i_d
            self.name = name
            self.surname = surname
            self.grade_average = grade_average

        def save_to_db(self):
            try:
                conn = sqlite3.connect("student_information.db")
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO student_information(
                       i_d, name, surname, grade_average)
                        VALUES(?, ?, ?, ?)''', (self.i_d, self.name, self.surname, self.grade_average))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error saving information to database: {e}")
            finally: conn.close()

    try:
        i_d = input("Enter your id: ")
        name = input("Enter your name: ")
        surname = input("Enter your surname: ")
        grade_average = int(input("Enter your grade average: "))
        student = Student(i_d, name, surname, grade_average)
        student.save_to_db()
        return i_d
    except ValueError as e:
        print(f"Invalid input: {e}")
# Create a function to retieve students who qualified
# Execute a query to get qualified students based on their grade average being equal to or greater than required average
# Return qualified students for later use
def get_qualified_students_by_id(student_id):
    conn = sqlite3.connect("student_information.db")
    cursor = conn.cursor()
    cursor.execute("ATTACH DATABASE 'courses.db' AS courses")
    cursor.execute('''SELECT s.i_d, s.name, s.surname, c.university, c.faculty, c.course
                      FROM student_information s
                      JOIN courses c ON s.grade_average >= c.required_avg
                      WHERE s.i_d = ?''', (student_id,))
    qualified_students = cursor.fetchall()
    conn.close()
    return qualified_students
# Create funtion to select a university
# Qualified_students is passed to the funtion to retrieve universities that the student qualifies for
# The selected university is returned

def select_university(qualified_students):
    try:
        universities = set(student[3] for student in qualified_students)
        print("Select a university:")
        for i, university in enumerate(universities):
            print(f"{i + 1}. {university}")
        selected_index = int(input("Enter the number of your choice: ")) - 1
        selected_university = list(universities)[selected_index]
        return selected_university
    except ValueError as e:
        print(f"Invalid input: {e}")
# Create function to select a fuculty
# qualified_students and selected_university are passed to the function to retrieve faculties within a chosen unversity
# These are only faculties containg courses that the student qualifies for based on the grades average
def select_faculty(qualified_students, selected_university):
    try:
        faculties = set(student[4] for student in qualified_students if student[3] == selected_university)
        print("Select a faculty:")
        for i, faculty in enumerate(faculties):
            print(f"{i + 1}. {faculty}")
        selected_index = int(input("Enter the number of your choice: ")) - 1
        return list(faculties)[selected_index]
    except ValueError as e:
        print(f"Invalid input: {e}")
# Create function to select a course
def select_course(qualified_students, selected_university, selected_faculty):
    try:
        courses = set(student[5] for student in qualified_students if student[3] == selected_university and student[4] == selected_faculty)
        print("Select a course:")
        for i, course in enumerate(courses):
            print(f"{i + 1}. {course}")
        selected_index = int(input("Enter the number of your choice: ")) - 1
        return list(courses)[selected_index]
    except ValueError as e:
        print(f"Invalid value: {e}")
# Create a function to check space availability
def check_course_capacity(selected_university, selected_faculty, selected_course):
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT current_students, max_students FROM courses
                     WHERE university = ? AND faculty = ? AND course = ?''',
                    (selected_university, selected_faculty, selected_course))
    result = cursor.fetchone()
    conn.close()
    if result:
        current_students, max_students = result
        return current_students < max_students
    return False
# Create function to add a student to the current applications in a course

def update_course_enrolment(selected_university, selected_faculty, selected_course):
    try:
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
        cursor.execute('''UPDATE courses SET current_students = current_students + 1
                      WHERE university = ? AND faculty = ? AND course = ?''',
                   (selected_university, selected_faculty, selected_course))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating course enrolment: {e}")
    finally:
        conn.close()
# Create function to check the application status
def check_application_status():
    i_d = input("Enter your student ID to check application status: ")
    with sqlite3.connect("student_information.db") as conn:
        cursor = conn.cursor()
        cursor.execute("ATTACH DATABASE 'courses.db' AS courses")
        cursor.execute('''SELECT s.name, s.surname, c.university, c.faculty, c.course
                          FROM student_information s
                          JOIN courses c ON s.grade_average >= c.required_avg
                          WHERE s.i_d = ?''', (i_d,))
        result = cursor.fetchone()   
        if result:
            name, surname, university, faculty, course = result
            print(f"Student: {name} {surname}")
            print(f"University: {university}")
            print(f"Faculty: {faculty}")
            print(f"Course: {course}")
            print("Your application is successful!")
        else:
            print("No application found or you do not meet the requirements.")

def main_application():
    try:
        create_student_table()

        options = ["Apply", "Check application status"]
        while True:
            print("What do you want to do?")
            for i, option in enumerate(options):
                print(f"{i + 1}. {option}")
            try:
                selected_index = int(input(f"Enter option number [1 - {len(options)}]: ")) - 1

                if selected_index == 0:
                    print("You selected apply")
                    student_id = get_student_info()
                    qualified_students = get_qualified_students_by_id(student_id)
                    if not qualified_students:
                        print("No courses available for your grade average.")
                        break
                    selected_university = select_university(qualified_students)
                    selected_faculty = select_faculty(qualified_students, selected_university)
                    selected_course = select_course(qualified_students, selected_university, selected_faculty)
                    if not check_course_capacity(selected_university, selected_faculty, selected_course):
                        print(f"Sorry, the course {selected_course} is full and cannot accept more students.")
                        break
                    print(f"You have applied for: {selected_course} in the faculty of {selected_faculty} at the {selected_university}")
                    update_course_enrolment(selected_university, selected_faculty, selected_course)
                    break
                elif selected_index == 1:
                    print("You selected to check application status")
                    check_application_status()
                else:
                    print("You have entered an invalid option")
            except ValueError as e:
                print(f"Invalid input: {e}")

    except Exception as e:
        print(f"An error occured: {e}")

if __name__ == "__main__":
    main_application()
