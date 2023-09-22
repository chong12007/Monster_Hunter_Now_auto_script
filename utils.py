import webbrowser

import PySimpleGUI as sg
import pyautogui
import time
import pygetwindow as gw
import PySimpleGUI as sg
from pygetwindow import Win32Window
import ctypes
import pyautogui
import cv2

pyautogui.FAILSAFE = False


def detect_app():
    app_titles = ["Vysor"]

    # Find the window with a matching title
    app_window = None
    # Test all title
    for title in app_titles:
        try:
            app_window = gw.getWindowsWithTitle(title)[0]
            break
        except IndexError:
            pass

    if app_window:
        return True, app_window
    else:
        return False, None


def adjust_screen(window):
    app_found, app_window = detect_app()

    if app_found:
        # Resize the window
        app_window.resizeTo(400, 1025)

        # Get Screen Center
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        window_width = app_window.width
        window_height = app_window.height

        screen_center_x = (screen_width - window_width) // 2
        screen_center_y = (screen_height - window_height) // 2

        app_window.activate()

        # Select app
        time.sleep(1)
        # Move the window to the center of the screen
        app_window.moveTo(screen_center_x, screen_center_y)

        window["row1"].update("Screen Adjusted!!", text_color="#509296", font=("Helvetica", 16, "bold"),
                              background_color="#f0f0f0")
        window["row2"].update("yay d >w< b yay", text_color="#509296", font=("Helvetica", 12, "bold"),
                              background_color="#f0f0f0")
        window.refresh()

    else:
        app_not_found(window)


def app_not_found(window):
    window["row1"].update("Error :(", text_color="red", font=("Helvetica", 16, "bold"), background_color="#f0f0f0")
    window["row2"].update("Unable to detect Phone", text_color="red", font=("Helvetica", 12, "bold"),
                          background_color="#f0f0f0")
    update_gui_msg("Supported Emulator :\nVysor(Tested)\n\n", window)
    window.refresh()
    pass


msg_history = ''


def update_gui_msg(msg, window):
    global msg_history

    msg_history += msg
    window.Element('_Multiline_').Update(msg_history, font=("Helvetica", 10, "bold"))
    window.refresh()


def click(coordinate, msg, window):
    update_gui_msg(msg, window)
    window.refresh()
    pyautogui.click(coordinate[0], coordinate[1], button="left")
    time.sleep(1)


def get_icon_coordinate_fullscreen(icon_path):
    screenshot = pyautogui.screenshot()
    screenshot.save("img/screenshot.png")
    screenshot_path = "img/screenshot.png"
    screenshot = cv2.imread(screenshot_path)

    # Load template image
    template = cv2.imread(icon_path)
    # Perform template matching on the ROI
    result = cv2.matchTemplate(screenshot, template, cv2.TM_SQDIFF_NORMED)

    # Get the matched location within the ROI
    # Set a threshold for the match
    threshold = 0.1

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val < threshold:
        top_left = (min_loc[0], min_loc[1])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        click_coordinate = (center[0], center[1])
        return click_coordinate
    else:
        return 0, 0
