
from datetime import datetime, timedelta

# Get the current date and time
now = datetime.now()
print(now)

# Get a date 7 days from now
future_date = now + timedelta(days=7)
print(future_date)

# Format the date as a string
date_string = now.strftime('%Y-%m-%d %H:%M:%S')
print(date_string)

# Parse a date from a string
parsed_date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
print(parsed_date)
