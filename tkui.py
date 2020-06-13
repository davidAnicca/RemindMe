from tkinter import *
from typing import List

from services import *
from data_backup import *
from functools import partial

screen = Tk()
screen.geometry('350x300')
screen.title("Remind Me")


def print_win_grid(where, info, row, column):
    Label(where, text=info).grid(row=row, column=column, pady=1, padx=35, sticky="W")


def clear_win(where):
    for widget in where.winfo_children():
        widget.destroy()


def date_tod(where, row, col):
    print_win_grid(where, "", row, col)
    print_win_grid(where, "today:", row + 1, 0)
    print_win_grid(where, today_date(), row + 1, 1)


def go_to_del(where, name_to_del, row, from_where, events):
    validation = del_event(name_to_del.get(), events)
    if validation:
        print_win_grid(where, "event deleted successfully", row + 1, 1)
        if from_where != screen:
            from_where.destroy()
        main_screen(events)
    else:
        print_win_grid(where, "try_again", row, 0)


def delete_screen(from_where, events):
    del_sc = Tk()
    del_sc.geometry("350x700")
    rows_filled = show_events(1, del_sc, events)
    Label(del_sc, text="name to delete").grid(row=rows_filled + 2, column=0)
    name_to_del = Entry(del_sc)
    name_to_del.grid(row=rows_filled + 2, column=1)
    ok_butt = Button(del_sc, text="ok", height=1, width=5,
                     command=partial(go_to_del, del_sc, name_to_del, rows_filled + 3, from_where, events))
    ok_butt.grid(row=rows_filled + 3, column=0)
    Label(del_sc, text="").grid(row=rows_filled + 4, column=0)
    close_button(del_sc, rows_filled + 5, 0)


def del_button(where, row, col, events):
    del_butt = Button(where, text="remove one", command=partial(delete_screen, where, events))
    del_butt.grid(row=row, column=col)


def show_events(all_ev, where, events):
    try:
        clear_win(where)
    except TclError:
        exit(0)
    refresh(events)
    if all_ev == 0:
        print_win_grid(where, "Today events", 0, 1)
    else:
        print_win_grid(where, "All events", 0, 1)
    print_win_grid(where, "", 1, 0)
    print_win_grid(where, "Name", 2, 0)
    print_win_grid(where, "Date", 2, 1)
    print_win_grid(where, "Time", 2, 2)
    if all_ev == 0:
        events_today = today(events)
    else:
        events_today = events
    row = 3
    if len(events_today) == 0:
        print_win_grid(where, "No events", 3, 1)
    else:
        for event in events_today:
            row += 1
            title = event.get_title()
            date_today = event.get_date()
            time_today = event.get_time()
            print_win_grid(where, title, row, 0)
            print_win_grid(where, date_today, row, 1)
            print_win_grid(where, time_today, row, 2)
    return row


def close_button(where, row, col):
    Button(where, text="close", height=1, width=5, command=where.destroy).grid(row=row, column=col)


def try_again(from_where, where, events):
    where.destroy()
    add_screen(from_where, events)


def ok(title, day, month, year, hour, minute, from_where, add_sc, events):
    validation = add_event(title.get(), day.get(), month.get(), year.get(), hour.get(), minute.get(), events)
    if validation:
        if from_where != screen:
            from_where.destroy()
        add_sc.destroy()
        main_screen(events)
    else:
        clear_win(add_sc)
        print_win_grid(add_sc, "invalid data", 0, 1)
        try_ag = Button(add_sc, text="try again", height=1, width=10,
                        command=partial(try_again, from_where, add_sc, events))
        try_ag.grid(row=1, column=1)


def add_screen(where, events):
    add_sc = Tk()
    add_sc.title("Add an event")
    add_sc.geometry("300x300")
    clear_win(add_sc)
    Label(add_sc, text="title").grid(row=0, column=0)
    title = Entry(add_sc)
    title.grid(row=0, column=1)
    Label(add_sc, text="day").grid(row=1, column=0)
    day = Entry(add_sc)
    day.grid(row=1, column=1)
    Label(add_sc, text="month").grid(row=2, column=0)
    month = Entry(add_sc)
    month.grid(row=2, column=1)
    Label(add_sc, text="year").grid(row=3, column=0)
    year = Entry(add_sc)
    year.grid(row=3, column=1)
    Label(add_sc, text="time").grid(row=4, column=0)
    hour = Entry(add_sc, width=10)
    hour.grid(row=4, column=1, sticky="W")
    minute = Entry(add_sc, width=10)
    minute.grid(row=4, column=1, sticky="E")
    Label(add_sc, text="hh:mm").grid(row=5, column=1)

    ok_button = Button(add_sc, text="ok",
                       command=partial(ok, title, day, month, year, hour, minute, where, add_sc, events),
                       height=1, width=5)
    ok_button.grid(row=7, column=1)
    close_button(add_sc, 8, 1)
    date_tod(add_sc, 9, 0)
    add_sc.mainloop()


def add_button(where, row, col, events):
    add_butt = Button(where, text="add", command=partial(add_screen, where, events), height=1, width=5, )
    add_butt.grid(row=row, column=col)


def second_screen(events):
    second = Tk()
    second.title("All events")
    second.geometry("350x700")
    rows_filled = show_events(1, second, events)
    Label(second).grid(row=rows_filled + 1, column=0)
    close_button(second, rows_filled + 2, 0)
    add_button(second, rows_filled + 2, 1, events)
    date_tod(second, rows_filled + 3, 0)
    del_button(second, rows_filled + 2, 2, events)
    second.mainloop()


def main_screen(events):
    rows_filled = show_events(0, screen, events)
    see_all = Button(screen, text="others", height=1, width=5, command=partial(second_screen, events))
    print_win_grid(screen, "", rows_filled + 1, 0)
    see_all.grid(row=rows_filled + 2, column=0)
    close_button(screen, rows_filled + 2, 1)
    add_button(screen, rows_filled + 2, 2, events)
    date_tod(screen, rows_filled + 3, 0)
    print_win_grid(screen, "", rows_filled + 5, 0)
    del_button(screen, rows_filled + 5, 0, events)


def run():
    events = data_in()
    main_screen(events)
    screen.mainloop()


run()
