import calendar


class BirthdayCalendar(calendar.HTMLCalendar):
    def __init__(self, birthday_day=None, birthday_month=None):
        super().__init__(firstweekday=0)
        self.birthday_day = birthday_day
        self.birthday_month = birthday_month
        self.current_month = None

    def formatday(self, day, weekday):
        if day == 0:
            return "<td class='noday'>&nbsp;</td>"

        is_birthday = (
            self.birthday_day == day and
            self.birthday_month == self.current_month
        )

        if is_birthday:
            return f"<td class='birthday'>{day}</td>"

        return f"<td>{day}</td>"

    def formatmonth(self, year, month, withyear=True):
        self.current_month = month
        return super().formatmonth(year, month, withyear)