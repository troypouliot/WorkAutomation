import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from configparser import ConfigParser
from os import getcwd



config = ConfigParser()

config.read('config.ini')


class Lithophane():
    def __init__(self, type, subtype):
        self.type = type
        self.subtype = subtype
        if self.type == 'nl':
            self.url = 'https://lithophanemaker.com/Night%20Light%20Lithophane.html'
        elif self.type == 'wind':
            self.url = 'https://lithophanemaker.com/Framed%20Lithophane.html'

    def dl_nl(self):
        pass

    def dl_wind(self):
        pass



my_lith = Lithophane(te := 'nl', f'{te}' + '_' + 'portrait')

res = config.get(my_lith.subtype, 'res')
width = config.get(my_lith.subtype, 'width')
height = config.get(my_lith.subtype, 'height')
max_thick = config.get(my_lith.subtype, 'max_thick')
min_thick = config.get(my_lith.subtype, 'min_thick')
user_email = config.get(my_lith.subtype, 'user')
frame_width = config.get(my_lith.subtype, 'frame_width')
slot_width = config.get(my_lith.subtype, 'slot_width')
slot_depth = config.get(my_lith.subtype, 'slot_depth')
adapt_thick = config.get(my_lith.subtype, 'adapt_thick')
light_to_lith_dis = config.get(my_lith.subtype, 'light_to_lith_dis')
radius = config.get(my_lith.subtype, 'radius')

op = webdriver.ChromeOptions()
p = {"download.default_directory": "C:\\Users\\troypouliot\\test", "safebrowsing.enabled":"false"}
op.add_experimental_option('prefs', p)
driver = webdriver.Chrome(options=op)
driver.get(my_lith.url)


inputs = driver.find_elements_by_tag_name('input')
for item in inputs:
    try:
        item.clear()
    except selenium.common.exceptions.InvalidElementStateException:
        pass


if my_lith.type == 'wind':
    select = Select(driver.find_element_by_id('hole_num'))
    select.select_by_visible_text('No Border')
    upload_btn = driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
    f_res = driver.find_element_by_id('lith_res').send_keys(res)
    f_width = driver.find_element_by_id('base_length').send_keys(width)
    f_height = driver.find_element_by_id('height').send_keys(height)
    f_max_thick = driver.find_element_by_id('max_thickness').send_keys(max_thick)
    f_min_thick = driver.find_element_by_id('min_thickness').send_keys(min_thick)
    user = driver.find_element_by_id('emailAddress').send_keys(user_email)
    download_btn = driver.find_element_by_name('submit')

else:
    upload_btn = driver.find_element_by_name('fileToUpload').send_keys(getcwd() + '/test.png')
    f_res = driver.find_element_by_id('lith_res').send_keys(res)
    f_max_thick = driver.find_element_by_id('t_max').send_keys(max_thick)
    f_min_thick = driver.find_element_by_id('t_min').send_keys(min_thick)
    f_frame_width = driver.find_element_by_id('frame_width').send_keys(frame_width)
    f_slot_width = driver.find_element_by_id('w_slot').send_keys(slot_width)
    f_slot_depth = driver.find_element_by_id('d_slot').send_keys(slot_depth)
    f_adapt_thick = driver.find_element_by_id('t_base').send_keys(adapt_thick)
    f_light_to_lith_dis = driver.find_element_by_id('LLS').send_keys(light_to_lith_dis)
    f_radius = driver.find_element_by_id('radius').send_keys(radius)
    f_width = driver.find_element_by_id('x_span').send_keys(width)
    f_height = driver.find_element_by_id('z_dim').send_keys(height)
    user = driver.find_element_by_id('emailAddress').send_keys(user_email)
    download_btn = driver.find_element_by_name('submit')
    f_x_shift = driver.find_element_by_id('x_shift').send_keys('0.5')
    f_y_shift = driver.find_element_by_id('y_shift').send_keys('0.5')
    f_rect_scale = driver.find_element_by_id('rect_scale').send_keys('1.0')

download_btn.click()
# driver.quit()

