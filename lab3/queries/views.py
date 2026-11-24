from django.http import JsonResponse
from .db_operations import (
    close_and_check_connection,
    run_atomic_rollback_demo,
    run_raw_sql_demo,
)


def db_lab_report(request):
    rows = run_raw_sql_demo()
    rollback_msg, student_after = run_atomic_rollback_demo(100.0)
    before_usable, after_conn = close_and_check_connection()

    return JsonResponse(
        {
            "raw_sql_rows": rows,
            "atomic_rollback": {
                "message": rollback_msg,
                "student_after_rollback": student_after,
            },
            "connection_management": {
                "usable_before_close": before_usable,
                "connection_object_after_close": str(after_conn),
            },
        }
    )
