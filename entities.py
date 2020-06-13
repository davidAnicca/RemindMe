class Event:
    def __init__(self, title, date, time):
        self._title = title
        self._date = date
        self._time = time

    def get_title(self):
        return self._title

    def get_date(self):
        return self._date

    def get_time(self):
        return self._time

