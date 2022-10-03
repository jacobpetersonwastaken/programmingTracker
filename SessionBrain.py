from json import load
from datetime import datetime
from pandas import DataFrame
from ctypes import windll
from PixelaCode import PixelaCode
from PlayVideo import PlayVideo
from os import getenv


class SessionBrain:
    """Decides if any of the programs logged are overlapping and gives accurate count of hours to log to pixela"""
    hours_to_log = 0
    date_to_log = ""
    today = datetime.now().strftime('%Y%m%d')
    dates_to_upload = []
    pixela = PixelaCode()

    def sum_day_time(self, date_to_sum):
        with open('runtime_sessions.json', 'r') as f:
            data = load(f)
        """Creates useable list for the df aka dataframe"""
        start_list = []
        for i in data[date_to_sum]:
            name = i
            for p in data[date_to_sum][name]:
                p["program_name"] = name
                start_list.append(p)
        df = DataFrame(start_list)
        """Gets first start time, how many hours it was up then adds it to the count"""
        min_start_df = df.iloc[[df["start_time"].idxmin()]]
        start_hours = [sum(i) for i in min_start_df["session_in_hours"]]
        self.hours_to_log += start_hours[0]

        max_end_df = df.iloc[[df["end_time"].idxmax()]]

        """checks if the first entry is also the last. If its not we cycle through all the end times greater"""
        if int(min_start_df["end_time"]) != int(max_end_df["end_time"]):
            min_end = int(min_start_df["end_time"])
            max_log = df.loc[df["end_time"] > min_end]
            vals = []
            """Add all the logs that end later to a list"""
            for (start, end, hours) in zip(max_log["start_time"], max_log["end_time"], max_log["session_in_hours"]):
                vals.append((start, end, sum(hours)))
            """cycles through list of greater end times and if its the first round compares it to the starting entry
            then any greater compare time to the previous one before"""
            for i, v in enumerate(vals):
                if i == 0:
                    if vals[i][0] < min_end:
                        self.hours_to_log += vals[i][1] - min_end
                    else:
                        self.hours_to_log += vals[i][2]
                else:
                    if vals[i - 1][1] < vals[i][1]:
                        self.hours_to_log += vals[i][1] - vals[i - 1][1]
                    else:
                        self.hours_to_log += vals[i][2]

    def upload(self):
        """pushes to pixela, if successful it logs push"""
        if self.pixela.upload_to_pixela(hours=self.hours_to_log,
                                        log_date=self.date_to_log):
            self.pixela.log_pixela_push(self.date_to_log)
            pl = PlayVideo()
            file_path = getenv('MEDIA_2_FILE_PATH')
            pl.play_video(fr"{file_path}", 5)
        else:
            pl = PlayVideo()
            file_path2 = getenv('MEDIA_3_FILE_PATH')
            pl.play_video(fr"{file_path2}", 6)

    def session_upload(self):
        """sums the total hours for each new day that hasn't been logged yet."""
        """Checks if there are any time differences from the last upload"""
        with open('runtime_sessions.json', 'r') as f:
            data = load(f)
            if "days_pushed_to_pixela" not in data:
                self.date_to_log = self.today
                self.sum_day_time(self.date_to_log)
                self.upload()
            else:
                last_day_logged = int(data["days_pushed_to_pixela"][-1])
                time_from_last_upload = int(self.today) - last_day_logged
                if time_from_last_upload > 1:
                    for i in range(1, time_from_last_upload + 1):
                        if str(last_day_logged + i) not in data:
                            pass
                        else:
                            self.dates_to_upload.append(str(last_day_logged + i))

                    self.date_to_log = self.dates_to_upload[0]
                    for i in self.dates_to_upload:
                        self.sum_day_time(i)
                    self.upload()
                else:
                    if self.today not in data["days_pushed_to_pixela"]:
                        self.date_to_log = self.today
                        self.sum_day_time(self.date_to_log)
                        self.upload()
                    else:
                        windll.user32.MessageBoxW(None, "Already Submitted Today.", "yee", 64)
