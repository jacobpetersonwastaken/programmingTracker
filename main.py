from Arduino import Arduino
from json import load, dump
from time import strftime
from datetime import datetime
from time import sleep
from psutil import process_iter
from threading import Thread
from dotenv import load_dotenv
from os import getenv, rename
from PlayVideo import PlayVideo

load_dotenv('.env')
refresh_rate_seconds = 10
trackPrograms = ["pycharm64.exe", "Code.exe", "studio64.exe", "idea64.exe", "atom.exe", "Unity.exe", "javaw.exe"]


def log_session(session_date, session_name: str, start_time, end_time, session_in_hours: float):
    """Takes each session and writes it to our file and organizes by date. If date doesnt exist then
    we create it. For multi day sessions the date is logged under the starting days date."""

    def save():
        with open('runtime_sessions.json', 'r') as f:
            data = load(f)
        try:
            """writes data to temp holding file. Then after 10 seconds writes to the main file."""
            with open('temp_save.json', 'w') as temp:
                if session_date in data:
                    """Adds to date if it exists"""
                    if session_name in data[session_date]:
                        hour_session_exist = [(i, v["start_time"]) for i, v in enumerate(data[session_date][session_name])
                                              if start_time == v["start_time"]]
                        if len(hour_session_exist) == 0:
                            data[session_date][session_name].append({"start_time": start_time,
                                                                     "end_time": end_time,
                                                                     "session_in_hours": [session_in_hours]})
                        else:
                            data[session_date][session_name][hour_session_exist[0][0]]["session_in_hours"].append(
                                session_in_hours)
                    else:
                        data[session_date][session_name] = [{"start_time": start_time,
                                                             "end_time": end_time,
                                                             "session_in_hours": [session_in_hours]}]
                else:
                    data[session_date] = {session_name: [{"start_time": start_time,
                                                          "end_time": end_time,
                                                          "session_in_hours": [session_in_hours]}]}
                dump(data, temp)
                sleep(10)
                with open("runtime_sessions.json", "w") as file:
                    dump(data, file)
        except:
            pass

    current_time = int(datetime.now().strftime('%H'))
    if 0 <= current_time <= 4:
        session_date = str(int(session_date) - 1)
        save()
    else:
        save()


def program_runtime():

    class ProgramRuntime:
        creation_time = 0
        session_date = strftime('%Y%m%d')
        time_elapsed = 0

        def get_program_runtime(self, name: str):
            """Checks all of the running apps. If the program were looking for (name) is there adds it to a list.
            we then call log session to write to our file.
            """
            running_apps = [i for i in process_iter(['name']) if name in i.info['name']]
            if len(running_apps) > 0:
                try:
                    if self.creation_time == 0:
                        self.creation_time = running_apps[0].as_dict()['create_time']
                except:
                    pass
            elif self.creation_time > 0 and len(running_apps) == 0:
                exit_time = datetime.now().timestamp()
                self.time_elapsed = round(exit_time - self.creation_time, 2)
                time_in_hour = round(((self.time_elapsed / 60) / 60), 4)

                start_hour_24 = datetime.fromtimestamp(self.creation_time).hour
                end_hour_24 = datetime.fromtimestamp(exit_time).hour

                """If its within 0 to 4am it will add the date as the day before. Because who the fuck
                 gets up and codes that early."""

                log_session(session_date=self.session_date, session_name=name, start_time=start_hour_24,
                            end_time=end_hour_24, session_in_hours=time_in_hour)

                pl = PlayVideo()

                media_path = getenv('MEDIA_4_FILE_PATH')
                pl.play_video(fr"{media_path}", 3.5)
                self.creation_time = 0

    thread_obj = [ProgramRuntime() for _ in range(0, 7)]
    while True:
        sleep(refresh_rate_seconds)
        for i, v in enumerate(trackPrograms):
            t1 = Thread(target=thread_obj[i].get_program_runtime, args=(v,))
            t1.start()
            t1.join()


def start():
    """Runs everything. If the current time is between 12am and 3am we check if the date has been added. If not
    we push the days total to pixela"""
    arduino_c = Arduino()
    Thread(target=arduino_c.run_arduino, args=()).start()
    Thread(target=program_runtime, args=()).start()


start()
