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
