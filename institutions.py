# This code is meant to create a database of universities and the courses they offer

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
    """ A class to represent a faculty course in a university.

        Attributes:
            name (str): The name of the course. 
            required_avg (int): The required average for the course. 
            max_students (int): The maximum number of students allowed. 
            current_students (int): The current number of students enrolled.
    """
    def __init__(self, name, required_avg, max_students):
        """ Initialize the Course with name, required average, and maximum students.
          Parameters:
           
              name (str): The name of the course.
              required_avg (int): The required average for the course.
              max_students (int): The maximum number of students allowed.
        """
        self.name = name
        self.required_avg = required_avg
        self.max_students = max_students
        self.current_students = 0 # Current students set to 0 to establish a starting point

class Faculty:
    """ A class to represent a faculty.

    Attributes:
        name (str): The name of the faculty. 
        courses (list): A list of courses offered by the faculty.
    """
    def __init__(self, name):
        self.name = name
        self.courses = [] #Empty list to add courses
# Method to add courses to the list in a faculty
    def add_course(self, course):
        """ Add a course to the faculty.

          Parameters: 
              course (Course): The course to be added. 
        """  
        self.courses.append(course)

class University:
    """ A class to represent a university. 

    Attributes:
        name (str): The name of the university.
        faculties (list): A list of faculties in the university.
    """
    def __init__(self, name):
        self.name = name
        self.faculties = []

    def add_faculty(self, faculty):
        """ Add a faculty to the university.

          Parameters:
              faculty (Faculty): The faculty to be added.
        """
        self.faculties.append(faculty)

    def save_info(self):
        """
        Save the university information to the database.
        """
        try:
            conn = sqlite3.connect("courses.db")
            cursor = conn.cursor()

            for faculty in self.faculties: # Loop iterates over each Faculty object
                for course in faculty.courses: #Loop iterates over each Course object in the faculty.courses list
                    cursor.execute('''INSERT INTO courses (university, faculty, course, required_avg, max_students, current_students)
                                    VALUES(?, ?, ?, ?, ?, ?)''',
                                (self.name, faculty.name, course.name, course.required_avg, course.max_students, course.current_students))

            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving information to database: {e}")
        finally:
            conn.close()

def create_course_db():
    """ 
    Create a database entry for a university and its faculties and courses.
    """
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
    """ 
    Main function to create the courses table and insert into the database.
    """
    create_courses_table()
    create_course_db()

if __name__ == "__main__":
    main()
