import pytz
from datetime import datetime, timedelta, timezone

def get_current_time_in_melbourne() -> datetime:
    """Get the current time in Melbourne timezone."""
    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)
    # Define the Melbourne timezone
    melbourne_tz = pytz.timezone('Australia/Melbourne')
    # Convert the UTC time to Melbourne time
    melbourne_now = utc_now.astimezone(melbourne_tz)
    return melbourne_now

def get_tz() -> '_UTCclass':
    """Get the Melbourne timezone."""
    return pytz.timezone('Australia/Melbourne')

def round_up_to_next_30_minutes(dt: datetime) -> datetime:
    """Round up the provided datetime to the next 30-minute interval."""
    # Calculate the number of minutes to add to round up to the next 30-minute mark
    add_minutes = 30 - (dt.minute % 30)
    if add_minutes == 30:
        add_minutes = 0
    rounded_time = dt + timedelta(minutes=add_minutes)
    # Set seconds and microseconds to zero
    rounded_time = rounded_time.replace(second=0, microsecond=0)
    return rounded_time

def get_next_30_minute_interval_as_string() -> str:
    """Get the next 30-minute interval from the current time as a string."""
    current_time = get_current_time_in_melbourne()
    rounded_time = round_up_to_next_30_minutes(current_time)
    # Return the time as a string in the format '8:00am' or '8:30am'
    return rounded_time.strftime('%I:%M%p').lower()

def get_current_date() -> str:
    """Get the current date as a string in the format 'DD-MM-YYYY'."""
    current_time = get_current_time_in_melbourne()
    # Return the date as a string in the format 'DD-MM-YYYY'
    return current_time.strftime('%d-%m-%Y')

# Example usage
print("Next 30-minute interval:", get_next_30_minute_interval_as_string())
print("Current date:", get_current_date())
