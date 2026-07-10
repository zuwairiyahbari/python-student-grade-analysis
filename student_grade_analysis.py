# Task 1 Working with data
import pandas as pd

# Read the CSV file
df = pd.read_csv('Ten_Students_Scores.csv')

# Calculate the Grade using weighted average
# Midterm: 20%, Final: 20%, Project1: 30%, Project2: 30%
df['Grade'] = (df['Midterm Exam- 100 Pts.'] * 0.2 +
               df['Final Exam- 100 Pts.'] * 0.2 +
               df['Project 1- 100 Pts.'] * 0.3 +
               df['Project 2 - 100 Pts.'] * 0.3)

# Assign Letter Grade based on the calculated Grade
def assign_letter_grade(grade):
    if grade >= 90:
        return 'A'
    elif grade >= 80:
        return 'B'
    elif grade >= 70:
        return 'C'
    else:
        return 'D'

df['Letter grade'] = df['Grade'].apply(assign_letter_grade)

# Save the new CSV file
df.to_csv('Ten_Students_Grades.csv', index=False)

# Display the results
print("Task #1")
print(df[['id', 'first_name', 'last_name', 'Grade', 'Letter grade']])

# Task 2 SQL and SQLite

import sqlite3
import pandas as pd


# Create database and table
def create_database():
    conn = sqlite3.connect('Student.db')
    cursor = conn.cursor()

    # Create table with specified schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Ten_Students (
            ID INTEGER PRIMARY KEY,
            First_name TEXT,
            Last_name TEXT,
            Midterm REAL,
            Final REAL,
            Project1 REAL,
            Project2 REAL,
            Grade REAL,
            Letter_Grade TEXT
        )
    ''')
    conn.commit()
    conn.close()



# Import records from CSV
def import_records():
    conn = sqlite3.connect('Student.db')

    # Read the CSV file created in Task #1
    df = pd.read_csv('Ten_Students_Grades.csv')

    # Rename columns to match database schema
    df = df.rename(columns={
        'id': 'ID',
        'first_name': 'First_name',
        'last_name': 'Last_name',
        'Midterm Exam- 100 Pts.': 'Midterm',
        'Final Exam- 100 Pts.': 'Final',
        'Project 1- 100 Pts.': 'Project1',
        'Project 2 - 100 Pts.': 'Project2',
        'Grade': 'Grade',
        'Letter grade': 'Letter_Grade'
    })

    # Insert records into database
    df.to_sql('Ten_Students', conn, if_exists='replace', index=False)
    conn.close()



# Display students sorted alphabetically by name
def display_students_sorted():
    conn = sqlite3.connect('Student.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ID, First_name, Last_name, Grade, Letter_Grade 
        FROM Ten_Students 
        ORDER BY Last_name ASC, First_name ASC
    ''')

    print("\nTask #2")
    print("\nStudents sorted alphabetically:")
    print("ID\tFirst Name\tLast Name\tGrade\tLetter Grade")

    for row in cursor.fetchall():
        print(f"{row[0]}\t{row[1]}\t\t{row[2]}\t\t{row[3]:.2f}\t{row[4]}")

    conn.close()


# Generate frequency distribution of Letter Grades
def grade_frequency():
    conn = sqlite3.connect('Student.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Letter_Grade, COUNT(*) as Count 
        FROM Ten_Students 
        GROUP BY Letter_Grade 
        ORDER BY Letter_Grade
    ''')

    print("\nFrequency distribution of Letter Grades:")
    print("Letter Grade\tCount")

    for row in cursor.fetchall():
        print(f"{row[0]}\t\t{row[1]}")

    conn.close()


# Remove records where Letter_Grade equals 'D'
def remove_d_grades():
    conn = sqlite3.connect('Student.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Ten_Students WHERE Letter_Grade = 'D'")
    conn.commit()

    print(f"\nRemoved {cursor.rowcount} record with grade 'D'")

    conn.close()


# Main execution
def main():



    create_database()
    import_records()
    display_students_sorted()
    grade_frequency()
    remove_d_grades()

    # Display final state after removal
    print("\nFinal state after removing 'D' grades:")
    display_students_sorted()


if __name__ == "__main__":
    main()
