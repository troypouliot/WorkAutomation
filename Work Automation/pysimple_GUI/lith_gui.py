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


sg.theme('DarkGrey5')
file_types = (('JPG IMAGE', '*.jpg'), ('PNG IMAGE', '*.png'))

lith_type_frame_layout = [[sg.Radio('NightLight', "lith_type", default=True, size=(10, 1), k='-nightlight-'),
                           sg.Radio('Window Cling', "lith_type", default=False, size=(10, 1), k='-window-')]]

sub_type_frame_layout = [[sg.pin(sg.Radio('Small', "size", default=True, key='-small-')),
                          sg.pin(sg.Radio('Medium', "size", default=False, key='-medium-')),
                          sg.pin(sg.Radio('Large', "size", default=False, key='-large-'))],
                         [sg.pin(sg.Radio('Square', "ori", default=True, key='-square-')),
                          sg.pin(sg.Radio('Portrait', "ori", default=False, key='-portrait-')),
                          sg.pin(sg.Radio('Landscape', "ori", default=False, key='-landscape-'))]]

image_preview_frame_layout = [
    [sg.Image(key="-IMAGE-")]
]

file_input_frame_layout = [[sg.Text('File: '), sg.Text('', key='-filename-')],
                           [sg.FileBrowse(file_types=file_types, key='-load_img_btn-')]]
dl_path_frame_layout = [[sg.Text('Download Path: '), sg.Text('', key='-dl_path-')],
                        [sg.FolderBrowse(initial_folder='c:/users', key='-dl_path_btn-')]]
layout = [[sg.Frame('Lithophane Type', lith_type_frame_layout, size=(300, 50))],
          [sg.pin(sg.Frame('Size', sub_type_frame_layout, key='sz', size=(300, 50)))],
          [sg.Frame('', dl_path_frame_layout, size=(300, 60))],
          [sg.Frame('Load Image', file_input_frame_layout, size=(300, 75))],
          [sg.Frame('Preview', image_preview_frame_layout, size=(300, 300))],

          [sg.Button('Create File'), sg.Button('Exit')]]

