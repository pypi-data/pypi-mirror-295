import random
import calendar
from datetime import datetime, timedelta, time

def get_working_past_date(start, end=0):
    return get_past_date(start, end, True)


def get_past_date(start, end=0, working_days=False):
    """
    Returns a past date in the format 'YYYY-MM-DD HH:MM:SS'.
    The date is calculated as a random date between (now - start days) and (now - end days).
    If working_days is True, the date will be a weekday and the time will be between 8:00 and 19:00.

    Parameters:
    start (int): The start day for the range.
    end (int): The end day for the range. Default is 0.
    working_days (bool): If True, the date will be a weekday and the time will be between 8:00 and 19:00.

    Returns:
    str: A string representing the past date.
    """
    if start < end:
        raise ValueError("Start day must be greater than or equal to end day.")

    now = datetime.now()
    start_date = now - timedelta(days=start)
    end_date = now - timedelta(days=end)

    random_date = start_date + (end_date - start_date) * random.random()

    if working_days:
        while random_date.weekday() > 4:  # 0-4 corresponds to Monday-Friday
            random_date = random_date - timedelta(days=1)

        # Generate a random time between 8:00 and 19:00
        random_time = time(hour=random.randint(8, 18), minute=random.randint(0, 59), second=random.randint(0, 59))
        random_date = random_date.replace(hour=random_time.hour, minute=random_time.minute, second=random_time.second)

    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def get_case_dates(status: str):
    created_at   = None
    initiated_at = None
    completed_at = None
    updated_at   = None
    
    if status == 'completed':
        created_at   = get_working_past_date(1000, 1)

        # calculate initiated, some seconds after created
        date_object = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        # Generate a random number of seconds between 10 and 1000
        random_seconds = random.randint(10, 1000)
        time_delta = timedelta(seconds=random_seconds)
        # Add the timedelta to the original datetime object
        new_date_object = date_object + time_delta
        initiated_at =  new_date_object.strftime('%Y-%m-%d %H:%M:%S')
        
        # calculate the complete_at as any day from initiate + 1 day until now 
        yesterday = datetime.now() - timedelta(days=1)
        # Calculate the difference in days
        days_difference = (yesterday - new_date_object).days

        completed_at = get_working_past_date(days_difference, 0)
        updated_at   = completed_at
    
    if status == 'in_progress':
        created_at   = get_working_past_date(1000, 1)

        # calculate initiated, some seconds after created
        date_object = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        # Generate a random number of seconds between 10 and 1000
        random_seconds = random.randint(10, 1000)
        time_delta = timedelta(seconds=random_seconds)
        # Add the timedelta to the original datetime object
        new_date_object = date_object + time_delta
        initiated_at =  new_date_object.strftime('%Y-%m-%d %H:%M:%S')
        
        completed_at = None
        updated_at   = initiated_at
    
    #print (f"  {created_at}\n  {initiated_at}\n  {completed_at}\n  {updated_at}\n")    
    return created_at, initiated_at, completed_at, updated_at


def add_secs(created_at: str, min: int, max: int):
        # calculate initiated, some seconds after created
        date_object = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
        # Generate a random number of seconds between 10 and 1000
        random_seconds = random.randint(min, max)
        time_delta = timedelta(seconds=random_seconds)
        # Add the timedelta to the original datetime object
        new_date_object = date_object + time_delta
        initiated_at =  new_date_object.strftime('%Y-%m-%d %H:%M:%S')
        return initiated_at
    
                
def get_HMS(execution_time: float):
    # Calculate minutes, seconds and hundredths of a second
    minutes, sec = divmod(execution_time, 60)
    seconds, hundredths = divmod(sec, 1)
    hundredths *= 100

    return f"{int(minutes):02}:{int(seconds):02}.{int(hundredths):02}"
    