from datetime import *
from entities import *
from data_backup import *


def today_date():
    date_x_time = datetime.now()
    return date_x_time.strftime("%d") + "-" + date_x_time.strftime("%m") + "-" + date_x_time.strftime("%y")


def refresh(events):
    for event in events:
        day, month, year = event.get_date().split("-")
        hour, minute = event.get_time().split(":")
        if year < datetime.now().strftime("%y"):
            events.remove(event)
        elif month < datetime.now().strftime("%m") and year == datetime.now().strftime("%y"):
            events.remove(event)
        elif day < datetime.now().strftime("%d") and month == datetime.now().strftime("%m"):
            events.remove(event)
        elif hour < datetime.now().strftime("%H") and day == datetime.now().strftime("%d"):
            events.remove(event)
        elif minute < datetime.now().strftime("%M") and hour == datetime.now().strftime("%H"):
            events.remove(event)
    data_out(events)


def validate(day, month, year, hour, minute):
    elements = [day, month, year, hour, minute]
    if "" in elements:
        return 0
    if len(year) == 2 and int(year) < 20:
        return 0
    if len(year) == 4 and int(year) < 2020:
        return 0
    for element in elements:
        try:
            int(element)
        except ValueError:
            return 0
    if int(month) == 2:
        if int(year) % 4 == 1 and int(year) % 100 != 0:
            if int(day >= 29):
                return 0
        elif int(day >= 28):
            return 0
    month_with_31 = ['01', '03', '05', '07', '08', '10', '12']
    if int(month) > 12:
        return 0
    if month in month_with_31:
        if int(day) > 31:
            return 0
    if month not in month_with_31 and int(month) != 2:
        if int(day) > 30:
            return 0
    if int(hour) > 23:
        return 0
    if int(minute) > 59:
        return 0
    return 1


def add_event(title, day, month, year, hour, minute, events):
    if validate(day, month, year, hour, minute):
        if len(year) == 4:
            short_year = year[2] + year[3]
            year = short_year
        if len(day) == 1:
            day = '0' + day
        if len(month) == 1:
            month = '0' + month
        if len(minute) == 1:
            minute = '0' + minute
        if len(hour) == 1:
            hour = '0' + hour
        new_title = title
        new_date = day + "-" + month + "-" + year
        new_time = hour + ":" + minute
        new_event = Event(new_title, new_date, new_time)
        events.append(new_event)
        refresh(events)
        data_out(events)
        return 1
    else:
        return 0


def del_event(name_to_del, events):
    for event in events:
        if event.get_title() == name_to_del:
            events.remove(event)
            data_out(events)
            return 1
    return 0


def today(events):
    events_today = []
    for event in events:
        if event.get_date() == today_date():
            events_today.append(event)
    return events_today