window = sg.Window('Lithophane Setup', layout,
                   icon=b'''iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWX
                        MAAC4jAAAuIwF4pT92AAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAACLNJRE
                        FUaIG9mmtQXOUZx3/nnF32xsKyLASWZUkIkEBMCORijGY0UdNooq2ZjOMt2uro1DrTTNrOaC/j+K
                        FfTO2o4612NGpbbTttGpXYKLkRQ5BcjEBMxIQmXEKAwBJgl93ssntOPxxYwmWB7Hr8zTDDnnef93
                        3+53nf572t8JfnUdCIGiCgVeXjELWq2Mf3JwI0FNKjVcUx0ExIotFQrrHD6xJsLybBOO18vXDkI/
                        APwC0PgTV9ZnaaRSQcp91AD1xohNAV2PUKXPhmZnaaCYk31CMRWH4XZLhh33vw5W5Q5KntNBNijN
                        POYgNBhN6LsOYRKFwKX1fB3ncgOBjbTjMhKXHaiRJYUqGvS/1/5Sa4YSN0NMHHL0N3awy7uD2dhs
                        nGaG8HNB2HM0fUNx4La7o6VkYouh4W3wb+fvjsTThzdKKNZlnLANiBXlSnaj+EjrNjv5MzD1Y/DN
                        I4L6zp0NOm/u9ph7o96qDPyoeAF77YAd0tsOKeUVvNhADkA2cvQOVbYE6BNT9Wnbnig29rwWqfKA
                        LU50NB2Lsd2s9AZh6sfQKy56rZ7NDf1cj2XoTVmyHZPqUQEQtZmMhEjwUJEwIiEUIM4SVAN366kK
                        eYMa6E5nLwgzZS0kOsfRz0wxlAb4Cl62O3nGwftvfB7Y+Cs2i0LMmovpATn6pR6rs0iZAkUnFQho
                        NFWHAhkRS7NQBkvLRxmUa6+ZIAl6IlHoqpOLUYr+d/rHrKgt44RcoZx0gKLlw2VsQIggBL7lD/Rt
                        ABWMnDzQ+wMR/hmsa/iJW8qP0A52hjL+cJUs9jdDXvRBBFHK6fAq8y1XzvuwxyBFIcatcC6O+eqR
                        85iCU8TilbSaPkGkVMJIV8cnmC0/wMBR0IAoosE/SnAY+ipoCJeD2w43lorFE/J5nAYJ6pkBzgSU
                        Q7CxJy/moUoAIIIAGQ4c4DoPlkHTAP+CWQPcHOmg4Gk5qhos/sEPJP12IZsAVITnwe6fF5UYaXqi
                        eBpqvKcouvw2C20LCvklAgAGQCW4HbuDo6igKRsDqQR1i6AdY9GatVO/AT4BEYHscJCbk8OMim11
                        /msXf+TM/gIAfGlSeZTJSvW0/AO8DB999FjkSGG94APDssyM65ryAcAlfxqO2sOZOl5jzgPuC3QO
                        mYEmnL7euei1fI24eq+PTrepo9PeysO4Ex143FljbmO+muXALeAZob6rjUfB5nwTz0RqMqSCnkfH
                        0KNTtOkTnbzvK7FiCIyYAZdW3gBIqBlcAmYDXgYrL3L5x7/qW49+z+UJA7X9yGXtJxKXgFn89L2d
                        o7WXjLrWqOHEaRZer3VdKwvxJBEMiaW4jBZMbT3sZATzdzFpdz46b7kfT6eF1JLCJ6SUexM4ft1Q
                        dZ/qNNDAWDnDlSQ09bK86i+eiS1P6rOl9A3sJSFFnG5/EQ8PbjcLm5YeO9lNx0M6IkxS0CEozICF
                        srdrKnoY67tz7NuRPHOP7fjzGYzKy6bzPZhZPMaBqQUESilcwt4MCJY/R1dVJ+xway8gtoPdXAt0
                        dqUBSFWflzEa7qalowYyH+UBBREBEncahBlAjnuDhasZP0HBfOwnnMLV9G78V2mo7V0t3aQs680a
                        6mBTMSEgqH2fzWG2z7dBcXensxGww4bWnRt1wPBFJtRMJDNOzfQ8HS6zFaLOSXLUGSdJw9fgRb5i
                        zszhzNhMxojGzbvYs/Ve1FJ0k4kq109veRaU3hzkWL2VBaxjfu2TQJApFwmE9e+SNp2U5W3bc5au
                        /19GBNd2gmAmYYkdJcN22XPTR2XKRwVhbP3nUPqWYLn51q4O1DVXx1/Ci+gQFMycnkLSzlWMVO0r
                        KcpGbOAsBgNmsqAq4xa71fe5jfV3yIKUnPH+59kDXzS6hra+H1hjpqT9Yx2NdHakYmsiwTDgb54S
                        +ewWCxaOl/lGvKWotcbtYUL2B/42n+9kU1g6EgG8uX4Z5fgu6mm3EWzScSiXC58yKyHKFg6XKSTC
                        YN3R8lZkQ6+/uRFRnnuCUHwGAwyG92/JOK+hOUuWfz3AMP8580e7RcURSCg4MYk5O183wcMReNbx
                        7cx+92/mvSMovBwMsPPMwL9z5IY8dFHnppG90n66PlgiB8ryJgCiFGnZ6qxtPsOX0ypvHGJcv491
                        NbcCRb2f3+uxzb9eHwCvf7J6aQrWvvoCBzFs99tAN/KPYWtTg7h49//ivWlZYzcKlL8xk8FjEHuy
                        SKzM/O4b3DnxMKR1hVNC9mJUk6HesXluJYVEZngou/eJlyY7VsTj4PrriR7dVVNHZMcTQ4zK2ShF
                        Ge5rRZI6bdIT6z/m7y0h38esc/kKe5fTEDi/r6vyvfrokphQTDQ3h8Ph64fiX1ba28tr+SoWkGc3
                        bAj9h8/jt1ciZEd8X9AT9/rammtbeHVo+H1t4eugYGogcLAC9W7uaD2ho233AT969YSZp54qxt0i
                        chnjoNBiNy9sQTE62ICnn7UBWv7qtEL0nk2tNZ4HSxoTST2Y4M5jgycKXZOdx0hneqD/LCZ5/w6v
                        5KNpYvY8vt68iwjl4imJPU7ar49SkUWUbJ0W7FezXRmf1Ey3kc1hRybGlIYuwepygK1We/ZXv1Qb
                        5qbebzp58l5aplSK/fzxvVh6Of5Tw3SlERisZpOaGtbn/AT6pp7MpWAV48UEVgaGj0odVK5LoSFG
                        u81z/Tk9C51ngRAALgsqWOfej1ItUeRWxsRAiFEmlyIoqC0Nmpzf2IOy2Ns93jfjKgKIitbdDejp
                        ydjeJyoaQkEKGhEGJHF2JLCwQC2ggpycriwNmmyeediIx4oR0utIPJhJKZgWyzoaTawDj5ITeAMD
                        QEXi/CgBehuxuhr2/Mrwo0EZJiNFKQ4eDMpWmO0wMBhJZWpJbhG05RArMJRRRBr4NIBIbCqohpuq
                        RmV29LXLnTCxmPHAGfj3jym2a3unPS7bhsNq2qn4BmQgRBYH1JCeIUc9J3iaatOJItrMhza9lElP
                        8Dj88Aoh1/rs8AAAAASUVORK5CYII=''')


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

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if values['-load_img_btn-'] != '':
        fp = os.path.normpath(values['-load_img_btn-'])
        fn = os.path.basename(fp)
        filename_elem.update(fn)
        if os.path.exists(fp):
            image = Image.open(values["-load_img_btn-"])
            image.thumbnail((300, 300))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
    if values['-dl_path_btn-'] != '':
        dl_path = os.path.normpath(values['-dl_path_btn-'])
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

    if event == 'Create File':
        if values['-dl_path_btn-'] and values['-load_img_btn-'] != '':
            my_lith = Lithophane(base_type, f'{base_type}_{sub_type}')
            if base_type == 'nl':
                my_lith.dl_nl(fp, dl_path)
            else:
                my_lith.dl_wind(fp, dl_path)
        else:
            sg.PopupOK(' Make sure all fields are filled in                ', title='Empty Fields')

        # break

window.close()
