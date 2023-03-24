import os
from time import sleep
import subprocess
import pyautogui
import pydirectinput
from entities.match_data import MatchData


class RecordVideo:
    def __init__(self, match_data: MatchData) -> None:
        self.__video_file_dir = os.path.abspath(r'.\media\Videos')
        self.__replay_file_dir = os.path.abspath(r'.\media\replays')
        self.__match_data = match_data

    def record(self):
        # self.__show_mouse_position()
        print('Starting recording of the match...')
        self.__run_game()
        self.__run_obs()
        sleep(50)
        # select champion
        self.__select_player()
        
        sleep(2)
        pydirectinput.keyDown('c')
        pydirectinput.keyUp('c')
        sleep(1)
        pydirectinput.keyDown('n')
        pydirectinput.keyUp('n')
        sleep(1)
        pydirectinput.keyDown('o')
        pydirectinput.keyUp('o')
        sleep(1)
        pydirectinput.keyDown('u')
        pydirectinput.keyUp('u')
        sleep(5)
        # zoom out
        # Press and hold Ctrl+Shift+Z
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('z')

        # Move mouse pointer down 5 times
        for i in range(5):
            pydirectinput.moveRel(0, 50)

        # Release all keys
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyUp('shift')
        pydirectinput.keyUp('z')
        # zoom out end
        
        
        self.__start_stop_recording()
        sleep(self.__duration_in_seconds())
        self.__start_stop_recording()
        sleep(10)
        # pydirectinput.click(962, 641)
        # pyautogui.click(962, 641)
        pyautogui.hotkey('alt', 'f4')
        sleep(1)
        # pydirectinput.leftClick(962, 641)
        # pyautogui.click(962, 641)
        pyautogui.hotkey('alt', 'f4')
        sleep(5)
        print('Recorded match')
        return self.select_video_file()

    def __run_game(self):
        file = os.listdir(self.__replay_file_dir)[0]
        subprocess.run(["start", "cmd", "/c", f"{self.__replay_file_dir}\{file}"], shell=True)

    def __run_obs(self):
        pyautogui.hotkey('super', '1')

    def __select_player(self):
        if self.__match_data['team1']['result'] == 'Victory':
            pydirectinput.keyDown('f1')
            pydirectinput.keyUp('f1')
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            pydirectinput.keyDown('f2')
            pydirectinput.keyUp('f2')
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])

    def __start_stop_recording(self):
        pyautogui.keyDown('shiftleft')
        pyautogui.keyDown('x')
        pyautogui.keyUp('shiftleft')
        pyautogui.keyUp('x')

    def __duration_in_seconds(self) -> int:
        array = self.__match_data['duration'].split(':')
        return (int(array[0]) * 60) + int(array[1]) - 15

    def __show_mouse_position(self):
        while True:
            print(pyautogui.position())
            sleep(1)

    def select_video_file(self):
        files = os.listdir(self.__video_file_dir)
        print(files)
        
        file_path = os.path.abspath(os.path.join(self.__video_file_dir, files[0]))
        return file_path

    def remove_video_file(self):
        file = os.listdir(self.__video_file_dir)
        os.rename(os.path.join(self.__video_file_dir, file[0]), os.path.join(
            os.path.dirname(self.__video_file_dir), 'uploaded', file[0]))
