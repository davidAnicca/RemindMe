from entities import *

#i have modified a file

def data_in():
    event_list = []
    input_file = open("data", "r")
    line = input_file.readline()
    while line:
        information = line.strip().split("+")
        title_in = information[0]
        date_in = information[1]
        time_in = information[2]
        event_in = Event(title_in, date_in, time_in)
        event_list.append(event_in)
        line = input_file.readline()
    input_file.close()
    return event_list


def sort_key(element):
    date_elements = element.get_date().split("-")
    return date_elements[2] + date_elements[1] + date_elements[0] + element.get_time()


def data_sort(event_list):
    event_list.sort(key=sort_key)


def data_out(event_list):
    data_sort(event_list)
    output_file = open("data", "w")
    for event in event_list:
        output_file.write(event.get_title() + "+" + event.get_date() + "+" + event.get_time() + "\n")
