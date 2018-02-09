from datetime import time

default_schedules = [
        {'shop': None, 'daytype': 1, 'periodtype': 1, 'period_start': time(10, 0),
         'period_end': time(19, 0), 'is_working': True},
        {'shop': None, 'daytype': 1, 'periodtype': 2, 'period_start': time(12, 0),
         'period_end': time(13, 0), 'is_working': False},
        {'shop': None, 'daytype': 1, 'periodtype': 3, 'period_start': time(15, 30),
         'period_end': time(16, 0), 'is_working': False},
        {'shop': None, 'daytype': 2, 'periodtype': 1, 'period_start': time(11, 0),
         'period_end': time(18, 0), 'is_working': True},
        {'shop': None, 'daytype': 2, 'periodtype': 2, 'period_start': time(13, 0),
         'period_end': time(14, 0), 'is_working': False},
    ]

