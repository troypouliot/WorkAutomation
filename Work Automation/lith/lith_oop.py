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

    def dl_nl(self):
        self.start_browser()
        self.clear_fields()
        self.driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
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

if __name__ == '__main__':


    my_lith = Lithophane(template, f'{template}_{size}')


    my_lith.dl_nl()


