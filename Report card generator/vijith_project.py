import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Digidara1000',
    database='report_card'
)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_report (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_name VARCHAR(100),
        student_age INT,
        math FLOAT,
        physics FLOAT,
        english FLOAT,
        chemistry FLOAT,
        biology FLOAT,
        total_marks FLOAT,
        average_marks FLOAT,
        grade VARCHAR(2)
    )
""")
conn.commit()

def assign_grade(avg):
    if avg >= 91:
        return 'A+'
    elif avg >= 81:
        return 'A'
    elif avg >= 71:
        return 'B'
    elif avg >= 61:
        return 'C'
    elif avg >= 51:
        return 'D'
    elif avg >= 33:
        return 'E'
    else:
        return 'F'

def insert_student():
    student_name = input('Enter student name: ')
    student_age = int(input('Enter student age: '))
    math = float(input('Enter marks in Math (0-100): '))
    physics = float(input('Enter marks in Physics (0-100): '))
    english = float(input('Enter marks in English (0-100): '))
    chemistry = float(input('Enter marks in Chemistry (0-100): '))
    biology = float(input('Enter marks in Biology (0-100): '))
    total_marks = math + physics + english + chemistry + biology
    average_marks = total_marks / 5
    grade = assign_grade(average_marks)

    insert_query = """
        INSERT INTO student_report (
            student_name, student_age, math, physics, english, chemistry, biology, total_marks, average_marks, grade
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (student_name, student_age, math, physics, english, chemistry, biology, total_marks, average_marks, grade)
    cursor.execute(insert_query, values)
    conn.commit()

    print("Student report saved to MySQL database.")

def view_students():
    cursor.execute("SELECT * FROM student_report")
    report = cursor.fetchall()

    if not report:
        print("No student records found.")
        return

    print("\n============= ALL STUDENT REPORT CARDS =============")
    for row in report:
        print("---------------------------------------------------")
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Age: {row[2]}")
        print(f"Math: {row[3]}")
        print(f"Physics: {row[4]}")
        print(f"English: {row[5]}")
        print(f"Chemistry: {row[6]}")
        print(f"Biology: {row[7]}")
        print(f"Total Marks: {row[8]}")
        print(f"Average Marks: {row[9]:.2f}")
        print(f"Grade: {row[10]}")
    print("===================================================")

def update_student():
    id = int(input("Enter Student ID to update: "))
    cursor.execute("SELECT * FROM student_report WHERE id = %s", (id,))
    student = cursor.fetchone()

    if not student:
        print("Student ID not found.")
        return

    print("\nLeave blank to keep existing values.")

    def get_new_value(prompt, current):
        val = input(f"{prompt} (current: {current}): ")
        return float(val) if val.strip() else current

    name = input(f"Enter new name (current: {student[1]}): ") or student[1]
    age = input(f"Enter new age (current: {student[2]}): ")
    age = int(age) if age.strip() else student[2]
    math = get_new_value("Math", student[3])
    physics = get_new_value("Physics", student[4])
    english = get_new_value("English", student[5])
    chemistry = get_new_value("Chemistry", student[6])
    biology = get_new_value("Biology", student[7])

    total = math + physics + english + chemistry + biology
    average = total / 5
    grade = assign_grade(average)

    update_query = """
        UPDATE student_report
        SET student_name=%s, student_age=%s, math=%s, physics=%s,
            english=%s, chemistry=%s, biology=%s,
            total_marks=%s, average_marks=%s, grade=%s
        WHERE id=%s
    """
    values = (name, age, math, physics, english, chemistry, biology, total, average, grade, id)
    cursor.execute(update_query, values)
    conn.commit()
    print("Student record updated successfully.")

def delete_student():
    id = int(input("Enter Student ID to delete: "))
    cursor.execute("SELECT * FROM student_report WHERE id = %s", (id,))
    if not cursor.fetchone():
        print("Student ID not found.")
        return

    cursor.execute("DELETE FROM student_report WHERE id = %s", (id,))
    conn.commit()
    print("Student record deleted.")

while True:
    print("\n========= STUDENT REPORT CARD MENU =========")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        insert_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        update_student()
    elif choice == '4':
        delete_student()
    elif choice == '5':
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number from 1 to 5.")

cursor.close()
conn.close()

