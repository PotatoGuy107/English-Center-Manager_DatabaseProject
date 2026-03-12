from infrastructure.config.database import get_connection

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
print([row[0] for row in cursor.fetchall()])

# Check Exam table structure
try:
    cursor.execute("SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Exam'")
    print("\nExam table structure:")
    for row in cursor.fetchall():
        print(f"  {row[0]} - {row[1]} - nullable: {row[2]}")
except Exception as e:
    print(f"Exam table not found: {e}")

conn.close()
