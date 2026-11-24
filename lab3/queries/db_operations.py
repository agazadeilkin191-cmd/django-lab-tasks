from django.db import connection, transaction


def run_raw_sql_demo():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                group_code TEXT NOT NULL,
                balance REAL NOT NULL
            )
            """
        )
        cursor.execute("DELETE FROM students")
        cursor.execute(
            "INSERT INTO students (full_name, group_code, balance) VALUES (%s, %s, %s)",
            ["Ilkin Agazade", "845A3", 250.0],
        )
        cursor.execute(
            "INSERT INTO students (full_name, group_code, balance) VALUES (%s, %s, %s)",
            ["Shaig Mammadov", "845A3", 180.0],
        )
        cursor.execute("SELECT id, full_name, group_code, balance FROM students")
        rows = cursor.fetchall()
    return rows


def run_atomic_rollback_demo(payment_amount=100.0):
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET balance = balance - %s WHERE full_name = %s",
                    [payment_amount, "Ilkin Agazade"],
                )
                raise RuntimeError("Simulated error during transfer")
    except RuntimeError as exc:
        rollback_message = f"Transaction rolled back due to error: {exc}"

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT full_name, group_code, balance FROM students WHERE full_name = %s",
            ["Ilkin Agazade"],
        )
        student_after_rollback = cursor.fetchone()

    return rollback_message, student_after_rollback


def close_and_check_connection():
    before_close_usable = connection.is_usable()
    connection.close()
    after_close_conn_obj = connection.connection
    return before_close_usable, after_close_conn_obj


if __name__ == "__main__":
    import os
    import sys
    import django

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_lab_project.settings")
    django.setup()

    print("--- 1. RAW SQL ---")
    for row in run_raw_sql_demo():
        print(row)

    print("\n--- 2. TRANSACTION.ATOMIC() ROLLBACK ---")
    msg, after = run_atomic_rollback_demo(100.0)
    print(msg)
    print("Student state after rollback:", after)

    print("\n--- 3. CONNECTION CLOSE & STATUS ---")
    before_usable, after_conn = close_and_check_connection()
    print("Usable before close:", before_usable)
    print("connection.connection after close():", after_conn)
