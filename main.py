import time
import webbrowser
import PySimpleGUI as sg
import pyautogui
import utils
import ctypes


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
    # Get the screen width and height

    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)

    window_width = screen_width - 430
    window_height = 30

    window_location = (window_width, window_height)  # Specify the desired coordinates of the window
    window_size = (400, 350)  # Width, Height
    theme = "SystemDefaultForReal"  # Replace with the desired theme name
    sg.theme(theme)

    window = sg.Window("MHN", layout, location=window_location, keep_on_top=True, size=window_size)

    def ui_content(window):
        # Infinite Looping
        while True:
            event, values = window.read()
            # if click start
            if event == "start":
                start_farm(window)

            # if click adjust screen
            if event == "adjust_screen":
                window["row1"].update("Adjust Screen...")
                window.refresh()
                utils.adjust_screen(window)
                pass

            if event == "github":
                webbrowser.open("https://github.com/chong12007/Monster_Hunter_Now_auto_script")

            # Close app
            if event is None or event == sg.WINDOW_CLOSED:
                break

    # Main content
    ui_content(window)

    window.close()


def farm_routine(window):
    window["row1"].update(f"Mob Slayed : 0", text_color="#509296", font=("Helvetica", 16, "bold"),
                          background_color="#f0f0f0")
    window["row2"].update(f"Material Collected : 0", text_color="#509296",
                          font=("Helvetica", 16, "bold"),
                          background_color="#f0f0f0")
    window.refresh()

    try:
        i = 0
        error_occur_count = 0
        icon_to_detect = 3
        mob_count = 0
        material_count = 0

        def find_mob(i, window):
            icon_path = f"img/monster{i}.png"
            coordinate = utils.get_icon_coordinate_fullscreen(icon_path)
            if coordinate[0] != 0 and coordinate[1] <= 600 and coordinate[1] >= 400:
                # Mob found
                utils.click(coordinate, "Mob Found\n", window)
                for i in range(8):
                    pyautogui.doubleClick(coordinate[0], coordinate[1], button="left")
                    time.sleep(0.8)
                time.sleep(5)
                return True

        def find_material(i, window):
            icon_path = f"img/material{i}.png"
            coordinate = utils.get_icon_coordinate_fullscreen(icon_path)
            if coordinate[0] != 0 and coordinate[1] <= 600 and coordinate[1] >= 400:
                # Material found
                utils.click(coordinate, "Material Found\n", window)
                for j in range(3):
                    pyautogui.doubleClick(coordinate)
                    time.sleep(0.5)
                time.sleep(5)
                return True

        # Keep loop find monster and material until quit program
        while True:
            i += 1
            if i > icon_to_detect:
                coordinate = utils.get_icon_coordinate_fullscreen("img/go_back_icon.png")
                if 600 < coordinate[1] < 950:
                    utils.click(coordinate, "Escape from big mob...\n", window)
                    time.sleep(5)

                utils.update_gui_msg("Sleep 200 seconds\n", window)
                time.sleep(200)
                i = 0
                continue

            mob_found = find_mob(i, window)
            if mob_found:
                mob_count += 1
                window["row1"].update(f"Mob killed : {mob_count}", text_color="#509296",
                                      font=("Helvetica", 16, "bold"),
                                      background_color="#f0f0f0")
                window.refresh()
                i = 0

            material_found = find_material(i, window)
            if material_found:
                material_count += 1
                window["row2"].update(f"Material Collected : {material_count}", text_color="#509296",
                                      font=("Helvetica", 16, "bold"),
                                      background_color="#f0f0f0")
                window.refresh()
                i = 0



    except Exception as e:
        print(e)
        # try:
        #     print(e)
        #     utils.update_gui_msg("Eror occur:Not staying at main screen\n", window)
        #     coordinate = utils.get_icon_coordinate_fullscreen("img/go_back_icon.png")
        #     if 600 < coordinate[1] < 950:
        #         utils.click(coordinate, "Escape from big mob...\n", window)
        #         time.sleep(5)
        # except Exception:
        #     pass


def start_farm(window):
    app_found, app_window = utils.detect_app()
    if app_found is False:
        utils.app_not_found(window)

    farm_routine(window)


if __name__ == '__main__':
    display_ui()