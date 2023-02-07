import numpy as np
from datetime import time
from datetime import date
from datetime import timedelta

from data.dataframe import df

SCHEDULE_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
GYM_DURATION = timedelta(3,0)
POSSIBLE_START = time(9,0)
POSSIBLE_END = time(23,0)
TIMES = ['Start', 'Finish']


class Generator:
    def __init__(self) -> None:
        self.schedule = self.init_schedule()
        print(self.schedule)
        self.space = self.find_space()

    """ INIT """

    def init_schedule(self) -> object:
        """
        Initiate the schedule
        """

        # Set the start and end day for the schedule
        start_date = self.get_start_day()
        end_date = self.get_end_day()

        # Calculate the amount of days to be scheduled
        scheduling_days = (end_date - start_date).days

        # Set the amount of weeks, days and shifts to be scheduled
        weeks = scheduling_days // len(SCHEDULE_DAYS)
        days = len(SCHEDULE_DAYS)
        occupation = len(TIMES)

        # Create schedule
        schedule = np.empty((weeks, days, occupation), dtype=list)

        # Fill schedule with empty lists
        # So that more employees can work during the same shift
        for week_num, week in enumerate(schedule):
            for day_num in range(len(week)):

                    if df.iloc[day_num]['Start'] != None or df.iloc[day_num]['Finish'] != None:
                        # Set time from df as strings
                        start_time = df.iloc[day_num]['Start']
                        finish_time = df.iloc[day_num]['Finish']

                        # Save in schedule as time objects
                        schedule[week_num][day_num][0] = self.convert_time(start_time)
                        schedule[week_num][day_num][1] = self.convert_time(finish_time)
                    else:
                        schedule[week_num][day_num][0] = None
                        schedule[week_num][day_num][1] = None

        return schedule

    """ GET """

    def get_date(self) -> object:
        """
        Find the current date
        """
        return date.today()

    def get_day(self, date) -> str:
        """
        Find the day of a certain date
        """
        return date.strftime("%A")

    def get_start_day(self) -> object:
        """
        Find date of start of schedule
        """
        return self.get_schedule_boundary(start=True)

    def get_end_day(self) -> object:
        """
        Find date of end of schedule
        """
        return self.get_schedule_boundary(start=False)

    def get_schedule_boundary(self, start) -> object:
        """
        Find date of start or end of schedule
        """

        # Set start or end date
        schedule_date = self.get_date()

        # Set starting month
        start_month = schedule_date.month

        # Set day increase for increasing day count
        day_increase = timedelta(1)

        # Set schedule day
        schedule_day = self.get_day(schedule_date)

        # Find start or end date
        # Start of the schdedule: a Monday
        # End of the schdedule: day before Monday and in next month
        while schedule_day != 'Monday' or (not start and schedule_date.month != start_month + 1):
            schedule_date = schedule_date + day_increase
            schedule_day = self.get_day(schedule_date)

        return schedule_date


    """ METHODS """

    def find_space(self) -> dict:
        """
        Method to find possible spaces
        """

        space = {}

        for week_num, week in enumerate(self.schedule):
            if week_num not in space:
                space[week_num] = {}

            for day_num, day in enumerate(week):
                if day_num not in space[week_num]:
                    space[week_num][day_num] = {}

                dictionary_entry = space[week_num][day_num]

                dictionary_entry['Start'], dictionary_entry['Finish']= self.read_day(day)

        return space

    def read_day(self, occupation:list) -> list:

        possible_time = []

        if occupation == None:
            possible_time.append(f'{POSSIBLE_START + GYM_DURATION}-{POSSIBLE_END - GYM_DURATION}')
        else:
            start_time, finish_time = occupation.split('-')

            if int(start_time) > POSSIBLE_START + GYM_DURATION:
                possible_time.append(f'{POSSIBLE_START + GYM_DURATION}-{start_time}')

            if int(finish_time) < POSSIBLE_END - GYM_DURATION and int(finish_time) > POSSIBLE_START:
                possible_time.append(f'{finish_time}-{POSSIBLE_END - GYM_DURATION}')

        return possible_time

    def convert_time(self, string:str) -> object:
        return time(int(string[:-2]), int(string[-2:]))