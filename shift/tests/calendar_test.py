import calendar
from collections import deque
import datetime

# 参考文献: https://blog.narito.ninja/detail/11/

now = datetime.datetime.now()

class BaseCalendarMixin:
    """カレンダー関連Mixinの、基底クラス"""
    first_weekday = 0  # 0は月曜から、1は火曜から。6なら日曜日からになります。
    week_names = ['月', '火', '水', '木', '金', '土', '日']  # これは、月曜日から書くことを想定します。['Mon', 'Tue'...

    def setup_calendar(self):
        """内部カレンダーの設定処理
        calendar.Calendarクラスの機能を利用するため、インスタンス化します。
        Calendarクラスのmonthdatescalendarメソッドを利用していますが、デフォルトが月曜日からで、
        火曜日から表示したい(first_weekday=1)、といったケースに対応するためのセットアップ処理です。
        """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """first_weekday(最初に表示される曜日)にあわせて、week_namesをシフトする"""
        # dequeしたものはrotateメソッドを持つ. deque.rotate(number)で, number分だけ要素を左にずらしていく. 
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)  
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    """月間カレンダーの機能を提供するMixin"""
    def get_previous_month(self, date):
        """前月を返す"""
        if date.month == 1:
            return date.replace(year=date.year-1, month=12, day=1)
        else:
            return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """次月を返す"""
        if date.month == 12:
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """その月の全ての日を返す"""
        # 帰ってくるのはdatetime型が格納された配列
        # monthdatescalendarは, pythonに組み込まれている. 
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self, _month, _year):
        """現在の月を返す"""
        # 引数の渡し方を変える
        month = _month
        year = _year

        # month = self.kwargs.get('month')
        # year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self, _month, _year):
        """月間カレンダー情報の入った辞書を返す"""
        self.setup_calendar()
        current_month = self.get_current_month(_month, _year)
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data

def week_name_test():
    demo_calendar = BaseCalendarMixin()
    week_names = deque(demo_calendar.week_names)
    week_names.rotate(1)
    print(week_names)

def month_days_test():
    demo_calendar = MonthCalendarMixin()
    demo_calendar.setup_calendar()
    print(demo_calendar.get_month_days(now))

def current_month_test():
    demo_calendar = MonthCalendarMixin()
    print(demo_calendar.get_current_month(now.month, now.year))

def month_calendar_test():
    demo_calendar = MonthCalendarMixin()
    print(demo_calendar.get_month_calendar(now.month, now.year))

# week_name_test()
# month_days_test()
# current_month_test()
month_calendar_test()