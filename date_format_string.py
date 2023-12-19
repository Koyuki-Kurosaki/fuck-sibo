from datetime import timedelta


class DateIterator:
    def __init__(self, start_date, end_date):
        self.current_date = start_date
        self.end_date = end_date

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_date > self.end_date:
            raise StopIteration

        formatted_date = self.current_date.strftime("%Y-%m-%dT%H:%M:%S")
        self.current_date += timedelta(days=7)  # Increment by one week
        return formatted_date
