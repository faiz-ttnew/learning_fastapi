import logging
import time

logger = logging.getLogger("uvicorn.error")

def notify_employee_created(emp_id: int):
    logger.info(
        "Notification started for employee id=%s",
        emp_id
    )

    # Local learning only: simulate a slow notification.
    time.sleep(3)

    logger.info(
        "Notification completed for employee id=%s",
        emp_id
    )