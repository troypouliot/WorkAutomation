import PySimpleGUI as sg
import os
# from pysimple_GUI.lith import lith_oop

#making some edits





#######################################################

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from configparser import ConfigParser
from os import getcwd






class Lithophane():
    def __init__(self, type, subtype):
        self.p = {"download.default_directory": "C:\\Users\\troypouliot\\test", "safebrowsing.enabled":"false"}
        self.op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.op)
        self.op.add_experimental_option('prefs', self.p)
        config = ConfigParser()
        config.read('config.ini')
        self.type = type
        self.subtype = subtype
        self.res = config.get(self.subtype, 'res')
        self.width = config.get(self.subtype, 'width')
        self.height = config.get(self.subtype, 'height')
        self.max_thick = config.get(self.subtype, 'max_thick')
        self.min_thick = config.get(self.subtype, 'min_thick')
        self.user_email = config.get(self.subtype, 'user')
        self.frame_width = config.get(self.subtype, 'frame_width')
        self.slot_width = config.get(self.subtype, 'slot_width')
        self.slot_depth = config.get(self.subtype, 'slot_depth')
        self.adapt_thick = config.get(self.subtype, 'adapt_thick')
        self.light_to_lith_dis = config.get(self.subtype, 'light_to_lith_dis')
        self.radius = config.get(self.subtype, 'radius')
        if self.type == 'nl':
            self.url = 'https://lithophanemaker.com/Night%20Light%20Lithophane.html'
        elif self.type == 'wind':
            self.url = 'https://lithophanemaker.com/Framed%20Lithophane.html'


    def start_browser(self):
        self.driver.get(self.url)

    def clear_fields(self):
        inputs = self.driver.find_elements_by_tag_name('input')
        for item in inputs:
            try:
                item.clear()
            except selenium.common.exceptions.InvalidElementStateException:
                pass

    def dl_wind(self):
        self.start_browser()
        self.clear_fields()
        select = Select(self.driver.find_element_by_id('hole_num'))
        select.select_by_visible_text('No Border')
        self.driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
        self.driver.find_element_by_id('lith_res').send_keys(my_lith.res)
        self.driver.find_element_by_id('base_length').send_keys(my_lith.width)
        self.driver.find_element_by_id('height').send_keys(my_lith.height)
        self.driver.find_element_by_id('max_thickness').send_keys(my_lith.max_thick)
        self.driver.find_element_by_id('min_thickness').send_keys(my_lith.min_thick)
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user_email)
        download_btn = self.driver.find_element_by_name('submit')
        download_btn.click()

    def dl_nl(self, file):
        self.start_browser()
        self.clear_fields()
        # self.driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
        self.driver.find_element_by_name('fileToUpload').send_keys(file)
        self.driver.find_element_by_id('lith_res').send_keys(my_lith.res)
        self.driver.find_element_by_id('t_max').send_keys(my_lith.max_thick)
        self.driver.find_element_by_id('t_min').send_keys(my_lith.min_thick)
        self.driver.find_element_by_id('frame_width').send_keys(my_lith.frame_width)
        self.driver.find_element_by_id('w_slot').send_keys(my_lith.slot_width)
        self.driver.find_element_by_id('d_slot').send_keys(my_lith.slot_depth)
        self.driver.find_element_by_id('t_base').send_keys(my_lith.adapt_thick)
        self.driver.find_element_by_id('LLS').send_keys(my_lith.light_to_lith_dis)
        self.driver.find_element_by_id('radius').send_keys(my_lith.radius)
        self.driver.find_element_by_id('x_span').send_keys(my_lith.width)
        self.driver.find_element_by_id('z_dim').send_keys(my_lith.height)
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user_email)
        download_btn = self.driver.find_element_by_name('submit')
        self.driver.find_element_by_id('x_shift').send_keys('0.5')
        self.driver.find_element_by_id('y_shift').send_keys('0.5')
        self.driver.find_element_by_id('rect_scale').send_keys('1.0')
        download_btn.click()

template = 'nl'
size = 'square'


###################################################################











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
    print(event, values)
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
        my_lith = Lithophane(template, f'{template}_{size}')
        my_lith.dl_nl(fp)

        break

window.close()