import sqlite3
from pyfingerprint.pyfingerprint import PyFingerprint



def initialize_database():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 fingerprint_id INTEGER UNIQUE NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id INTEGER NOT NULL,
                 date DATE DEFAULT (date('now')),
                 time TIME DEFAULT (time('now', 'localtime')),
                 FOREIGN KEY (student_id) REFERENCES students(student_id))''')

    conn.commit()
    conn.close()

def enroll_student():
    try:
        f = PyFingerprint('COM1', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

        name = input('Enter student name: ')

        print('Waiting for finger...')

        while not f.readImage():
            pass

        f.convertImage(0x01)

        print('Remove your finger...')
        input('Press Enter when ready...')

        print('Place the same finger again...')

        while not f.readImage():
            pass

        f.convertImage(0x02)

        if f.compareCharacteristics() == 0:
            raise Exception('Fingerprints do not match!')

        f.createTemplate()
        fingerprint_id = f.storeTemplate()

        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()

        c.execute("INSERT INTO students (name, fingerprint_id) VALUES (?, ?)",
                  (name, fingerprint_id))

        conn.commit()
        conn.close()

        return True

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return False


def mark_attendance():
    try:
        f = PyFingerprint('COM1', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

        print('Waiting for finger...')

        while not f.readImage():
            pass

        f.convertImage(0x01)

        result = f.searchTemplate()

        position = result[0]

        if position >= 0:
            print('Fingerprint recognized! Student ID:', position)
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()

            c.execute("INSERT INTO attendance (student_id) VALUES (?)",
                      (position,))

            conn.commit()
            conn.close()
        else:
            print('Fingerprint not recognized!')

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))

def get_average_attendance(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?", (student_id,))
    total_attendance_count = c.fetchone()[0]

    c.execute("SELECT COUNT(DISTINCT date) FROM attendance WHERE student_id = ?", (student_id,))
    unique_days_count = c.fetchone()[0]

    conn.close()

    if total_attendance_count == 0 or unique_days_count == 0:
        return 0

    average_attendance = (total_attendance_count / unique_days_count) * 100
    return average_attendance

def get_attendance_count(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?", (student_id,))
    result = c.fetchone()

    if result is None:
        print('Invalid student ID.')
        attendance_count = 0
    else:
        attendance_count = result[0]

    conn.close()

    return attendance_count


def main():
    initialize_database()

    print('==============================================')
    print('          Fingerprint Attendance System')
    print('==============================================')
    print('1. Enroll Student')
    print('2. Mark Attendance')
    print('3. Check Attendance Count')
    print('4. Check Average Attendance')
    print('==============================================')

    choice = int(input('Enter your choice (1, 2, 3, or 4): '))

    if choice == 1:
        if enroll_student():
            print('Student enrolled successfully!')
        else:
            print('Student enrollment failed.')
    elif choice == 2:
        mark_attendance()
    elif choice == 3:
        student_id = int(input('Enter student ID: '))
        attendance_count = get_attendance_count(student_id)
        print('==============================================')
        print('Attendance Count:', attendance_count)
    elif choice == 4:
        student_id = int(input('Enter student ID: '))
        average_attendance = get_average_attendance(student_id)
        print('==============================================')
        print('Average Attendance:', average_attendance, '%')
    else:
        print('Invalid choice.')
    print('==============================================')


main()
