from datetime import datetime

date_format = "%H:%M, %d/%m/%Y"

def has_date_time(str):
    # Define the format string matching the input string
    try:
    # Parse the string and create the datetime object
        datetime.strptime(str[1:18], date_format)
        return True
    except:
        return False

def extract_date_time(str):
    # Define the format string matching the input string
    try:
    # Parse the string and create the datetime object
        date_time_obj = datetime.strptime(str[1:18], date_format)
    except:
        print(str)
        date_time_obj = datetime.now()
    return date_time_obj

def get_wa_page(data):
    """Loads important info from watsapp, handling datetime, MR number,
       and mileage

    Args:
        data (str): The text content of the page.

    Returns:
        list: A list of tuples containing
        (datetime, MR number, and travel distance).
    """

    app_list = []
    previous_mileage = 0
    non_num_message = ''
    for line in data.split('\n'):
        if line.isalnum():
            message = line
        else:
            message = line[line.find(':', 10)+2:]
            
        if message == '':
            continue
        
        if message[0].isnumeric():
            mileage = line[line.find(':', 10)+1:]
            if '?' in mileage:
                mileage = int(mileage[:-1])
            else:
                mileage = int(mileage)
            distance = mileage - previous_mileage
            previous_mileage = mileage
            
            if non_num_message:
                app_list.append((date_time, non_num_message, distance))
        else:
            non_num_message = message
            date_time = extract_date_time(line) #Issue
            
            
    return app_list

def copy_fuel_claim(data):
    """get_wa_page and copy to clipboard.

    Args:
        data (str): The text content of the page.

    Returns:
        str: A str of the fuel claim with tabs. Mean't to be pasted in the
        fuel claim.
    """
    apps = get_wa_page(data)
    string = ''
    previous_date = apps[0][0].date()
    for datetime, name, distance in apps:
##        if datetime.date() != previous_date:
##            string=f'{string}\n{name}\t{distance}\t' # Next line
        string=f'{string}{name}\t{distance}\t'
    
    return string

if __name__ == "__main__":
    data = """[08:51, 08/07/2024] Aidhin: 32
MR639260
[09:23, 08/07/2024] Aidhin: 68
[10:42, 08/07/2024] Aidhin: MR638178
81?
[12:05, 08/07/2024] Aidhin: MR630486
91
[13:56, 08/07/2024] Aidhin: Home
134

[10:42, 09/07/2024] Aidhin: 135
[10:42, 09/07/2024] Aidhin: MR638178
235
"""
    print(get_wa_page(data))
   

