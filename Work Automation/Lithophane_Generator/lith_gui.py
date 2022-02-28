import PySimpleGUI as sg
import os
import io
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from configparser import ConfigParser
from PIL import Image

version = '1.3.1'

class Lithophane:
    def __init__(self, type):
        self.driver = None
        config = ConfigParser()
        config.read(['./config/config.ini', './config.ini'])
        self.type = type
        self.section = 'DEFAULT'
        self.res = config.get(self.section, 'res')
        self.max_thick = config.get(self.section, 'max_thick')
        self.min_thick = config.get(self.section, 'min_thick')
        self.frame_width = config.get(self.section, 'frame_width')
        self.slot_width = config.get(self.section, 'slot_width')
        self.slot_depth = config.get(self.section, 'slot_depth')
        self.adapt_thick = config.get(self.section, 'adapt_thick')
        self.light_to_lith_dis = config.get(self.section, 'light_to_lith_dis')
        self.user = config.get(self.section, 'user')
        self.nl_url = config.get(self.section, 'nl_url')
        self.window_url = config.get(self.section, 'window_url')
        self.nl_sq_rad = config.get(self.section, 'nl_sq_rad')
        self.nl_sq_wid = config.get(self.section, 'nl_sq_wid')
        self.nl_sq_hei = config.get(self.section, 'nl_sq_hei')
        self.nl_sq_gimp = config.get(self.section, 'nl_sq_gimp')
        self.nl_por_rad = config.get(self.section, 'nl_por_rad')
        self.nl_por_wid = config.get(self.section, 'nl_por_wid')
        self.nl_por_hei = config.get(self.section, 'nl_por_hei')
        self.nl_por_gimp = config.get(self.section, 'nl_por_gimp')
        self.nl_lan_rad = config.get(self.section, 'nl_lan_rad')
        self.nl_lan_wid = config.get(self.section, 'nl_lan_wid')
        self.nl_lan_hei = config.get(self.section, 'nl_lan_hei')
        self.nl_lan_gimp = config.get(self.section, 'nl_lan_gimp')
        self.w_sm_frame = config.get(self.section, 'w_sm_frame')
        self.w_sm_wid = config.get(self.section, 'w_sm_wid')
        self.w_sm_hei = config.get(self.section, 'w_sm_hei')
        self.w_med_frame = config.get(self.section, 'w_med_frame')
        self.w_med_wid = config.get(self.section, 'w_med_wid')
        self.w_med_hei = config.get(self.section, 'w_med_hei')
        self.w_lrg_frame = config.get(self.section, 'w_lrg_frame')
        self.w_lrg_wid = config.get(self.section, 'w_lrg_wid')
        self.w_lrg_hei = config.get(self.section, 'w_lrg_hei')
        self.b_frame = config.get(self.section, 'b_frame')
        self.b_frame_width = config.get(self.section, 'b_frame_width')
        self.b_frame_height = config.get(self.section, 'b_frame_height')
        self.b_frame_angle = config.get(self.section, 'b_frame_angle')
        self.b_sm_size = config.get(self.section, 'b_sm_size')

    def newchromebrowser(self, headless=True, downloadpath=None):
        """ Helper function that creates a new Selenium browser """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        if downloadpath is not None:
            prefs = {"profile.default_content_settings.popups": 0, "download.default_directory": downloadpath}
            # os.makedirs(downloadpath, exist_ok=True)
            options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(options=options)
        return self.driver


    def start_browser(self, path, _type):
        try:
            self.newchromebrowser(headless=False, downloadpath=path)
            if _type == 'wind' or _type == 'box':
                self.driver.get(self.window_url)
            else:
                self.driver.get(self.nl_url)
        except selenium.common.exceptions.SessionNotCreatedException as err:
            sg.popup('Something went wrong:' + '\n' * 2 + str(err), title='Error')


    def clear_fields(self):
        inputs = self.driver.find_elements_by_tag_name('input')
        for item in inputs:
            try:
                item.clear()
            except selenium.common.exceptions.InvalidElementStateException:
                pass

    def dl_wind(self, file, path, sub_type):
        _type = 'wind'
        self.start_browser(path, _type)
        self.clear_fields()
        select = Select(self.driver.find_element_by_id('hole_num'))
        select.select_by_visible_text('No Border')
        self.driver.find_element_by_name('fileToUpload').send_keys(file)
        self.driver.find_element_by_id('lith_res').send_keys(my_lith.res)
        self.driver.find_element_by_id('max_thickness').send_keys(my_lith.max_thick)
        self.driver.find_element_by_id('min_thickness').send_keys(my_lith.min_thick)
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user)
        self.driver.find_element_by_id('x_shift').send_keys('0.5')
        self.driver.find_element_by_id('y_shift').send_keys('0.5')
        self.driver.find_element_by_id('rect_scale').send_keys('1.0')
        if sub_type == 'sm':
            self.driver.find_element_by_id('base_length').send_keys(my_lith.w_sm_wid)
            self.driver.find_element_by_id('height').send_keys(my_lith.w_sm_hei)
        elif sub_type == 'med':
            self.driver.find_element_by_id('base_length').send_keys(my_lith.w_med_wid)
            self.driver.find_element_by_id('height').send_keys(my_lith.w_med_hei)
        else:
            self.driver.find_element_by_id('base_length').send_keys(my_lith.w_lrg_wid)
            self.driver.find_element_by_id('height').send_keys(my_lith.w_lrg_hei)
        download_btn = self.driver.find_element_by_name('submit')
        download_btn.click()

    def dl_box(self, file, path, sub_type):
        _type = 'box'
        self.start_browser(path, _type)
        self.clear_fields()
        select = Select(self.driver.find_element_by_id('hole_num'))
        select.select_by_visible_text('Frame Only')
        self.driver.find_element_by_name('fileToUpload').send_keys(file)
        self.driver.find_element_by_id('lith_res').send_keys(my_lith.res)
        self.driver.find_element_by_id('max_thickness').send_keys(my_lith.max_thick)
        self.driver.find_element_by_id('min_thickness').send_keys(my_lith.min_thick)
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user)
        self.driver.find_element_by_id('x_shift').send_keys('0.5')
        self.driver.find_element_by_id('y_shift').send_keys('0.5')
        self.driver.find_element_by_id('rect_scale').send_keys('1.0')
        self.driver.find_element_by_id('base_width').send_keys(my_lith.b_frame_width)
        self.driver.find_element_by_id('base_height').send_keys(my_lith.b_frame_height)
        self.driver.find_element_by_id('ledge_angle').send_keys(my_lith.b_frame_angle)
        if sub_type == 'sm':
            self.driver.find_element_by_id('base_length').send_keys(my_lith.b_sm_size)
            self.driver.find_element_by_id('height').send_keys(my_lith.b_sm_size)
        elif sub_type == 'med':
            self.driver.find_element_by_id('base_length').send_keys(my_lith.w_med_wid)
            self.driver.find_element_by_id('height').send_keys(my_lith.w_med_hei)
        else:
            self.driver.find_element_by_id('base_length').send_keys(my_lith.w_lrg_wid)
            self.driver.find_element_by_id('height').send_keys(my_lith.w_lrg_hei)
        download_btn = self.driver.find_element_by_name('submit')
        download_btn.click()

    def dl_nl(self, file, path, sub_type):
        _type = 'nl'
        self.start_browser(path, _type)
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
        self.driver.find_element_by_id('emailAddress').send_keys(my_lith.user)
        self.driver.find_element_by_id('x_shift').send_keys('0.5')
        self.driver.find_element_by_id('y_shift').send_keys('0.5')
        self.driver.find_element_by_id('rect_scale').send_keys('1.0')
        if sub_type == 'square':
            self.driver.find_element_by_id('radius').send_keys(my_lith.nl_sq_rad)
            self.driver.find_element_by_id('x_span').send_keys(my_lith.nl_sq_wid)
            self.driver.find_element_by_id('z_dim').send_keys(my_lith.nl_sq_hei)
        elif sub_type == 'portrait':
            self.driver.find_element_by_id('radius').send_keys(my_lith.nl_por_rad)
            self.driver.find_element_by_id('x_span').send_keys(my_lith.nl_por_wid)
            self.driver.find_element_by_id('z_dim').send_keys(my_lith.nl_por_hei)
        else:
            self.driver.find_element_by_id('radius').send_keys(my_lith.nl_lan_rad)
            self.driver.find_element_by_id('x_span').send_keys(my_lith.nl_lan_wid)
            self.driver.find_element_by_id('z_dim').send_keys(my_lith.nl_lan_hei)
        download_btn = self.driver.find_element_by_name('submit')
        download_btn.click()


