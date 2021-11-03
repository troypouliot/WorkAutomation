import PySimpleGUI as sg
import os
from pysimple_GUI.lith import lith_oop


file_types = (('JPG IMAGE', '*.jpg'), ('PNG IMAGE', '*.png'))
lith_type_frame_layout = [[sg.Radio('NightLight', "lith_type", default=True, size=(10,1), k='-R1-'), sg.Radio('Window Cling', "lith_type", default=False, size=(10,1), k='-R2-')]]
size_frame_layout = [[sg.pin(sg.Radio('Small', "size", default=True, key='-small-')), sg.pin(sg.Radio('Medium', "size", default=False, key='-medium-')), sg.pin(sg.Radio('Large', "size", default=False, key='-large-'))],
                     [sg.pin(sg.Radio('Square', "ori", default=True, key='-square-')), sg.pin(sg.Radio('Portrait', "ori", default=False, key='-portrait-')), sg.pin(sg.Radio('Landscape', "ori", default=False, key='-landscape-'))]]

load_img_frame_layout = [[sg.Text('File: '), sg.Text('', key='-filename-')],
                         [sg.FileBrowse(file_types=file_types)]]
layout = [[sg.Frame('Lithophane Type', lith_type_frame_layout)],
          [sg.pin(sg.Frame('Size', size_frame_layout, key='sz'))],
          [sg.Frame('Load Image', load_img_frame_layout)],
          [sg.Button('Ok'),  sg.Button('Cancel')]]

window = sg.Window('Lithophane Setup', layout)

while True:
    event, values = window.read(timeout=100)
    filename_elem = window['-filename-']
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break


    if values['Browse'] != '':
        fp = os.path.normpath(values['Browse'])
        fn = os.path.basename(fp)
        filename_elem.update(fn)
    if values['-R2-']:
        window['-small-'].update(visible=True)
        window['-medium-'].update(visible=True)
        window['-large-'].update(visible=True)
        window['-square-'].update(visible=False)
        window['-portrait-'].update(visible=False)
        window['-landscape-'].update(visible=False)

    if values['-R1-']:
        window['-small-'].update(visible=False)
        window['-medium-'].update(visible=False)
        window['-large-'].update(visible=False)
        window['-square-'].update(visible=True)
        window['-portrait-'].update(visible=True)
        window['-landscape-'].update(visible=True)

    if event == 'Ok':
        lith_oop.my_lith.dl_nl()
        break

window.close()