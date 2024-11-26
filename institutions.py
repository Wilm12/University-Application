import sqlite3

# Create courses table
def create_courses_table():
    try:
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                        (university TEXT, faculty TEXT, course TEXT,
                        required_avg INTEGER, max_students INTEGER, current_students INTEGER DEFAULT 0)''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating courses table: {e}")
    finally:
        conn.close()

class Course:
    def __init__(self, name, required_avg, max_students):
        self.name = name
        self.required_avg = required_avg
        self.max_students = max_students
        self.current_students = 0

class Faculty:
    def __init__(self, name):
        self.name = name
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

class University:
    def __init__(self, name):
        self.name = name
        self.faculties = []

    def add_faculty(self, faculty):
        self.faculties.append(faculty)

    def save_info(self):
        try:
            conn = sqlite3.connect("courses.db")
            cursor = conn.cursor()

            for faculty in self.faculties:
                for course in faculty.courses:
                    cursor.execute('''INSERT INTO courses (university, faculty, course, required_avg, max_students, current_students)
                                    VALUES(?, ?, ?, ?, ?, ?)''',
                                (self.name, faculty.name, course.name, course.required_avg, course.max_students, course.current_students))

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving information to database: {e}")
        finally:
            conn.close()

def create_course_db():
    try:
        university_name = input("Enter university name: ")
        university = University(university_name)

        while True:
            faculty_name = input("Enter faculty name (or 'done' to finish): ")
            if faculty_name.lower() == 'done':
                break
            faculty = Faculty(faculty_name)

            while True:
                course_name = input("Enter course name (or 'done' to finish): ")
                if course_name.lower() == 'done':
                    break
                required_avg = float(input("Enter the average required: "))
                max_students = int(input("Enter the maximum number of students allowed: "))
                course = Course(course_name, required_avg, max_students)
                faculty.add_course(course)
            university.add_faculty(faculty)

        university.save_info()
        print(f"Data for {university.name} has been saved successfully.")
    except ValueError as e:
        print(f"Invalid input: {e}")

def main():
    create_courses_table()
    create_course_db()

if __name__ == "__main__":
    main()
