import re
import webbrowser as wb
from datetime import datetime


rat = """


"""

def load_coordinates():
    lines = rat.split('\n')
    for line in lines:
        if is_valid_coordinate(line):
            wb.open(f'https://www.google.com/maps/place/{line}')

def load_trips():
    trips = ''
    lines = rat.split('\n')
    for line in lines:
        if is_valid_coordinate(line):
            trips += f'{line}/'
    wb.open(f'https://www.google.com/maps/dir/{trips}')

def is_valid_coordinate(coord):
  """
  This function checks if a string is a valid coordinate format (latitude,longitude).

  Args:
      coord: The string to be checked.

  Returns:
      True if the string is a valid coordinate format, False otherwise.
  """
  regex = r"^[-+]?\d+\.\d+(,\s*[-+]?\d+\.\d+)?$"
  return bool(re.match(regex, coord))

def is_valid_time(time_str):
  """
  Checks if the given string is a valid digital time format (HH:MM).

  Args:
      time_str: The string to validate.

  Returns:
      True if the string is a valid digital time, False otherwise.
  """
  try:
    # Try converting the string to a datetime object with time only format
    datetime.strptime(time_str, "%H:%M")
    return True
  except ValueError:
    # If conversion fails, it's not a valid time format
    return False

def is_valid_date(date_str):
  """
  Checks if the given string is a valid date in the format "DD MMM YYYY".

  Args:
      date_str: The string to validate.

  Returns:
      True if the string is a valid date, False otherwise.
  """
  try:
    # Try converting the string to a datetime object with the specified format
    datetime.strptime(date_str, "%d %b %Y")
    return True
  except ValueError:
    # If conversion fails, it's not a valid date format
    return False

def combine_datetime(date_str, time_str):
  """
  Combines a valid time string and a valid date string into a datetime object.

  Args:
      time_str: The time string in HH:MM format.
      date_str: The date string in DD MMM YYYY format.

  Returns:
      A datetime object representing the combined date and time, 
      or None if either input string is invalid.
  """
  try:
    # Parse the date string
    date_obj = datetime.strptime(date_str, "%d %b %Y")
    # Parse the time string (assuming 24-hour format)
    time_obj = datetime.strptime(time_str, "%H:%M").time()
    # Combine date and time into a datetime object
    return datetime.combine(date_obj, time_obj)
  except ValueError:
    # Handle invalid input formats
    return None

    
def get_rat_page(data):
    """Loads important info from a page, handling date, time, MR number,
       bank/private, and access flags.

    Args:
        data (str): The text content of the page.

    Returns:
        list: A list of tuples containing (datetime, MR number).
    """

    app_list = []
    bank_property = 'Pvt'
    access = 'access'

    for line in data.split('\n'):
        if is_valid_time(line):
            time = line
        elif is_valid_date(line):
            date = line
        elif 'MR' in line:
            mr_number = line[:8]
            if 'Access has not been arranged' in line:
                access = 'No access'
        elif line in ('Standard Bank', 'FNB Housing Finance .', 'SA Home Loans'):
            bank_property = 'Bank'
        elif 'View Comment' in line:
            # The assumtion is: View Comment means end of the appointment. Hence, put the data together
            app_list.append((combine_datetime(date, time), f'{mr_number} {bank_property} {access}'))
            # Reset
            bank_property = 'Pvt'
            access = 'access'

    return app_list

def wa_datetime_convert(string):
    try:
        # Remove the square brackets and split the string by comma
        date_time_list = string[1:-1].split(",")

        # Combine the date and time parts into a single string
        datetime_str = " ".join(date_time_list)

        # Convert the string to a datetime object
        datetime_obj = datetime.strptime(datetime_str, "%H:%M %d/%m/%Y")
    except ValueError:
        # Check if it's a time not datetime
        try:
            # Try converting with both AM and PM formats
            string = string.strip()  # Remove leading/trailing spaces
            datetime_obj = datetime.strptime(string, "%H%p").time()
        except ValueError:
            try:
                datetime_obj = datetime.strptime(string, "%H:%M").time()
            except:
                return
        
    return datetime_obj

def get_watsapp_page(data):
    """Loads important info from a page, handling date, time, MR number, and bank/property flags.

    Args:
        data (str): The text content of the page.

    Returns:
        list: A list of tuples containing (datetime, appointment).
    """

    app_list = []
    for line in data.split('\n'):
        if 'Aidhin:' in line:
            if 'i have access' in line.lower():
                index = line.lower().find('to')
                app = line[index+3:]
                app = app.split('.')[0]
##                app = wa_datetime_convert(app)
                time = line[:19]
                app_list.append((wa_datetime_convert(time), app))
            elif 'note:' in line.lower():
                index = line.lower().find('note:')
                note = line[index:]            
    return app_list

    

if __name__ == "__main__":
    print(load_coordinates())

