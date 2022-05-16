from subprocess import Popen
from time import sleep

from psutil import Process, NoSuchProcess


class PlayVideo:
    def play_video(self, path: str, clip_length):
        try:
            video = Popen([path], shell=True)
            tell = video.pid
            sleep(clip_length)
            parent = Process(tell)
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
        except ProcessLookupError:
            pass
        except NoSuchProcess:
            pass
