import mysql.connector as myConn

db = myConn.connect(host="localhost", user="root", password="Lak1han@")
cursor = db.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS temp123")
cursor.execute("USE temp123")

cursor.execute("""
CREATE TABLE IF NOT EXISTS UserData (
    StudentName VARCHAR(30),
    CollegeName VARCHAR(50),
    Round1Marks FLOAT CHECK (Round1Marks BETWEEN 0 AND 10),
    Round2Marks FLOAT CHECK (Round2Marks BETWEEN 0 AND 10),
    Round3Marks FLOAT CHECK (Round3Marks BETWEEN 0 AND 10),
    TechnicalRoundMarks FLOAT CHECK (TechnicalRoundMarks BETWEEN 0 AND 20),
    TotalMarks FLOAT CHECK (TotalMarks BETWEEN 0 AND 50),
    Result VARCHAR(10),
    `Rank` INT
)
""")

def calculate_rank():
    cursor.execute("SELECT StudentName, TotalMarks FROM UserData ORDER BY TotalMarks DESC")
    records = cursor.fetchall()
    rank = 1
    previous_marks = None
    rank_dict = {}
    
    for record in records:
        if previous_marks is not None and record[1] < previous_marks:
            rank += 1
        rank_dict[record[0]] = rank
        previous_marks = record[1]
    
    for name, rank in rank_dict.items():
        cursor.execute("UPDATE UserData SET `Rank` = %s WHERE StudentName = %s", (rank, name))
    db.commit()

def add_user_data():
    while True:
        StudentName = input("Enter the student's name (less than 30 characters): ").strip()
        if len(StudentName) > 30:
            print("Name cannot be more than 30 characters")
            continue

        CollegeName = input("Enter the college name (less than 50 characters): ").strip()
        if len(CollegeName) > 50:
            print("College name cannot be more than 50 characters")
            continue

        Round1Marks = float(input("Enter Round 1 marks (between 0 to 10): ").strip())
        if Round1Marks < 0 or Round1Marks > 10:
            print("Round 1 marks must be between 0 and 10")
            continue

        Round2Marks = float(input("Enter Round 2 marks (between 0 to 10): ").strip())
        if Round2Marks < 0 or Round2Marks > 10:
            print("Round 2 marks must be between 0 and 10")
            continue

        Round3Marks = float(input("Enter Round 3 marks (between 0 to 10): ").strip())
        if Round3Marks < 0 or Round3Marks > 10:
            print("Round 3 marks must be between 0 and 10")
            continue

        TechnicalRoundMarks = float(input("Enter Technical Round marks (between 0 to 20): ").strip())
        if TechnicalRoundMarks < 0 or TechnicalRoundMarks > 20:
            print("Technical Round marks must be between 0 and 20")
            continue

        TotalMarks = Round1Marks + Round2Marks + Round3Marks + TechnicalRoundMarks
        Result = "Selected" if TotalMarks >= 35 else "Rejected"

        cursor.execute(
            "INSERT INTO UserData (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (StudentName, CollegeName, Round1Marks, Round2Marks, Round3Marks, TechnicalRoundMarks, TotalMarks, Result)
        )

        db.commit()

        print(f"Record added for {StudentName} successfully")
        break

while True:
    add_user_data()
    more = input("Do you want to add another record? (yes/no): ").strip().lower()
    if more != "yes":
        break

calculate_rank()

cursor.execute("SELECT * FROM UserData ORDER BY `Rank`")
records = cursor.fetchall()

print("All records:")
for record in records:
    print(record)

cursor.close()
db.close()
