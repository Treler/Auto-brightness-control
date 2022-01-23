import os
import pygame
import platform
from gtts import gTTS
from time import sleep
from datetime import datetime
from screen_brightness_control import get_brightness, set_brightness


your_name = "Alexander"  # your name (nickname) for voice assistant
time_check = 3600  # time (in secs) after script will check your current brightness and change it if necessary
max_brightness = 60  # max value brightness (in percents)
min_brightness = 30  # min value brightness (in percents)


# function for starting music file
def start_music(filename):
    try:
        pygame.init()
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.2)
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(60)

    except Exception:
        StartMusicError()


# find necessary path for store files (folder "Temp" mostly)
def get_path():
    try:
        path_to_temp = ""
        system_name = platform.system()
        main_disk = os.environ['HOMEDRIVE']

        if system_name == "Windows":
            path_to_temp = f"{main_disk}\\Users\\{os.getlogin()}\\AppData\\Local\\Temp\\"

        if system_name == "Linux":
            path_to_temp = "/tmp/"

        if system_name == "Darwin":
            path_to_temp = "/Library/Caches/TemporaryItems/"

        return path_to_temp

    except Exception:
        GetPathError()


# creating mp3 file with message about changes
def create_mp3(name_mp3, change, value, name, path_to_temp):
    try:
        obj = gTTS(f"{name}, {change} brightness to {value}", lang="en", slow=False)
        obj.save(f"{path_to_temp}" + name_mp3)

    except Exception:
        CreateMP3Error()


sleep(60)  # time for the system initializing after you switch on your computer

# main cycle
while True:
    path = get_path()
    hour_now = datetime.now().hour
    brightness_now = get_brightness()

    if hour_now in range(21, 24) or hour_now in range(0, 9):

        if brightness_now != min_brightness:
            create_mp3("decrease.mp3", "decrease", f"{str(min_brightness)}", your_name, path)
            set_brightness(min_brightness)
            start_music(f"{path}" + "decrease.mp3")

    if hour_now in range(9, 21):

        if brightness_now != max_brightness:
            create_mp3("increase.mp3", "increase", f"{str(max_brightness)}", your_name, path)
            set_brightness(max_brightness)
            start_music(f"{path}" + "increase.mp3")


class GetPathError(Exception):
    def __init__(self):
        print("Get path error")


class CreateMP3Error(Exception):
    def __init__(self):
        print("Create MP3 error")


class StartMusicError(Exception):
    def __init__(self):
        print("Start music error")
