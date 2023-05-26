# Get results data from web pages
from bs4 import BeautifulSoup
# from html.parser import HTMLParser

def get_relays(page):

    soup = BeautifulSoup(page, 'html.parser')
    r = soup.find('pre').text
    r = r.splitlines()
    lst = []

    # Get event details
    try:
        event_details = r[5]
        event_details = event_details.split()

        if event_details[6].strip().lower() != 'class':
            event = event_details[4] + " " + event_details[5].strip()+ " " + event_details[6].strip()
        else:
            event = event_details[4] + " " + event_details[5].strip()

        cl = event_details[-1] if event_details[-1].isnumeric() else event_details[-2].strip()
        gender = event_details[2].strip()
    except IndexError:
        event_details = 'error'

    # Event Results
    for line in r:
        try:
            my_dict = {}
            if len(line) > 0:
                clean_line = line.split('  ')
                clean_line = list(filter(None, clean_line))

                if (clean_line[0][0].isnumeric() and clean_line[0][1] != ')') or (clean_line[0].strip()[0:2].isnumeric() and clean_line[0].strip()[2] != ')'):
                    if (clean_line[0].strip()[2] != '.' and clean_line[0].strip()[1] != '.' ):
                        position = clean_line[0].strip().split(' ',1)[0]
                        school = clean_line[0].strip().split(' ',1)[1]

                        my_dict['event'] = event
                        my_dict['class'] = cl
                        my_dict['gender'] = gender
                        my_dict['position'] = position
                        my_dict['name'] = ''
                        my_dict['school'] = school
                
                        try:
                            if clean_line[-1].strip() != '' and clean_line[-1].strip().isnumeric():
                                points = clean_line[-1].strip()
                            elif clean_line[-1].strip() == '' and clean_line[-2].strip().isnumeric():
                                points = clean_line[-2].strip()
                            else:
                                points = 0
                            mark = clean_line[1].strip()
                            my_dict['mark'] = mark
                            my_dict['points'] = points
                        except IndexError:
                            points = 0
                            mark = clean_line[-2].strip()
                            my_dict['mark'] = mark
                            my_dict['points'] = points
                        lst.append(my_dict)
        except IndexError:
            continue
    return lst


def get_races(page):
    soup = BeautifulSoup(page, 'html.parser')
    r = soup.find('pre').text
    r = r.splitlines()
    lst = []

    # Get event details
    event_details = r[5]
    event_details = event_details.split()

    if event_details[6].strip().lower() != 'class' and event_details[6].strip().lower() != 'open':
        event = event_details[4] + " " + event_details[5].strip()+ " " + event_details[6].strip()
    else:
        event = event_details[4] + " " + event_details[5].strip()

    if event_details[-1].isnumeric():
        cl = event_details[-1]
    elif event_details[-1].lower() == 'open' or event_details[-1].lower() == 'hurdles':
        cl = 0
    else:
        cl = event_details[-2].strip()

    gender = event_details[2].strip()
    
    # Event Results
    for line in r:
        my_dict = {}
        if len(line) > 0:
            clean_line = line.split('  ')
            clean_line = list(filter(None, clean_line))
            
            if (clean_line[0][0].isnumeric() and clean_line[0][1] != ')') or (clean_line[0].strip()[0:2].isnumeric() and clean_line[0].strip()[2] != ')'):
                position = clean_line[0].strip().split(' ',1)[0]
                name = clean_line[0].strip().split(' ',1)[1]
                school = clean_line[1].strip()
                
                my_dict['event'] = event
                my_dict['class'] = cl
                my_dict['gender'] = gender
                my_dict['position'] = position
                my_dict['name'] = name
                my_dict['school'] = school
                
                try:
                    if clean_line[-1].strip() != '' and clean_line[-1].strip().isnumeric():
                        points = clean_line[-1].strip()
                    elif clean_line[-1].strip() == '' and clean_line[-2].strip().isnumeric():
                        points = clean_line[-2].strip()
                    else:
                        points = 0
                    mark = clean_line[2].strip()
                    my_dict['mark'] = mark
                    my_dict['points'] = points
                except IndexError:
                    points = 0
                    mark = clean_line[-1].strip()
                    my_dict['mark'] = mark
                    my_dict['points'] = points
                lst.append(my_dict)
    return lst


def get_field_events(page):

    soup = BeautifulSoup(page, 'html.parser')
    r = soup.find('pre').text
    r = r.splitlines()
    lst = []

    # Get event details
    event_details = r[5]
    event_details = event_details.split()

    if event_details[6].strip().lower() != 'class' and event_details[6].strip().lower() != 'open':
        event = event_details[4] + " " + event_details[5].strip()+ " " + event_details[6].strip()
    else:
        event = event_details[4] + " " + event_details[5].strip()

    if event_details[-1].isnumeric():
        cl = event_details[-1]
    elif event_details[-1].lower() == 'open':
        cl = 0
    else:
        cl = event_details[-2].strip()

    gender = event_details[2].strip()

    # Event Results
    for line in r:
        my_dict = {}
        if len(line) > 0:
            clean_line = line.split('  ')
            clean_line = list(filter(None, clean_line))

            if (clean_line[0][0].isnumeric() and clean_line[0][1] != ')') or (clean_line[0].strip()[0:2].isnumeric() and clean_line[0].strip()[2] != ')'):
                if (clean_line[0].strip()[2] != '.' and clean_line[0].strip()[1] != '.'):
                    position = clean_line[0].strip().split(' ',1)[0]
                    name = clean_line[0].strip().split(' ',1)[1]
                    school = clean_line[1].strip()
                    my_dict['event'] = event
                    my_dict['class'] = cl
                    my_dict['gender'] = gender
                    my_dict['position'] = position
                    my_dict['name'] = name
                    my_dict['school'] = school
            
                    try:
                        if clean_line[-1].strip() != '' and clean_line[-1].strip().isnumeric():
                            points = clean_line[-1].strip()
                        elif clean_line[-1].strip() == '' and clean_line[-2].strip().isnumeric():
                            points = clean_line[-2].strip()
                        else:
                            points = 0
                        mark = clean_line[2].strip()
                        my_dict['mark'] = mark
                        my_dict['points'] = points
                    except IndexError:
                        points = 0
                        mark = clean_line[-1].strip()
                        my_dict['mark'] = mark
                        my_dict['points'] = points
                    lst.append(my_dict)
    return lst