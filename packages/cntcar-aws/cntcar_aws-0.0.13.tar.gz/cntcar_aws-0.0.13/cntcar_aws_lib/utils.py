from croniter import croniter
from datetime import datetime as dt

def handle_error(e, detail=""):
    """Generic error handler function.
    
    Parameters:
        e : Exception
            The exception object.
        detail : str
            Additional detail or message to include in the error log.
    
    Returns:
        None
    """
    print(f'Error: {str(e)}')
    if detail: print(f'detail: {detail}')


def get_next_cron_date(cron_expression:str, base_time:dt = dt.now()):
    """
    This function calculates the next date based on a cron expression.

    Parameters:
        cron_expression : str
            A string representing the cron expression.
        base_time : datetime
            A datetime object representing the base time to calculate the next date, if not provided, the current time will be used.

    Returns:
        str
    """
    try:
        cron = croniter(cron_expression, base_time)
        next_date = cron.get_next(dt)
        next_date = next_date.strftime('%Y-%m-%d %H:%M:%S.%f')
        print(f'Based on the cron expression "{cron_expression}", the next invocation will be at {next_date}')
        return next_date
    except Exception as e:
        detail = f'Error getting next cron date: {str(e)}'
        handle_error(e,detail)