import subprocess
import pyautogui
from hand_movement.metadata import Position

pyautogui.FAILSAFE = False


class Controller:

    __launchpad_state = False

    _speed = 500

    def setSpeed(self, speed: int):
        self._speed = speed/1000

    def __init__(self, speed: int = 500) -> None:
        self._speed = 500

    def moveCursor(self, movement: Position):
        x, y = pyautogui.position()
        pyautogui.moveTo(x + movement.x, y + movement.y)

    def click(self):
        pyautogui.click()

    def getLaunchpadState(self):
        return self.__launchpad_state

    def open_launchpad(self):
        output = subprocess.check_output(["open",  "-a", "Launchpad"])
        print(output)
        self.__launchpad_state = True
        return self.__launchpad_state

    def close_launchpad(self):
        if self.__launchpad_state:
            pyautogui.press("esc")
            self.__launchpad_state = False
        return self.__launchpad_state

    def change_launchpad_page(self, direction: str):
        done = False
        if self.__launchpad_state:
            pyautogui.keyDown("command")
            if direction == "left":
                pyautogui.press("left")
                done = True
            elif direction == "right":
                pyautogui.press("right")
                done = True
        return done

    def leftKey(self):
        pyautogui.press("left")
        return True

    def rightKey(self):
        pyautogui.press("right")
        return True

    def downKey(self):
        pyautogui.press("down")
        return True

    def upKey(self):
        pyautogui.press("up")
        return True