sg.theme('DarkGrey5')
file_types = (('Images', '*.jpg *.jpeg *.png *.bmp'), )


def main_window():
    lith_type_frame_layout = [
        [sg.Radio('NightLight', "lith_type", default=True, size=(10, 1), k='-nightlight-', enable_events=True),
         sg.Radio('Window Cling', "lith_type", default=False, size=(10, 1), k='-wind_cling-', enable_events=True),
         sg.Radio('Box', "lith_type", default=False, size=(10, 1), k='-box-', enable_events=True)]]

    sub_type_frame_layout = [[sg.pin(sg.Radio('Square', "ori", default=True, key='-square-', enable_events=True)),
                              sg.pin(sg.Radio('Portrait', "ori", default=False, key='-portrait-', enable_events=True)),
                              sg.pin(sg.Radio('Landscape', "ori", default=False, key='-landscape-', enable_events=True))],
                             [sg.pin(sg.Radio('Small', "size", default=True, key='-small-', enable_events=True)),
                              sg.pin(sg.Radio('Medium', "size", default=False, key='-medium-', enable_events=True)),
                              sg.pin(sg.Radio('Large', "size", default=False, key='-large-', enable_events=True))],
                             ]

    image_preview_frame_layout = [[sg.Image(key="-IMAGE-")]]

    file_input_frame_layout = [[sg.Text('File: '), sg.Text('', key='-filename-')],
                               [sg.FileBrowse(file_types=file_types, key='-load_img_btn-')]]
    dl_path_frame_layout = [[sg.Text('Download Path: '), sg.Text('', key='-dl_path-')],
                            [sg.FolderBrowse(initial_folder='c:/users', key='-dl_path_btn-')]]
    layout = [[sg.Frame('Lithophane Type', lith_type_frame_layout, size=(300, 50))],
              [sg.pin(sg.Frame('Size', sub_type_frame_layout, key='sz', size=(300, 50)))],
              [sg.Frame('', dl_path_frame_layout, size=(300, 60))],
              [sg.Frame('Load Image', file_input_frame_layout, size=(300, 75))],
              [sg.Frame('Preview', image_preview_frame_layout, size=(300, 300))],

              [sg.Button('Create File'), sg.Button('Exit'), sg.Button('Change Settings', key='-settings_btn-')],
              [sg.Push(), sg.Text('Version: {}'.format(version), justification='right', font='Helvetica 8')]]

    return sg.Window('Lithophane Setup', layout, finalize=True,
                     icon=b'''iVBORw0KGgoAAAANSUhEUgAAAJIAAACrCAYAAACNDsXrAAAACXBIWX
                            MAABbuAAAW7gEac8QCAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAFUJJRE
                            FUeJztnXucHFWVx7+numcmr1EEBAlkzUC6q2dGCUpAIOsqa7IqxsciT1+gKywigvh+sR/0o+7KQ0
                            EeyiqrLrIrrssHXVx5rAQVRCSCBGamq3qSoMEEDESTyOQx3XX2j54hIenqrsftR6r6+/nMJ9NV95
                            46mfnNvbfuPfdcIcmoZhgfP4FKZQkiQ0ABmIOIonofIleQz9/ZbjeTgLTbgaYxOvpiMpkfAgvrlh
                            O5glzuw4h4rXEsmSRTSKVSH573EDAYsManse0vNtOlpGO124Gm4HlnEVxEABdTKg01y500kEwhwX
                            tDlu/B8/6pKZ6khOR1bSMjLyKbXR+hZplyeR7Dw08Y9ykFJK9F6ulZHLFmlkzmNKO+pIjkCUn1pZ
                            Hripxg0JNUkUQh5WLUfiVr1sww5kuKSJ6QRA6NUXsG27YNG/MlRSRPSHBgrNqW9RJDfqSKJArphb
                            Fqq3aFFIFkCWlkpBeYE8uGZUUfrKeYZAmptzf+QFm1O8MdgWQJyfN6DVg5CNWMATupIllCUjUhpC
                            xjYwcYsJMqkiUk6DNiRWSuETspImlCMtEiQTbbFVJIkiUkz+sxYke1K6SQJEtIIma6NtX9jNhJEc
                            kSUjZrpmsTeb4ROykiWUIql83EV6nuY8ROikiWkCxr0pClrpBCkiwhiZgRUrdFCk1XSLXtdIUUkm
                            QJqVIpG7Ej8gIjdlJEsoRkaozU7dpC0xVSbbpCCkmyhLR9uykh9fDww7MN2UoFyRKSuRYJZszotk
                            ohSJaQsllzQrKs7ux2CJIlpNmzzby1AXhevJDdlJEsIa1bZ65FUu0KKQTJEtKiRZNAxZC1fkN2Uk
                            G23Q40gQnMiKArpGkcZ3887yVY1hPYdrFWkSQK6Rm6QjLDyMgcstmrgHdgWVWtOM4GVP+bTOZqcr
                            mR6aLJ6tqqTBixYlnpHiOtXTuTbPZHwJk8t8F5ISLn4Hm/xXU/N73jJolCesaQnXS3SBMT1wHH1y
                            mRRfUiXPdSSKaQzLRIaX5rK5X+DnhnwNIXUCoNJ1FI3RYpDitW9OB514aoYaH6riQKyUyLFDeHwN
                            5Kf//pwGGh6njeK7tC8id9QlIVRD4aup7IQPKEpGqma1NNX9c2Pr4sYlqffZInJJHuGCkqnvePEW
                            taSRSSma5NJF1dm+McDLwuYu2NyROSqqkxUtpapDOAaOl8VNclT0jwF0N20iMkVQHeHbm+yPrkCc
                            lcizQL1eT9fGpRKh0NLIhh4Q/J+0GZG2xbOE464rZVT45Zf3XyhARbjFlKQ5SkqsQWEjyQPCFZ1k
                            aD1pIvpGLxWET+KoYFpa/vweQJqVw2J6SenuQPuDOZuK1RiYGBPydPSCZbpKRHAFS7tbfGsiHyAC
                            QxjKS392mD1p5n0FbnMT5+DDAvlg3V30ASQ20HBrZRLE4gMiu2raAtkqqF6y5G9ThEDka1F5GNQB
                            GRB8jnx2L70gw87yQDNn4OSRQSgMgG4MUG7DRukRznDFz3YmA+ItP1dt5XBcdxELmBbPabHHrok7
                            H9MoGq4DgnPcfX8GygUHgIkti1VYlyFOmeeJ7/tm1VwXWvB74NzG9gyUb180xOjlMsXjA1k9xeSq
                            WjY76tAfx0+pj7rpDqUS8pqeN8DNX3hLQ4B5ErcN3L4zlmABPdmsgd0992hVQP1X1rXl+9+kBELo
                            ph+UKKxahn78anGsAW720NQOTO6W+TKSQRUy1S7TNJJic/CMRbPhG5OFb9ODjOkcBATCuj5HKPT3
                            9IppA8z4yQap1GuXx5lmrIRVyWMDb2agN2wmNZRrs1SO5bW/OEdMghi/G8g4xYt6wbGRk5kuHhJ2
                            red5z9gSVU3wg3IvIICxb8ChGN9VxVE6/9t+/6MZlCsqwn8DwTlg6aGk/s/MVVKktjvjLvylx6en
                            7O6OiJDA09+uxVxzka+DDwFqYP6lGtfrnuahzncrZs+cZU0oxwuO4rUA23S2RPnqGv7+5dLyRTSJ
                            OT68kYObtvNqtXzwN+/+wVkaUmDD+Lao5MZgXF4q1Y1h/xvCOAY+vUOBS4hv7+s3GcM7Dth0M+7+
                            1x3AVA5KcMDGzb9VIyx0hPPrkBU+ltPG/hs9+PjOwLHGnE7nPpQ+StqL4PkXoi2pWFwL0Ui28K/J
                            Tq+O7UKA7uxo93v5BMIR1/fBl4yogtz3vts99nMkuIGtfcHGYjcjOOE0wcBx/8WiDu6ZiKakqEVM
                            XUgPtkSqXppZKouyyaSQa4Addd0rCk6lkGnvdbbPsPu19MspBqvwmF5wBUr6dYPAWR0w3ZNE0Pqt
                            +pe6hzqXQI8IbYT6rRGkGyhWRucVT1JERuAuIfB9885jI+bvve9bz3YuLlKpNJnZBMxiXtHVQquZ
                            rXR0bmAOcaeMIfWbDg17VuJFdI1XigdGFZtVfzs9kPAC808ISfTK/27/FoA8Y7E89LX4ukumiPa4
                            5zcKQMI7Xt1+zWIMlCSmPXBieyevXOZZ3qBs9vo2ri2LBJenru8LuZzJltSGfXBnMol39MqfQByu
                            WnKZW+QHWtzgS/4LDDNvndTLKQnkbjrW3ulageieovsSwM//9vrXczuV2biLkdt11A9X/r3U6ukE
                            weudVlFYWCU69AcoW0bduOdruQIH7UqEByhQRdIZlCpG63BkkWUibT7drM8Awiv2hUKLlC6uvrCs
                            kEqneRy21vVCy5Qpo/vyskE4jcFqRYcoX0+OO97XYhEVjW7Y0LBZmQVBXGxv4Kkf2nrvSRyTzBzJ
                            nrmTdvaxwfm8rmzTPJJne+tUW45HKrghSs/ZNeter5TE6+G5E34bovJ5N57tZlVZiYAMd5GngQWA
                            H8Gsu6i1xuc0znzdDbO8vQTpL0ohqoW4NaQnLd0ymXr0QkSNjBfsDSqS/wvB0Ui3cj8kPg+9i2mb
                            jpKHjefm17dlIIOD4C2LlBa82afdix41rAVDjpdkR+gOp12HbD10fjuO5SVH1Xq7s0ZBv9/fsxd2
                            6gdNPVwXap9DJ27FiJOREB9E3tofo5jnNPy7cnq76opc9LGiI/CyoiAIuxsTyet5y4KeDqsxjLWo
                            7j3InjLGxc3ACq+ZY8J6l4XuBuDcDCsv4Z8M8DZJYlwG9wnGumNhs2D5GhptpPOpb1YKjiwKua5I
                            ofGeBcslmXYvGculto4tGali+piKwOVRzH2Up7t9n8Fjjf6IB8fHwelcrvGxfs4sN28vlZfoH+te
                            iEme0jgJ9RLN7IqlVxcxpW8bzXGLFjjruAy4GrMLcDuJn8LoyIACxEftUsb0IgiLyNcrmI43xxly
                            3SUTnNiFcmUP0Ctv0abPsj2Pb5VCrHYnLzZjMQWRO2ikWlchLwwya4E4WZwCfxvBKuez5r1oTvco
                            vFAVTNpp6JTplM5pLnXBka+h2qX26TP8HwvAhCGhx8Gtt+C6p/C/wf0AkR8wegeiU7dqymWLyAtW
                            tnBq4p8ik6o8sG1ZU1l4z6+v4V6OTohAhCmqZQWI5tLwWGELkS+LNBx6JyECJXMDGxBsf5AmNj8+
                            uWrmY6C5uyuHmI1E5kMTDwZ6AThhR+xBDSNLZdJJ//INu2HQKcDTxkwLG4HAh8CstaheP8BMd57x
                            6ict2lwC10SmsEIPIn33uqd/reaz+hhRQsGWKpdCye9xnghLAPaDIbqbac+9G6SdUw3IRt1x74j4
                            29Gsta3mJ/guF5+zM4GGqncrC/3lzuPvL5ZaheGsmx5rEv1ZyKnSgigD7fO563soV+hGFzWBFBmG
                            5ARCkUPjY1fuoSDP+DA4eHNwKP+95vH6G7NYgynsjlLkTka1EelkIObnA/XEba1hBqaWSa8EISUX
                            K584DvRHlgyjik7l2RkRb5EYYWCQlAxCOf/wdU/yNS/fQwh1Wr6o3fIv3Smkzdrdl+RH9VFqmwfv
                            0ZwM2RbaQBz/NvlSIsRTQdy3IjVYv10OOPL5PPnwJcH8tOkimX/YU0Odl5QspkilGqxZ+8E6mQz5
                            9FdXW7y+6I+AtpYuIxTJ1QYIZNUY9KNTMLLKLY9kdQ/TjQ3QO0KyL+b26LFk2iukfy8zYSaXwEpp
                            cTCoVLEHkz0Bl72zqDRm9uv2uRH0GI1K1BM9al8vlb8byjiKHuhNFoU0UntUiRZ9ubs8A5OOhiWU
                            cjcmNT7O9dNIr6XNcSL4IgEnmCtHkr5bncZvL5d6B6Cp0RktIu6gvJ3GmX8bGsDmuRdqVQ+C8sax
                            GdEH8j8hvgNqDcwqfOYc2aferc75Su7UkWLPhj1Mqtid3J5VaRzy9G5ByqoR+tZhLVU8nnF2Hbr8
                            fzltFKMW3f7t8qiXRG16Yaa92vdUFg1WWV6wAb+CatnSa4iULh+89+Ghy8HdVPt+zpluU/4J6c7A
                            whiYTaELk7rY8mtO2nsO2zEDkO+GVLnqn6SA0/LkX1Zy15vuf5t0idIiTLivW7aF9Yaj5/P7a9GN
                            XXAzWPbjKGyJ4LpyKK551Ha4Lw/SclFy58hva/jCied18cA+2Pby4UbsO2X4HIW4FA2cEicHjNq9
                            Uj0q8yYP9xRD6G6kIs6+VUl4t2CtSy5jSov9aAD3Fw4uayar+Qpsnnb8ayhoGLMd9KvIoVK3pq3r
                            GszxLnIGXVOyiXB8nnL6VQWEku9xC2/RHgg7uUmdXASnuFJBJ7iNE5QgLI5bZj258FjsJs9GA/c+
                            a83ueZm4F/iWh3CyJvZ3j4L3vcyee/Btw/9an+vjzVducpiJ13obOENI1tP0xv7zFU3+7MIOK/32
                            3WrGuJNsN8lW+XIKLA+YA3dW5aPd/a2SIp5XKgzLX16EwhAQwMbJt6u3sPYCJ77gmMj9d+DZ83by
                            uqn29QfwfVv9zbqC5u3otlfaluDdv+NSJfpXFAffuEJPIgQ0OxZ9c7P39wPv8tXHcU1R8BB8Sw1E
                            OlciHwoZp3K5XryWY/CgzUuLuccvltDA+HPwI+l/sQjz3mvy0JwPPWYrXpb7rO8aJh6NwWaVfy+f
                            tRPYYYYQ5TnI3j7F/zzvDwDkQ+V+POKP39yyKJCKpd3MDAtrplMpn2jZECHFgThL1DSACFwho876
                            +JN4k5G7jQ924udwMw+pxrlvWJMEk5IyHyB+LP9G+mGj9/HqpvBk4EvkH9CMx15HIPxHwuEHTLdi
                            exbt0stmy5henc3uHZhuoQhULtcUt1K/VdTP9sentfMJX0obm4rotqLnQ9kUfxvGuoVL5b8+2xmi
                            b6VmDPIzVEvkQ+/4ko7u7O3tMiTTN37gS9vW8CovbtM7CsS3zvDg7ejeplU58qzJ/fmmjPWss49R
                            kHlpDPv5RC4es1RQSQz9/pu9Xe874V8pm+7H1CguobXbl8ItXsI+FRPYlSyT8Jq21/EtWPI3JZ2B
                            R4MQgTC3Qz2ewibPungUpbVq2XqnsbHS8ahs5/a/NjeHgHK1acQn//d4FTQtf3vCtQXYTInmOI6j
                            X/VqsZiNwb6FRs1Uux7Y9PzVPVZ2RkX3p6vo7qyTXsGGuNYG9tkaZZtGiSdeveTrSW6Qhct3OScm
                            3deh/1j0/1gA9MJfJoLCLXXUY2+2hNEcGTPO95/xnR05rs3UKC6iZNyzoNiJK46vMGEp+aYeHCZ+
                            ocIrMZkTdj21cHsuW6Z07Nux1U877IZabfRPd+IUF1ja6//y3APSFrHtDSALdGiFxT4+oDeN5R5P
                            O3BrIxOnoQqlfi/0a+ga1bjWeTSYaQoPo2l80um4rLDo7nncf4eJwZc3PkcndMvWFtR+RRRM5hy5
                            bFDA4G349vWZcB/q2s6uVTMVBG2fvmkRpRnbm+GxgOXEfkIvL5RmttnY/jvBP49zol1lIuD/lOFc
                            QgOS3SNLb9FJXKUkRKgeuovrp5DrWIYnERUL/LEjm3GSKCJAoJYGhoPZb1GuCxgDVe0cTDdZqP6w
                            5OrZnNrlPqpsDjrAgkU0gACxasxbKWEGzf2BzGx2uH43Y6jrMQ1bsB/6NjRf5ET88FzXQjuUICpk
                            6IXgI03vjnecc13R/TVGfn76Z+eI2i+r6o6WqCkmwhQTUBffVskvobM0WObY1DhigWT8bzbgfq7e
                            IFkUuw7Zua7U7yhQRQKKxE9bXApjqljm6VO7FxnPcj8j3q5fGuchu5XEvmydIhJIBCYQXwRvzCdl
                            UXsHLlC1rqUxQc58NUt1A1igMv0dt7es21xCaQHiEB2PYvsKxTqb3vX5gxY1GrXQqF654NXEbj+b
                            +n8Lw3tiSOaop0CQkgl/sf32UR1aNa7E1wSqU3onptgJJ/AU4wGSIShPQJCcC2L6P2ulxnCml8fA
                            GedwPVg6XrMYnqydi2kfDZMKRTSNVgtU/WuHNMq11pyNq1M6lUfkCQg3tU30eh4BdB0FTSKSSAfP
                            5eYPfF0Bfhuoe2wx1fJiYuJdjR89+jUGhbvvP0CqkaHHbHHtc9r3Pmk6qHGZ4boORGtm8PUq5ppF
                            dIAKqje1yr5m1qP2vW7IPqvxEkQkPkyxx+uP9plS0g3UISqRXn0xlC2rHjKzTK0V1lC5731Wa704
                            h0C8myav0VH06p5L8A2gpcdxlwZsDSt1AobGmiN4FIt5DK5VqxORaqS1ruyzQjI/uiel3g8iLfb1
                            yo+aRbSCK1g7xUT22xJzvJZq8E5gYsvQ2RjjitO91CUt3uc+cERkdf3FJfHn54No5zNfCOwHVUHy
                            KX8/s/tJR0C2ly0m8XbQ+ZTOt2l7juG5gxwwHeH6qeZd3fuFBrSLeQZs+utx37TMbG5jfdh2qSh1
                            tofJByLZqbDTgE6RaSf4sE0INlXdx0H1S/StSt87XmwdpEuoVUqTTa+vwuxsaaN69UKh0GFCLXV+
                            2Yw5XTLaRyuZGQBMu6uok7TIJMOPqxoRPmj6ZJt5CC8TJc96KmWK5UDoxRu1nJ7SPRFVIwPoPr/k
                            27ndiNx9rtwK50hRSMDKo3Mja2n1GrqpHPR0MkWnLUJtEVUnAOwbK+YdRiNrshcl3Pa8e5d750hR
                            SOv8dxzMX9eF6cTYvRRdgEukIKz5dx3SOMWKoePxG1i4p1mpFpukIKTx+ed4VBew9FqqXaFdJej8
                            ircJwoSxp7ohr1CNCnjTzfEF0hRcXzzEQHWFY0IWWzbQ2t3Z10C+nww7cCp02lCg53zJaqmcFupR
                            JNSJVKvTwGLSd5qf/iMDb20qmcSq+kGrvtN/P8ALZtLumE46zDLwNtbcrk872B0iS3iL03YXszGB
                            x8BHgE+AoAo6M5MpnjEHkZ1ahFmVpxN3EO7k5E7vHJh+3Hpk4SEXSFVJ+hoRJQAr7T5CfdA7yO6g
                            lHm6jm1a7+q/onVDdhWdOfN8WaEW8S/w/ViE0ecu00qQAAAABJRU5ErkJggg==''')


