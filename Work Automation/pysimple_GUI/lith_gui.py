import PySimpleGUI as sg
import os
import io
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser
from PIL import Image


class Lithophane:
    def __init__(self, type, subtype):
        self.driver = None
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
            self.url = config.get(self.subtype, 'nl_url')
        elif self.type == 'wind':
            self.url = config.get(self.subtype, 'window_url')

    def newchromebrowser(self, headless=True, downloadpath=None):
        """ Helper function that creates a new Selenium browser """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        if downloadpath is not None:
            prefs = {}
            # os.makedirs(downloadpath, exist_ok=True)
            prefs["profile.default_content_settings.popups"] = 0
            prefs["download.default_directory"] = downloadpath
            options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def start_browser(self, path):
        self.newchromebrowser(headless=False, downloadpath=path)
        self.driver.get(self.url)

    def clear_fields(self):
        inputs = self.driver.find_elements_by_tag_name('input')
        for item in inputs:
            try:
                item.clear()
            except selenium.common.exceptions.InvalidElementStateException:
                pass

    def dl_wind(self, file, path):
        self.start_browser(path)
        self.clear_fields()
        select = Select(self.driver.find_element_by_id('hole_num'))
        select.select_by_visible_text('No Border')
        # self.driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
        self.driver.find_element_by_name('fileToUpload').send_keys(file)
        self.driver.find_element_by_id('lith_res').send_keys(my_lith.res)
        self.driver.find_element_by_id('base_length').send_keys(my_lith.width)
        self.driver.find_element_by_id('height').send_keys(my_lith.height)
        self.driver.find_element_by_id('max_thickness').send_keys(my_lith.max_thick)
        self.driver.find_element_by_id('min_thickness').send_keys(my_lith.min_thick)
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user_email)
        self.driver.find_element_by_id('x_shift').send_keys('0.5')
        self.driver.find_element_by_id('y_shift').send_keys('0.5')
        self.driver.find_element_by_id('rect_scale').send_keys('1.0')
        download_btn = self.driver.find_element_by_name('submit')
        download_btn.click()

    def dl_nl(self, file, path):
        self.start_browser(path)
        self.clear_fields()
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


file_types = (('JPG IMAGE', '*.jpg'), ('PNG IMAGE', '*.png'))

lith_type_frame_layout = [[sg.Radio('NightLight', "lith_type", default=True, size=(10,1), k='-nightlight-'), sg.Radio('Window Cling', "lith_type", default=False, size=(10,1), k='-window-')]]

sub_type_frame_layout = [[sg.pin(sg.Radio('Small', "size", default=True, key='-small-')), sg.pin(sg.Radio('Medium', "size", default=False, key='-medium-')), sg.pin(sg.Radio('Large', "size", default=False, key='-large-'))],
                         [sg.pin(sg.Radio('Square', "ori", default=True, key='-square-')), sg.pin(sg.Radio('Portrait', "ori", default=False, key='-portrait-')), sg.pin(sg.Radio('Landscape', "ori", default=False, key='-landscape-'))]]

image_preview_frame_layout = [
    [sg.Image(key="-IMAGE-")]
]

file_input_frame_layout = [[sg.Text('File: '), sg.Text('', key='-filename-')],
                           [sg.FileBrowse(file_types=file_types)]]
dl_path_frame_layout = [[sg.Text('Download Path: '), sg.Text('', key='-dl_path-')],
                         [sg.FolderBrowse(initial_folder='c:/users')]]
layout = [[sg.Frame('Lithophane Type', lith_type_frame_layout)],
          [sg.pin(sg.Frame('Size', sub_type_frame_layout, key='sz'))],
          [sg.Frame('', dl_path_frame_layout)],
          [sg.Frame('Load Image', file_input_frame_layout)],
          [sg.Frame('Preview', image_preview_frame_layout, size=(200,200))],

          [sg.Button('Ok'),  sg.Button('Cancel')]]

window = sg.Window('Lithophane Setup', layout)

while True:
    event, values = window.read(timeout=100)
    filename_elem = window['-filename-']
    dl_path_elem = window['-dl_path-']



    if values['-nightlight-'] and values['-square-']:
        base_type = 'nl'
        sub_type = 'square'
    elif values['-nightlight-'] and values['-portrait-']:
        base_type = 'nl'
        sub_type = 'portrait'
    elif values['-nightlight-'] and values['-landscape-']:
        base_type = 'nl'
        sub_type = 'landscape'
    elif values['-window-'] and values['-small-']:
        base_type = 'wind'
        sub_type = 'sm'
    elif values['-window-'] and values['-medium-']:
        base_type = 'wind'
        sub_type = 'med'
    elif values['-window-'] and values['-large-']:
        base_type = 'wind'
        sub_type = 'lrg'

    if event in (sg.WIN_CLOSED, 'Cancel'):
        break

    if values['Browse'] != '':
        fp = os.path.normpath(values['Browse'])
        fn = os.path.basename(fp)
        filename_elem.update(fn)
        if os.path.exists(fp):
            image = Image.open(values["Browse"])
            image.thumbnail((200, 200))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
    if values['Browse0'] != '':
        dl_path = os.path.normpath(values['Browse0'])
        dl_path_elem.update(dl_path)
    if values['-window-']:
        window['-small-'].update(visible=True)
        window['-medium-'].update(visible=True)
        window['-large-'].update(visible=True)
        window['-square-'].update(visible=False)
        window['-portrait-'].update(visible=False)
        window['-landscape-'].update(visible=False)

    if values['-nightlight-']:
        window['-small-'].update(visible=False)
        window['-medium-'].update(visible=False)
        window['-large-'].update(visible=False)
        window['-square-'].update(visible=True)
        window['-portrait-'].update(visible=True)
        window['-landscape-'].update(visible=True)



    if event == 'Ok':
        my_lith = Lithophane(base_type, f'{base_type}_{sub_type}')
        if base_type == 'nl':
            my_lith.dl_nl(fp, dl_path)
        else:
            my_lith.dl_wind(fp, dl_path)

        # break

window.close()
