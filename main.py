import time
import webbrowser

import PySimpleGUI as sg
import pyautogui
import utils




def display_ui():
    # Set a Layout
    layout = [
        [sg.Text("Stay on the Page then activate", key="row1", text_color="#509296", font=("Helvetica", 14, "bold"),
                 background_color="#f0f0f0")],
        [sg.Text("Please Adjust the screen before using", key="row2", text_color="#509296",
                 font=("Helvetica", 12, "bold"), background_color="#f0f0f0")],
        [],
        [sg.Multiline('', key='_Multiline_', size=(48, 7), autoscroll=True)],
        [sg.Button("Adjust Screen", key="adjust_screen", button_color="#509296")],
        [sg.Button("Start", key="start", button_color="#509296")],
        [sg.Text("Please leave a star on my github if this script helps you T^T,Click me to github", key="github",
                 enable_events=True, text_color='blue', background_color="#f0f0f0")]
    ]

    # window setting
    window_location = (0, 200)  # Specify the desired coordinates of the window
    window_size = (400, 350)  # Width, Height
    theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(theme)

    window = sg.Window("MHN", layout, location=window_location, keep_on_top=True, size=window_size)

    # Main content
    ui_content(window)

    window.close()



def farm_mob(window) :
    app_found, app_window = utils.detect_app()
    if app_found:
        farm_mob_routine(window)
    else:
        utils.app_not_found(window)

def farm_mob_routine(window) :
    count = 0

    window["row1"].update(f"Mob killed : {count}", text_color="#509296", font=("Helvetica", 16, "bold"),
                          background_color="#f0f0f0")
    window["row2"].update("Click the exit on top right to stop", text_color="#509296", font=("Helvetica", 10, "bold"),
                          background_color="#f0f0f0")
    window.refresh()

    Mob_found = True
    i = 0
    # monster png
    icon_To_detect = 5
    # # Keep loop momotalk until quit program
    while True:
        while Mob_found:

            i += 1
            if i > icon_To_detect:
                utils.update_gui_msg("Sleep 100 seconds\n",window)
                time.sleep(100)
                i = 0
                continue

            icon_path = f"img/monster{i}.png"
            coordinate = utils.get_icon_coordinate_fullscreen(icon_path)
            if coordinate[0] != 0 and coordinate[1] <= 600:
                # Mob found
                slay_mob(coordinate, window)
                count += 1
                window["row1"].update(f"Mob killed : {count}", text_color="#509296",
                                      font=("Helvetica", 16, "bold"),
                                      background_color="#f0f0f0")
                window.refresh()

                time.sleep(10)

            icon_path = f"img/material{i}.png"
            coordinate = utils.get_icon_coordinate_fullscreen(icon_path)
            if coordinate[0] != 0 and coordinate[1] <= 600:
                pass





def find_mob(window) :
    pass

def find_material(window) :
    pass

def slay_mob(coordinate,window) :
    utils.click(coordinate,"Mob Found\n",window)

    for i in range(4) :
        pyautogui.doubleClick(coordinate[0], coordinate[1], button="left")
        time.sleep(0.5)




def ui_content(window):

    while True:
        event, values = window.read()
        # if click momotalk
        if event == "start":
           farm_mob(window)


        # if click reset
        if event == "adjust_screen":
            window["row1"].update("Adjust Screen...")
            window.refresh()
            utils.adjust_screen(window)
            pass

        if event == "github":
            webbrowser.open("https://github.com/chong12007/Blue_Archieve_JP.git")

        # Close app
        if event is None or event == sg.WINDOW_CLOSED:
            break


if __name__ == '__main__':
    display_ui()