def get_config_param(option, section='DEFAULT'):
    config = ConfigParser()
    config.read(['./config/config.ini', './config.ini'])
    return config.get(section, option).replace('%', '%%')


def settings_window():
    default_frame = sg.Frame('Default Settings', [[sg.Column([[sg.Text('Resolution:')],
                                                              [sg.Input(k='res', size=(3, 1),
                                                                        default_text=get_config_param('res'))],
                                                              [sg.Text('Adapter Thickness:')],
                                                              [sg.Input(k='adapt_thick', size=(4, 1),
                                                                        default_text=get_config_param('adapt_thick'))],
                                                              [sg.Text('Light to Lith Distance:')],
                                                              [sg.Input(k='light_to_lith_dis', size=(3, 1),
                                                                        default_text=get_config_param('light_to_lith_dis'))],
                                                              [sg.Text('User:')],
                                                              [sg.Input(k='user', size=(20,1),
                                                                        default_text=get_config_param('user'))],
                                                              [sg.Text('Nightlight URL:')],
                                                              [sg.Input(k='nl_url', size=(20,1),
                                                                        default_text=get_config_param('nl_url'))],
                                                              [sg.Text('Window URL:')],
                                                              [sg.Input(k='window_url', size=(20,1),
                                                                        default_text=get_config_param('window_url'))]
                                                              ], vertical_alignment='top'),
                                                   sg.Column([[sg.Text('Minimum Thickness:')],
                                                             [sg.Input(k='min_thick', size=(3, 1),
                                                                       default_text=get_config_param('min_thick'))],
                                                            [sg.Text('Maximum Thickness:')],
                                                            [sg.Input(k='max_thick', size=(3, 1),
                                                                      default_text=get_config_param('max_thick'))],
                                                            [sg.Text('Frame Width:')],
                                                            [sg.Input(k='frame_width', size=(3, 1),
                                                                      default_text=get_config_param('frame_width'))],
                                                            [sg.Text('Slot Width:')],
                                                            [sg.Input(k='slot_width', size=(4, 1),
                                                                      default_text=get_config_param('slot_width'))],
                                                            [sg.Text('Slot Depth:')],
                                                            [sg.Input(k='slot_depth', size=(4, 1),
                                                                      default_text=get_config_param('slot_depth'))]], vertical_alignment='top')]], pad=5)
    nl_frame = sg.Frame('NightLight Settings', [[sg.Column([[sg.Frame('Square', [[sg.Text('Radius:')],
                                                 [sg.Input(k='nl_sq_rad', size=(3, 1),
                                                           default_text=get_config_param('nl_sq_rad'))],
                                                 [sg.Text('Width:')],
                                                 [sg.Input(k='nl_sq_wid', size=(6, 1),
                                                           default_text=get_config_param('nl_sq_wid'))],
                                                 [sg.Text('Height:')],
                                                 [sg.Input(k='nl_sq_hei', size=(6, 1),
                                                           default_text=get_config_param('nl_sq_hei'))],
                                                 [sg.Text('GIMP Crop Ratio:')],
                                                 [sg.Input(k='nl_sq_gimp', size=(6, 1),
                                                           default_text=get_config_param('nl_sq_gimp'))]
                                                 ], pad=5)]]),
                                     sg.Column([[sg.Frame('Portrait', [[sg.Text('Radius:')],
                                                   [sg.Input(k='nl_por_rad', size=(3, 1),
                                                             default_text=get_config_param('nl_por_rad'))],
                                                   [sg.Text('Width:')],
                                                   [sg.Input(k='nl_por_wid', size=(6, 1),
                                                             default_text=get_config_param('nl_por_wid'))],
                                                   [sg.Text('Height:')],
                                                   [sg.Input(k='nl_por_hei', size=(6, 1),
                                                             default_text=get_config_param('nl_por_hei'))],
                                                   [sg.Text('GIMP Crop Ratio:')],
                                                   [sg.Input(k='nl_por_gimp', size=(6, 1),
                                                             default_text=get_config_param('nl_por_gimp'))]
                                                   ], pad=5)]]),
                                     sg.Column([[sg.Frame('Square', [[sg.Text('Radius:')],
                                                 [sg.Input(k='nl_lan_rad', size=(3, 1),
                                                           default_text=get_config_param('nl_lan_rad'))],
                                                 [sg.Text('Width:')],
                                                 [sg.Input(k='nl_lan_wid', size=(6, 1),
                                                           default_text=get_config_param('nl_lan_wid'))],
                                                 [sg.Text('Height:')],
                                                 [sg.Input(k='nl_lan_hei', size=(6, 1),
                                                           default_text=get_config_param('nl_lan_hei'))],
                                                 [sg.Text('GIMP Crop Ratio:')],
                                                 [sg.Input(k='nl_lan_gimp', size=(6, 1),
                                                           default_text=get_config_param('nl_lan_gimp'))]
                                                 ], pad=5)]])]])

    window_frame = sg.Frame('Window Cling Settings', [[sg.Column([[sg.Frame('Small',
                                                    [[sg.Text('Frame:')],
                                                              [sg.Input(k='w_sm_frame', size=(9, 1),
                                                                        default_text=get_config_param('w_sm_frame'),
                                                                        disabled=True,
                                                                        disabled_readonly_background_color='grey')],
                                                              [sg.Text('Width:')],
                                                              [sg.Input(k='w_sm_wid', size=(6, 1),
                                                                        default_text=get_config_param('w_sm_wid'))],
                                                              [sg.Text('Height:')],
                                                              [sg.Input(k='w_sm_hei', size=(6, 1),
                                                                        default_text=get_config_param('w_sm_hei'))]
                                                              ], pad=5)]]),
                                                       sg.Column([[sg.Frame('Medium',
                                                    [[sg.Text('Frame:')],
                                                               [sg.Input(k='w_med_frame', size=(9, 1),
                                                                         default_text=get_config_param('w_med_frame'),
                                                                         disabled=True,
                                                                         disabled_readonly_background_color='grey')],
                                                               [sg.Text('Width:')],
                                                               [sg.Input(k='w_med_wid', size=(6, 1),
                                                                         default_text=get_config_param('w_med_wid'))],
                                                               [sg.Text('Height:')],
                                                               [sg.Input(k='w_med_hei', size=(6, 1),
                                                                         default_text=get_config_param('w_med_hei'))]
                                                               ], pad=5)]]),
                                                       sg.Column([[sg.Frame('Large', [[sg.Text('Frame:')],
                                                      [sg.Input(k='w_lrg_frame', size=(9, 1),
                                                                default_text=get_config_param('w_lrg_frame'),
                                                                disabled=True,
                                                                disabled_readonly_background_color='grey')],
                                                      [sg.Text('Width:')],
                                                      [sg.Input(k='w_lrg_wid', size=(6, 1),
                                                                default_text=get_config_param('w_lrg_wid'))],
                                                      [sg.Text('Height:')],
                                                      [sg.Input(k='w_lrg_hei', size=(6, 1),
                                                                default_text=get_config_param('w_lrg_hei'))]
                                                      ], pad=5)]])]])

    layout = [[default_frame],
              [nl_frame],
              [window_frame],
              [sg.Button('Save'), sg.Button('Close')], [sg.Button('Load Default Values', key='-load_defaults-')]]
    return sg.Window('Settings', layout, finalize=True, modal=True, resizable=True)


