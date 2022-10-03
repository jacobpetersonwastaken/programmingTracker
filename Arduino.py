from time import sleep
from serial import Serial
from threading import Thread
from PlayVideo import PlayVideo
from SessionBrain import SessionBrain
from dotenv import load_dotenv
from os import getenv


class Arduino:
    arduino = Serial('COM8', 115200)
    arduino.timeout = 1
    counter = 0
    upload_limit = 1
    its_working_limit = 0
    upload = False

    def its_working_tracker(self):
        sleep(10)
        if self.counter <= self.its_working_limit:
            self.counter = 0

    def upload_tracker(self):
        sleep(10)
        if self.counter <= self.upload_limit:
            self.counter = 0

    def pixela_upload(self):
        if self.counter == 0:
            Thread(target=self.upload_tracker, args=()).start()
        self.counter += 1
        if self.counter > self.upload_limit:
            self.upload = True
            self.counter = 0
            sesh_brain = SessionBrain()
            sesh_brain.session_upload()
            sleep(3)
        self.arduino.write("o".encode())
        self.upload = False

    def it_works(self):
        if self.counter == 0:
            Thread(target=self.its_working_tracker, args=()).start()
        self.counter += 1

        if self.counter >= self.its_working_limit:
            pl = PlayVideo()
            load_dotenv('.env')
            file_path = getenv('MEDIA_1_FILE_PATH')
            pl.play_video(fr"{file_path}", 5)
            self.counter = 0
        self.arduino.write("o".encode())
        sleep(0.3)

    def run_arduino(self):
        while True:
            on = self.arduino.readline().decode('utf-8')
            if on == "w":
                self.it_works()
            elif on == "u":
                self.pixela_upload()
