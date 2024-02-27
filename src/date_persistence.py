from datetime import datetime

def save_start_date(date, filename):
    """Save the start date to a file."""
    with open(filename, 'w') as file:
        file.write(date.strftime("%d.%m.%Y"))

def load_start_date(default_date_str, filename):
    """Load the start date from a file, or use the default if the file doesn't exist."""
    try:
        with open(filename, 'r') as file:
            date_str = file.read().strip()
        return datetime.strptime(date_str, "%d.%m.%Y")
    except (IOError, ValueError):
        # If file does not exist or contains invalid date, use default
        return datetime.strptime(default_date_str, "%d.%m.%Y")