def settings_window_tabbed():
    default_tab = [[sg.Column([[sg.Text('Resolution:')],
                  [sg.Input(k='res', size=(3, 1),
                            default_text=get_config_param('res'))],
                  [sg.Text('Adapter Thickness:')],
                  [sg.Input(k='adapt_thick', size=(4, 1),
                            default_text=get_config_param('adapt_thick'))],
                  [sg.Text('Light to Lith Distance:')],
                  [sg.Input(k='light_to_lith_dis', size=(3, 1),
                            default_text=get_config_param('light_to_lith_dis'))],
                  [sg.Text('User:')],
                  [sg.Input(k='user', size=(20,1),
                            default_text=get_config_param('user'))],
                  [sg.Text('Nightlight URL:')],
                  [sg.Input(k='nl_url', size=(20,1),
                            default_text=get_config_param('nl_url'))],
                  [sg.Text('Window URL:')],
                  [sg.Input(k='window_url', size=(20,1),
                            default_text=get_config_param('window_url'))]
                  ], vertical_alignment='top'),
       sg.Column([[sg.Text('Minimum Thickness:')],
                  [sg.Input(k='min_thick', size=(3, 1),
                            default_text=get_config_param('min_thick'))],
                  [sg.Text('Maximum Thickness:')],
                  [sg.Input(k='max_thick', size=(3, 1),
                            default_text=get_config_param('max_thick'))],
                  [sg.Text('Frame Width:')],
                  [sg.Input(k='frame_width', size=(3, 1),
                            default_text=get_config_param('frame_width'))],
                  [sg.Text('Slot Width:')],
                  [sg.Input(k='slot_width', size=(4, 1),
                            default_text=get_config_param('slot_width'))],
                  [sg.Text('Slot Depth:')],
                  [sg.Input(k='slot_depth', size=(4, 1),
                            default_text=get_config_param('slot_depth'))]], vertical_alignment='top')]]
    nl_tab = [[sg.Column([[sg.Frame('Square', [[sg.Text('Radius:')],
                         [sg.Input(k='nl_sq_rad', size=(3, 1),
                                   default_text=get_config_param('nl_sq_rad'))],
                         [sg.Text('Width:')],
                         [sg.Input(k='nl_sq_wid', size=(6, 1),
                                   default_text=get_config_param('nl_sq_wid'))],
                         [sg.Text('Height:')],
                         [sg.Input(k='nl_sq_hei', size=(6, 1),
                                   default_text=get_config_param('nl_sq_hei'))],
                         [sg.Text('GIMP Crop Ratio:')],
                         [sg.Input(k='nl_sq_gimp', size=(6, 1),
                                   default_text=get_config_param('nl_sq_gimp'))]
                         ], pad=5)]]),
     sg.Column([[sg.Frame('Portrait', [[sg.Text('Radius:')],
                           [sg.Input(k='nl_por_rad', size=(3, 1),
                                     default_text=get_config_param('nl_por_rad'))],
                           [sg.Text('Width:')],
                           [sg.Input(k='nl_por_wid', size=(6, 1),
                                     default_text=get_config_param('nl_por_wid'))],
                           [sg.Text('Height:')],
                           [sg.Input(k='nl_por_hei', size=(6, 1),
                                     default_text=get_config_param('nl_por_hei'))],
                           [sg.Text('GIMP Crop Ratio:')],
                           [sg.Input(k='nl_por_gimp', size=(6, 1),
                                     default_text=get_config_param('nl_por_gimp'))]
                           ], pad=5)]]),
     sg.Column([[sg.Frame('Square', [[sg.Text('Radius:')],
                             [sg.Input(k='nl_lan_rad', size=(3, 1),
                                       default_text=get_config_param('nl_lan_rad'))],
                             [sg.Text('Width:')],
                             [sg.Input(k='nl_lan_wid', size=(6, 1),
                                       default_text=get_config_param('nl_lan_wid'))],
                             [sg.Text('Height:')],
                             [sg.Input(k='nl_lan_hei', size=(6, 1),
                                       default_text=get_config_param('nl_lan_hei'))],
                             [sg.Text('GIMP Crop Ratio:')],
                             [sg.Input(k='nl_lan_gimp', size=(6, 1),
                                       default_text=get_config_param('nl_lan_gimp'))]
                             ], pad=5)]])]]

    window_tab = [[sg.Column([[sg.Frame('Small',
                                [[sg.Text('Frame:')],
                                 [sg.Input(k='w_sm_frame', size=(9, 1),
                                           default_text=get_config_param('w_sm_frame'),
                                           disabled=True,
                                           disabled_readonly_background_color='grey')],
                                 [sg.Text('Width:')],
                                 [sg.Input(k='w_sm_wid', size=(6, 1),
                                           default_text=get_config_param('w_sm_wid'))],
                                 [sg.Text('Height:')],
                                 [sg.Input(k='w_sm_hei', size=(6, 1),
                                           default_text=get_config_param('w_sm_hei'))]
                                 ], pad=5)]]),
           sg.Column([[sg.Frame('Medium',
                                [[sg.Text('Frame:')],
                                 [sg.Input(k='w_med_frame', size=(9, 1),
                                           default_text=get_config_param('w_med_frame'),
                                           disabled=True,
                                           disabled_readonly_background_color='grey')],
                                 [sg.Text('Width:')],
                                 [sg.Input(k='w_med_wid', size=(6, 1),
                                           default_text=get_config_param('w_med_wid'))],
                                 [sg.Text('Height:')],
                                 [sg.Input(k='w_med_hei', size=(6, 1),
                                           default_text=get_config_param('w_med_hei'))]
                                 ], pad=5)]]),
           sg.Column([[sg.Frame('Large', [[sg.Text('Frame:')],
                                      [sg.Input(k='w_lrg_frame', size=(9, 1),
                                                default_text=get_config_param('w_lrg_frame'),
                                                disabled=True,
                                                disabled_readonly_background_color='grey')],
                                      [sg.Text('Width:')],
                                      [sg.Input(k='w_lrg_wid', size=(6, 1),
                                                default_text=get_config_param('w_lrg_wid'))],
                                      [sg.Text('Height:')],
                                      [sg.Input(k='w_lrg_hei', size=(6, 1),
                                                default_text=get_config_param('w_lrg_hei'))]
                                      ], pad=5)]])]]

    box_tab = [[sg.Column([[sg.Frame('Small',
                                        [[sg.Text('Size:')],
                                         [sg.Input(k='b_sm_size', size=(3, 1),
                                                   default_text=get_config_param('b_sm_size'))],
                                        [sg.Text('Frame:')],
                                         [sg.Input(k='b_frame', size=(12, 1),
                                                   default_text=get_config_param('b_frame'),
                                                   disabled=True,
                                                   disabled_readonly_background_color='grey')],
                                         [sg.Text('Outer Frame Thickness:')],
                                         [sg.Input(k='b_frame_width', size=(6, 1),
                                                   default_text=get_config_param('b_frame_width'))],
                                         [sg.Text('Outer Frame Width:')],
                                         [sg.Input(k='b_frame_height', size=(6, 1),
                                                   default_text=get_config_param('b_frame_height'))],
                                         [sg.Text('Outer Frame Angle:')],
                                         [sg.Input(k='b_frame_angle', size=(6, 1),
                                                   default_text=get_config_param('b_frame_angle'))]
                                         ], pad=5)]]),
                   # sg.Column([[sg.Frame('Medium',
                   #                      [[sg.Text('Frame:')],
                   #                       [sg.Input(k='box_sm_frame', size=(12, 1),
                   #                                 default_text=get_config_param('b_frame'),
                   #                                 disabled=True,
                   #                                 disabled_readonly_background_color='grey')],
                   #                       [sg.Text('Width:')],
                   #                       [sg.Input(k='b_frame_width', size=(6, 1),
                   #                                 default_text=get_config_param('b_frame_width'))],
                   #                       [sg.Text('Height:')],
                   #                       [sg.Input(k='b_frame_height', size=(6, 1),
                   #                                 default_text=get_config_param('b_frame_height'))]
                   #                       ], pad=5)]]),
                   # sg.Column([[sg.Frame('Large', [[sg.Text('Frame:')],
                   #                                [sg.Input(k='box_sm_frame', size=(12, 1),
                   #                                          default_text=get_config_param('b_frame'),
                   #                                          disabled=True,
                   #                                          disabled_readonly_background_color='grey')],
                   #                                [sg.Text('Width:')],
                   #                                [sg.Input(k='b_frame_width', size=(6, 1),
                   #                                          default_text=get_config_param('b_frame_width'))],
                   #                                [sg.Text('Height:')],
                   #                                [sg.Input(k='b_frame_height', size=(6, 1),
                   #                                          default_text=get_config_param('b_frame_height'))]
                   #                                ], pad=5)]])
                ]]

    layout = [[sg.TabGroup([[sg.Tab('Default', default_tab, k='-default_tab-'), sg.Tab('Nightlight', nl_tab),
                             sg.Tab('Window', window_tab), sg.Tab('Box', box_tab)]], enable_events=True, key='-tab_group-')],
              [[sg.Button('Save'), sg.Button('Close')], [sg.Button('Load Default Values', key='-load_defaults-')]]]
    return sg.Window('Settings', layout, finalize=True, modal=True, resizable=True)

