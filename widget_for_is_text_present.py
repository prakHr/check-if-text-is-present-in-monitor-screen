import PySimpleGUI as sg
from advanced_automation_utilities import Screen, ScreenInfo
import math

def check(is_text_present,final_text):
    rv = False
    if is_text_present in final_text:
        rv = True
    return rv

def get_text_from_monitor_screen(block_width, block_height, is_text_present):
    left, top, right, bottom = ScreenInfo().work_area

    monitor_screen_width = right - left
    monitor_screen_height = bottom - top

    total_columns = math.ceil(monitor_screen_width / block_width)
    total_rows = math.ceil(monitor_screen_height / block_height)

    screen = Screen()
    blocks = []
    merged_rows = []

    for row in range(total_rows):
        row_texts = []

        for col in range(total_columns):
            block_left = left + col * block_width
            block_top = top + row * block_height

            block_right = min(
                block_left + block_width, right
            )
            block_bottom = min(
                block_top + block_height, bottom
            )

            text = screen.read_text(
                region=(
                    block_left,
                    block_top,
                    block_right,
                    block_bottom
                ),
                monitor_index=0
            )

            text = str(text).strip() if text else ""

            blocks.append({
                "row": row,
                "column": col,
                "region": (
                    block_left,
                    block_top,
                    block_right,
                    block_bottom
                ),
                "text": text
            })

            if text:
                row_texts.append(text)

        merged_row = "".join(row_texts)

        if merged_row:
            merged_rows.append(merged_row)

    final_text = "".join(merged_rows)
    is_text_present = check(is_text_present,final_text)
    return {
        "work_area": (left, top, right, bottom),
        "monitor_screen_width": monitor_screen_width,
        "monitor_screen_height": monitor_screen_height,
        "is_text_present": is_text_present
    }


def is_a_single_letter_or_not(text):
    SPACE = " "
    text_array = text.split(SPACE)
    if len(text_array)==1:
        text = text_array[0]
        text = text.lower()
        if len(text)==0:
            return False
        for i in range(len(text)):
            if 'a'<= text[i]<='z':
                continue
            return False
        return True
    return False

layout = [
    [sg.Text("Search for your text on screen?")],
    [sg.Input(key='-INPUT-')],
    [sg.Text(size=(100,1), key='-OUTPUT-')],
    [sg.Button('Ok'), sg.Button('Quit')]
]

window = sg.Window('search any single letter word, try words only outside the widget if you want to try inside try it atleast 2 times!', layout)
block_width, block_height = 1000, 1000
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    is_text_present = values['-INPUT-']
    is_a_single_letter_or_not_check = is_a_single_letter_or_not(is_text_present)
    if is_a_single_letter_or_not_check==True:
        results = get_text_from_monitor_screen(block_width, block_height, is_text_present)
        rv = results["is_text_present"]
        if rv==True:
            rv = "is found"
        else:
            rv = "is not found"
        window['-OUTPUT-'].update(f"{is_text_present} {rv}")
    else:
        window['-OUTPUT-'].update(f"not a single letter word")

window.close()
