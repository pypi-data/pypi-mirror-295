import tqdm
import json
import pandas as pd
import numpy as np
import requests

class Timetable():
    """
    Class for interaction with timetable service

    Args:
        url (str): The URL of the JSON file to download.
    """

    def __init__(self, num):
        self.url = "https://cau.edupage.org/timetable/server/regulartt.js?__func=regularttGetData"
        self.payload = {"__args":["null",f"{num}"],"__gsh":"00000000"}

    def download(self):
        """
        Download a JSON file from a URL and return the JSON data.
        """
        response = requests.post(self.url, stream=True, json=self.payload)

        total_size = int(response.headers.get('content-length', 0))

        progress_bar = tqdm.tqdm(total=total_size, unit='iB', unit_scale=True)

        with open('data.json', 'wb') as file:

            for data in response.iter_content(1024):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        # If the download was successful, print a message
        if total_size != 0 and progress_bar.n != total_size:
            print("Error: something went wrong")
        else:
            print("Download successful!")

    def parse_to_df(self):
        """
        Parse JSON Timetable data into dataframes. Can be useful for analytics
        and complex tasks that easier perform with dataframes neither JSON.

        Args:
            self
        """
        with open("data.json", "r", encoding="utf8") as file:
            self.data = json.load(file)

        tables = self.data["r"]["dbiAccessorRes"]["tables"]

        # Classes - to get information about
        classes = tables[12]["data_rows"]
        self.df_classes = pd.DataFrame(classes)
        
        # Groups - to get information about
        groups = tables[15]["data_rows"]
        self.df_groups = pd.DataFrame(groups)
        
        # Periods - to get information about
        periods = tables[1]['data_rows']
        self.df_periods = pd.DataFrame(periods)

        # Cards - to get information about
        cards = tables[20]["data_rows"]
        self.df_cards = pd.DataFrame(cards)

        # Lessons - to get information about
        lessons = tables[18]["data_rows"]
        self.df_lessons = pd.DataFrame(lessons)
        
        # Classrooms - to get information about
        classrooms = tables[11]["data_rows"]
        self.df_classrooms = pd.DataFrame(classrooms)
        
        # Subjects - to get information about
        subjects = tables[13]["data_rows"]
        self.df_subjects = pd.DataFrame(subjects)

    def get_week_by_class_id(self, class_id: str) -> dict:
        """
        Get the weekly timetable by classId.

        Args:
            class_id (str): id of the group for which we looking timetable for, usually has format "*N", where N is number.

        Return:
            week (dict): JSON that contain the timetable of group with class_id.
        """
        self.parse_to_df()
        lessons = self.df_lessons[self.df_lessons['classids'].apply(lambda x: class_id in x)]
        cards = self.df_cards[self.df_cards['lessonid'].apply(lambda x: x in lessons['id'].tolist())]

        # Cards
        data = pd.merge(self.df_periods, cards, left_on='id', right_on='period')
        data = data[['starttime', 'endtime', 'lessonid', 'days', 'classroomids']]

        # Lessons
        data = pd.merge(data, lessons, left_on='lessonid', right_on='id')
        data = data[['starttime', 'endtime', 'durationperiods', 'days', 'classroomids', 'subjectid']]

        # Subjects
        data = pd.merge(data, self.df_subjects, left_on='subjectid', right_on='id')
        data = data[['starttime', 'endtime', 'durationperiods', 'days', 'classroomids', 'name', 'color']]
        
        # Classrooms
        data['classroomids'] = data['classroomids'].apply(lambda x: x[0])
        data = pd.merge(data, self.df_classrooms, left_on='classroomids', right_on='id')
        data = data[['starttime', 'endtime', 'durationperiods', 'days', 'name_x', 'color_x', 'name_y']]
        data = data.rename(columns={"starttime": "start", "endtime": "end", 'durationperiods': 'period', 'name_x': 'subject', 'color_x': 'color','name_y': 'classroom'})
        
        days = data['days'].unique()
        days = np.sort(days)[::-1]
        
        week = {}
        for i, day in enumerate(days):
            week[i] = data[data['days'] == day].to_dict(orient='records')
        
        return week

    def get_groups(self):
        self.parse_to_df()
        groups = dict()
        for _class in self.df_classes[['id', 'name']].to_dict(orient="records"):
            groups[_class['name']] = _class['id']

        return groups