window_main, window_settings = main_window(), None
window = None
# base_type = None
# sub_type = None
while True:

    event, values = window_main.read(timeout=1000)


    if event == sg.WIN_CLOSED or event == 'Exit':
        window_main.close()
        break

    if event == sg.WIN_CLOSED or event == 'Exit':
        window_main.close()
    if window == window_main:  # if closing win 2, mark as closed
        window_main = None
    elif window == window_settings:  # if closing win 1, mark as closed
        window_settings = None

    if values['-nightlight-'] and values['-square-']:
        base_type = 'nl'
        sub_type = 'square'
    elif values['-nightlight-'] and values['-portrait-']:
        base_type = 'nl'
        sub_type = 'portrait'
    elif values['-nightlight-'] and values['-landscape-']:
        base_type = 'nl'
        sub_type = 'landscape'
    elif values['-wind_cling-'] and values['-small-']:
        base_type = 'wind'
        sub_type = 'sm'
    elif values['-wind_cling-'] and values['-medium-']:
        base_type = 'wind'
        sub_type = 'med'
    elif values['-wind_cling-'] and values['-large-']:
        base_type = 'wind'
        sub_type = 'lrg'
    elif values['-box-'] and values['-small-']:
        base_type = 'box'
        sub_type = 'sm'
    elif values['-box-'] and values['-medium-']:
        base_type = 'box'
        sub_type = 'med'
    elif values['-box-'] and values['-large-']:
        base_type = 'box'
        sub_type = 'lrg'

    if values['-load_img_btn-'] != '':
        filename_elem = window_main['-filename-']
        fp = os.path.normpath(values['-load_img_btn-'])
        fn = os.path.basename(fp)
        filename_elem.update(fn)
        if os.path.exists(fp):
            image = Image.open(values["-load_img_btn-"])
            image.thumbnail((300, 300))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window_main["-IMAGE-"].update(data=bio.getvalue())
    if values['-dl_path_btn-'] != '':
        dl_path_elem = window_main['-dl_path-']
        dl_path = os.path.normpath(values['-dl_path_btn-'])
        dl_path_elem.update(dl_path)
    if event == '-wind_cling-':
        window_main['-small-'].update(visible=True)
        window_main['-medium-'].update(visible=True)
        window_main['-large-'].update(visible=True)
        window_main['-square-'].update(visible=False)
        window_main['-portrait-'].update(visible=False)
        window_main['-landscape-'].update(visible=False)

    if event == '-nightlight-':
        window_main['-small-'].update(visible=False)
        window_main['-medium-'].update(visible=False)
        window_main['-large-'].update(visible=False)
        window_main['-square-'].update(visible=True)
        window_main['-portrait-'].update(visible=True)
        window_main['-landscape-'].update(visible=True)

    if event == '-box-':
        window_main['-small-'].update(visible=True)
        window_main['-medium-'].update(visible=True)
        window_main['-large-'].update(visible=True)
        window_main['-square-'].update(visible=False)
        window_main['-portrait-'].update(visible=False)
        window_main['-landscape-'].update(visible=False)

    if event == 'Create File':
        try:
            my_lith = Lithophane(base_type)
            if base_type == 'nl':
                my_lith.dl_nl(fp, dl_path, sub_type)
            elif base_type == 'box':
                my_lith.dl_box(fp, dl_path, sub_type)
            else:
                my_lith.dl_wind(fp, dl_path, sub_type)
        except NameError as err:
            print(err)
            sg.PopupOK('Make sure all fields are set', )


    # if event != sg.TIMEOUT_KEY:
    #     print(event, values)
    #     print(base_type, sub_type)

    if event == '-settings_btn-':
        window = settings_window_tabbed()
        config = ConfigParser()
        config.read(['./config/config.ini', './config.ini'])

        ###################################
        #   Loop for the settings window
        ###################################
        while True:
            event, values = window.read(timeout=1000)
            # if event != sg.TIMEOUT_KEY:
            print(values)
            if event == sg.WIN_CLOSED or event == 'Close':
                window.close()
                break
            elif event == '-load_defaults-':
                config2 = ConfigParser()
                config2.read(['./default_config.ini', './config/default_config.ini'])
                for x in config2['DEFAULT']:
                    window[x].update(config2['DEFAULT'][x].replace('%', '%%'))
                    # print(config2['DEFAULT'][x])
            elif event == 'Save':
                # print('you saved')
                for k in values:
                    if k is not None and k != '-tab_group-':
                        print(k, values[k])
                        config.set('DEFAULT', k, values[k])
                with open('./config/config.ini', 'w') as configfile:
                    config.write(configfile)


window_main.close()
