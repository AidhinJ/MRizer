import requests
import rat_info

data = """

"""
# Priority
inactive = ["Inactive:"]
first = ['First Priority (Active without photos):']
secondary = ['Secondary:']

for time, mr in rat_info.get_rat_page(data):
    prop = requests.get(f'https://www.myroof.co.za/{mr[:8]}')
    index = prop.text.find('Property Photos')
    prop_photos = prop.text[index:index+1000]
    
    if index == -1:  # Inactive
        inactive.append(mr)
    elif 'title=""' in prop_photos:
        first.append(mr)
    else:
        secondary.append(mr)

for priority in (first, secondary, inactive):
    for mr in priority:
        if len(mr) > 1:
            print(mr)
    print()
