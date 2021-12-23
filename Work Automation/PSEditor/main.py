import PySimpleGUI as sg
from configparser import ConfigParser
import os
import pprint


def ini_to_dict(file):
    with open(file) as f:
        file_contents = '[DEFAULT]\n' + f.read().replace('%', '%%')
    file_dict = {}
    config = ConfigParser()
    config.read_string(file_contents)
    contents_list = config.items('DEFAULT')
    for item in contents_list:
        file_dict[item[0]] = item[1]
    return file_dict


def get_table_headers(data):
    return list(data.keys())


def get_table_data(data):
    return list(data.values())


def load_all_settings(path):
    settings = {}
    for filename in os.listdir(path):
        if filename.endswith(".ini"):
            settings[filename] = ini_to_dict(os.path.join(path, filename))
    return settings

def format_for_table(data):
    lst = []
    for i in range(0, len(data)):
        pass



def num_of_rows(data):
    stuff = []
    for i in data.keys():
        stuff.append(len(data[i]))
    return max(stuff)


path_to_ini = './data/'
data_dict = load_all_settings(path_to_ini)
pprint.pprint(data_dict)
print(len(data_dict))


# print(test)


# ------ Window Layout ------
# layout = [[sg.Table(values=[get_table_data(data)], headings=get_table_headers(data), max_col_width=10,
#                     auto_size_columns=False,
#                     display_row_numbers=False,
#                     justification='right',
#                     num_rows=20,
#                     alternating_row_color='lightyellow',
#                     vertical_scroll_only=False,
#                     key='-TABLE-',
#                     selected_row_colors='red on yellow',
#                     enable_events=True,
#                     expand_x=False,
#                     expand_y=True,
#                     enable_click_events=True,           # Comment out to not enable header and other clicks
#                     tooltip='This is a table')],
#           [sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
#           [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')],
#           [sg.Text('Read = read which rows are selected')],
#           [sg.Text('Double = double the amount of data in the table')],
#           [sg.Text('Change Colors = Changes the colors of rows 8 and 9'), sg.Sizegrip()]]
#
# # ------ Create Window ------
# window = sg.Window('The Table Element', layout, size=(600,600),
#                    ttk_theme='clam',
#                    resizable=True)
#
# # ------ Event Loop ------
# while True:
#     event, values = window.read()
#     print(event, values)
#     if event == sg.WIN_CLOSED:
#         break
#     elif event == 'Change Colors':
#         window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))
#     if isinstance(event, tuple):
#         # TABLE CLICKED Event has value in format ('-TABLE=', '+CLICKED+', (row,col))
#         if event[0] == '-TABLE-':
#             if event[2][0] == -1 and event[2][1] != -1:           # Header was clicked and wasn't the "row" column
#                 col_num_clicked = event[2][1]
#             window['-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')
# window.close()
#
#
