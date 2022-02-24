from numpy import uint8, array
from cv2 import FONT_HERSHEY_SIMPLEX, putText, waitKey, destroyAllWindows, imshow, imdecode, resize, setWindowProperty,\
    WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN, namedWindow, imread, error
from requests import get, ConnectionError as cError
from keyboard import is_pressed
from time import time
from winsound import Beep
from threading import Thread
from pyaudio import PyAudio, paInt16
from tkinter import *
from tkinter import ttk
import configparser


def is_all_file_to_dir():
    print('file test')
    try:
        print('config.ini test found')
        with open('config.ini', 'r') as _a:
            print('config.ini found')
            print(_a.read())
    except FileNotFoundError as fe:
        print(fe)
        print('config.ini not found')
        with open('config.ini', 'w') as file:
            print('create config.ini')
            file.write("""[DEFAULT]
locate_to_img = 
update_send_to_android = 1.0
full_time_flash = 25
size_windows = 1920 1080
audio_beep = 500 400
count_battery_pie = 60
use_microphone = True
use_camera = True
fullscreen = True""")
            print('writing data in config.ini')
            file.close()
            print('file config.ini create and save')
            print('file config.ini close')
    try:
        print('ips.cfg test found.')
        with open('ips.cfg', 'r') as _b:
            print('ips.cfg found')
            print(_b.read())
    except FileNotFoundError as fe:
        print(fe)
        print('ips.cfg not found')
        with open('ips.cfg', 'w') as file:
            print('create ips.cfg')
            file.write('')
            print('writing data in ips.cfg')
            file.close()
            print('file ips.cfg create and save')
            print('file ips.cfg close')


class IPweb:
    def __init__(self, list_address):
        config = configparser.ConfigParser()
        config.read('config.ini')
        # option
        self.locate_to_img = str(config['DEFAULT']['locate_to_img'])
        self.update_send_to_android = float(config['DEFAULT']['update_send_to_android'])
        self.full_time_flash = int(config['DEFAULT']['full_time_flash'])
        s1 = config['DEFAULT']['size_windows'].split()
        self.size_windows = (int(s1[0]), int(s1[1]))
        s2 = config['DEFAULT']['audio_beep'].split()
        self.audio_beep = (int(s2[0]), int(s2[1]))
        self.count_battery_pie = int(config['DEFAULT']['count_battery_pie'])
        self.microphone = (True if config['DEFAULT']['use_microphone'] else False)
        self.camera = (True if config['DEFAULT']['use_camera'] else False)
        self.fullscreen =(True if config['DEFAULT']['fullscreen'] == 'True' else False)
        print(self.fullscreen)
        #
        self.range_list = lambda _list: [_list for self.i in range(len(ips_ADDRESS))]
        self.flash = self.range_list(False)
        self.overlay = self.range_list(False)
        self.night = self.range_list(False)
        self.i = None
        self.battery_pie = self.range_list(float(self.count_battery_pie))
        self.microphone_list = self.range_list(bool(self.microphone))
        self.camera_list = self.range_list(bool(self.camera))
        self.sm = 0
        self.start_time_flash = None
        self.end_flash_time = None
        self.time_flash = self.range_list(self.full_time_flash)
        self.p1 = None
        self.ip = None
        self.ips = list_address
        self.req = None
        self.req_context = None
        self.format_line = ''.join('|' for self.i in range(self.count_battery_pie))
        self.numpy_img = None
        self.img = None
        self.connect = self.range_list(True)
        self.time_std = None
        self.win_id = 0
        self.audio_ = None
        self.fg = 0
        self.cord = None
        self.start_time = time()
        self.start_time_2 = time()
        self.start_time_3 = time()
        self.start_time_4 = time()
        self.start_time_5 = time()
        self.start_time_6 = time()
        self.start_time_7 = time()
        self.start_time_8 = time()
        print(f'connected to {{id:{self.win_id},device: camera}}')
        print(f'connected to {{id:{self.win_id},device: microphone}}')
        self.p1_desk = lambda: self.audio_stream()
        self.p1 = Thread(target=self.p1_desk)
        if self.microphone_list[self.win_id-1]:
            self.action_microphone()
        self.stop = None
        self.poc = 0
        while True:
            self.action_camera()
            if is_pressed('space'):
                if time() - self.start_time > 1:
                    if self.win_id < len(self.ips):
                        self.wait()
                        self.win_id += 1
                        print(f'connected to {{id:{self.win_id},device: camera}}')
                        print(f'connected to {{id:{self.win_id},device: microphone}}')
                        self.beep()
                        if self.p1.is_alive():
                            if self.microphone_list[self.win_id-1]:
                                self.stop = True
                                self.p1.join()
                                self.action_microphone()
                    if self.win_id >= len(self.ips):
                        self.wait()
                        self.win_id = 0
                    destroyAllWindows()
            if is_pressed('m'):
                if time() - self.start_time_6 > self.update_send_to_android:
                    self.stop = True
                    if self.microphone_list[self.win_id-1]:
                        print('microphone disconnected')
                        self.microphone_list[self.win_id-1] = False
                        if self.p1.is_alive():
                            self.p1.join()
                    else:
                        self.microphone_list[self.win_id-1] = True
                        self.action_microphone()
                    self.start_time_6 = time()
            if is_pressed('c'):
                if time() - self.start_time_7 > self.update_send_to_android:
                    if self.camera_list[self.win_id-1]:
                        print('camera disconnected')
                        self.camera_list[self.win_id-1] = False
                    else:
                        print('camera connected')
                        self.camera_list[self.win_id-1] = True
                    self.start_time_7 = time()

            if waitKey(1) == 27:
                destroyAllWindows()
                self.stop = True
                if self.flash[self.win_id-1]:
                    if self.connect[self.win_id-1]:
                        get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/disabletorch')
                if self.overlay[self.win_id-1]:
                    if self.connect[self.win_id-1]:
                        get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/settings/overlay?set=off')
                if self.p1.is_alive():
                    self.p1.join()
                exit()

    def beep(self):
        print('loading song')
        Beep(self.audio_beep[0],
             self.audio_beep[1])

    def r_overlay(self):
        if not self.overlay[self.win_id-1]:
            if self.connect[self.win_id-1]:
                get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/settings/overlay?set=on')
            self.overlay[self.win_id-1] = True
            self.sm = 50
        else:
            if self.connect[self.win_id-1]:
                get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/settings/overlay?set=off')
            self.sm = 0
            self.overlay[self.win_id-1] = False

    def night_vision(self):
        if not self.night[self.win_id-1]:
            if self.connect[self.win_id-1]:
                get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/settings/night_vision?set=on')
            self.night[self.win_id-1] = True
        else:
            if self.connect[self.win_id-1]:
                get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/settings/night_vision?set=off')
            self.night[self.win_id-1] = False

    def wait(self):
        print('wait')
        self.start_time = time()
        self.start_time_2 = time()
        self.start_time_3 = time()
        self.start_time_4 = time()
        self.start_time_5 = time()
        self.start_time_6 = time()
        self.start_time_7 = time()
        self.start_time_8 = time()

    def action_camera(self):
        name = f"{self.ip}_{self.win_id-1}"
        self.img = self.requests_to_img()
        if self.fullscreen:
            namedWindow(name, WND_PROP_FULLSCREEN)
            setWindowProperty(name, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)
        imshow(name, self.img)

    def no_connect(self):
        self.img = imread('no.jpg')

    def action_microphone(self):
        print('connect to microphone')
        if self.connect[self.win_id-1]:
            self.p1_desk = lambda: self.audio_stream()
            self.p1 = Thread(target=self.p1_desk)
            self.stop = False
            if not self.p1.is_alive():
                if self.win_id <= len(self.ips)-1:
                    self.p1.start()
                else:
                    self.win_id = 0
                    self.p1.start()
        else:
            pass
        print('microphone connected')

    def send_to_android(self):
        print('send api[flashlight]')
        if not self.flash[self.win_id-1]:
            self.start_time_flash = time()
            if self.battery_pie[self.win_id-1] > 0:  # if self.battery_pie[self.win_id] >= 0:  #

                self.flash[self.win_id-1] = True
                if self.connect[self.win_id-1]:
                    get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/enabletorch')
            else:
                self.battery_pie[self.win_id] = 0
        else:
            self.time_flash[self.win_id-1] -= round(self.end_flash_time - self.start_time_flash)
            self.flash[self.win_id-1] = False
            if self.connect[self.win_id-1]:
                get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/disabletorch')

    def resize_windows(self):
        self.img = resize(self.img, self.size_windows)

    def text_cam(self, text, pos, font_size, text_size, color, down=False):
        self.img = putText(self.img, text, (pos[0], (pos[1]+self.sm) if not down else pos[1]),
                           FONT_HERSHEY_SIMPLEX, text_size, color, font_size)

    def audio_stream(self):
        try:
            self.audio_ = get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/audio.wav', stream=True)
            ch = self.audio_.iter_content(chunk_size=44100)
            p = PyAudio()
            audio = p.open(channels=1, format=paInt16, rate=44100, output=True)
            for c in ch:
                if not self.stop:
                    audio.write(c)
                else:
                    break
        except cError as ce:
            print(ce)
            self.error()

    def format_pr(self):
        self.text_cam("".join("|" for self.i in range(self.count_battery_pie)),
                      (self.size_windows[0]//10, self.size_windows[1]-20), 6, 0.7, (0, 0, 255))
        self.text_cam(self.format_line, (self.size_windows[0]//10, self.size_windows[1]-20), 6, 0.7, (0, 255, 0))
        bp = str(int(self.battery_pie[self.win_id-1]))
        rbp =lambda count: round(float(self.count_battery_pie)/count)
        self.cord = ((self.size_windows[0]//11)-15, self.size_windows[1]-20)
        self.text_cam(bp, self.cord, 3, 0.7, (0, 0, 0))
        if int(bp) >= 0:
            if rbp(1)>= int(bp) >= rbp(1.5):
                self.text_cam(bp, self.cord, 3, 0.7, (0, 255, 0))
            elif rbp(1.5) >= int(bp) >= rbp(3):
                self.text_cam(bp, self.cord, 3, 0.7, (0, 255, 255))
            else:
                self.text_cam(bp, self.cord, 3, 0.7, (0, 0, 255))
        else:
            self.text_cam('0', self.cord, 3, 0.7, (0, 0, 255))

    def info(self):
        if self.night[self.win_id-1]:
            self.text_cam(f'night vision: {str(self.night[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-80), 2, 0.7, (0, 255, 0),
                          down=True)
        else:
            self.text_cam(f'night vision: {str(self.night[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-80), 2, 0.7, (0, 0, 255),
                          down=True)
        if self.flash[self.win_id-1]:
            self.text_cam(f'flashlight: {str(self.flash[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-20), 2, 0.7, (0, 255, 0), down=True)
        else:
            self.text_cam(f'flashlight: {str(self.flash[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-20), 2, 0.7, (0, 0, 255), down=True)
        if self.overlay[self.win_id-1]:
            self.text_cam(f'overlay: {str(self.overlay[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-50), 2, 0.7, (0, 255, 0), down=True)
        else:
            self.text_cam(f'overlay: {str(self.overlay[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-50), 2, 0.7, (0, 0, 255), down=True)
        if self.microphone_list[self.win_id-1]:
            self.text_cam(f'microphone: {str(self.microphone_list[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-110), 2, 0.7, (0, 255, 0),
                          down=True)
        else:
            self.text_cam(f'microphone: {str(self.microphone_list[self.win_id-1])}',
                          (self.size_windows[0]-270, self.size_windows[1]-110), 2, 0.7, (0, 0, 255),
                          down=True)
        if self.camera_list[self.win_id-1]:
            self.text_cam(f'camera: {str(self.camera_list[self.win_id-1])}', (1650, 940), 2, 0.7, (0, 255, 0),
                          down=True)
        else:
            self.text_cam(f'camera: {str(self.camera_list[self.win_id-1])}', (1650, 940), 2, 0.7, (0, 0, 255),
                          down=True)
        n1 = self.update_send_to_android-(time() - self.start_time_4)
        n2 = self.update_send_to_android-(time() - self.start_time_2)
        n3 = self.update_send_to_android-(time() - self.start_time_3)
        n4 = self.update_send_to_android-(time() - self.start_time)
        n5 = self.update_send_to_android-(time() - self.start_time_6)
        n6 = self.update_send_to_android-(time() - self.start_time_7)
        _n = lambda n: round(n*10)/10 if n>0 else 0
        self.text_cam(f'time to update "F": {_n(n1)}',
                      (self.size_windows[0]-270, self.size_windows[1]-170), 2, 0.7, (255, 255, 255), down=True)
        self.text_cam(f'time to update "O": {_n(n2)}',
                      (self.size_windows[0]-270, self.size_windows[1]-200), 2, 0.7, (255, 255, 255), down=True)
        self.text_cam(f'time to update "N": {_n(n3)}',
                      (self.size_windows[0]-270, self.size_windows[1]-230), 2, 0.7, (255, 255, 255), down=True)
        self.text_cam(f'time to update "M": {_n(n5)}',
                      (self.size_windows[0]-270, self.size_windows[1]-260), 2, 0.7, (255, 255, 255), down=True)
        self.text_cam(f'time to update "C": {_n(n6)}',
                      (self.size_windows[0]-270, self.size_windows[1]-290), 2, 0.7, (255, 255, 255), down=True)
        self.text_cam(f'time to update win: {_n(n4)}',
                      (self.size_windows[0]-270, self.size_windows[1]-320), 2, 0.7, (255, 255, 255), down=True)

    def key_press_option_(self):
        if not self.flash[self.win_id-1]:
            self.time_std = time()
        if is_pressed('f'):
            if time() - self.start_time_4 > self.update_send_to_android:
                self.send_to_android()
                self.start_time_4 = time()
        if self.flash[self.win_id-1]:
            self.end_flash_time = time()
        if self.end_flash_time:
            if self.end_flash_time - self.start_time_5 > 1 / (self.count_battery_pie / self.full_time_flash):
                self.battery_pie[self.win_id-1] -= 1
                self.start_time_5 = time()
            self.format_line = ''.join('|' for self.i in range(round(self.battery_pie[self.win_id-1])))
            if (self.end_flash_time - self.start_time_flash) > self.time_flash[self.win_id-1] + 1:
                self.send_to_android()
            if self.flash[self.win_id-1]:
                self.format_pr()
            else:
                self.format_pr()
        else:
            self.format_pr()
        if is_pressed('o'):
            if time() - self.start_time_2 > self.update_send_to_android:
                self.r_overlay()
                self.start_time_2 = time()
        if is_pressed('n'):
            if time() - self.start_time_3 > self.update_send_to_android:
                self.night_vision()
                self.start_time_3 = time()
        if is_pressed('r'):
            if time() - self.start_time_3 > self.update_send_to_android:
                try:
                    self.take()
                    self.connect[self.win_id-1] = True
                    self.action_microphone()
                except cError as ce:
                    print(ce)
                self.start_time_8 = time()

    def error(self):
        self.img = imread(self.locate_to_img + 'no.jpg')
        self.connect[self.win_id-1] = False

    def take(self):
        try:
            self.req = get(f'http://{self.ips[self.win_id-1]}:{port[self.win_id-1]}/shot.jpg')
            self.req_context = self.req.content
            self.numpy_img = array(bytearray(self.req_context), dtype=uint8)
            self.img = imdecode(buf=self.numpy_img, flags=-1)
        except error as er:
            print(er)

    def requests_to_img(self):
        try:
            if self.connect[self.win_id-1]:
                if self.camera_list[self.win_id-1]:
                    self.take()
                else:
                    self.img = imread(self.locate_to_img + 'off.png')
                self.connect[self.win_id-1] = True
            else:
                self.img = imread(self.locate_to_img + 'no.jpg')
        except cError as ce:
            print(ce)
            self.error()
        self.resize_windows()
        self.text_cam(self.ips[self.win_id-1], (0, 25), 2, 0.7, (255, 255, 255))
        self.text_cam(f"cam {self.win_id}", (0, 50), 2, 0.7, (255, 255, 255))
        # key_press
        self.key_press_option_()
        #

        # info
        self.info()
        #
        return self.img


class ips:
    def __init__(self):
        self.split_data = []
        self.root = Tk()
        self.root.title('ips webcam')
        self.root.geometry('400x500')
        self.buttonVar = BooleanVar()
        self.buttonVar.set(False)
        self.var = False
        self.root.resizable(width=False, height=False)
        self.root['background'] = '#ffb700'
        self.label = ttk.Label(self.root, text='ips', padding=10, font='Times 15 bold', background='#ffb700')
        self.label.pack()
        self.button = Checkbutton(self.root, text='edit mode', bg="#ffb700", activebackground="#ffb700")
        self.button['var'] = self.buttonVar
        self.button['onvalue'] = True
        self.button['offvalue'] = False
        self.button['command'] = self.check
        self.button.pack()
        self._input = Text(self.root, font='Arial 16 bold')
        self._input['bg'] = '#242424'
        self._input['fg'] = '#e6e6e6'
        self._input['pady'] = 10
        self._input['padx'] = 5
        self.label_text = ''
        with open('ips.cfg', 'r') as file:
            self.label_text = file.read()
            self.label_ips = Label(self.root, text=self.label_text, bg='#242424', width=100, height=13)
            self.label_ips['font'] = 'Arial 16 bold'
            self.label_ips['fg'] = '#e6e6e6'
            self.label_ips.pack()
            file.close()
        self._input.pack_forget()
        self.root.bind('<Escape>', self._exit)
        self.root.mainloop()

    def check(self):
        self.var = self.buttonVar.get()
        if self.var:
            self._input.pack()
            self._input.delete(1.0, 'end')
            self._input.insert('end', self.label_text)
            self.label_ips.pack_forget()
        else:
            self._input.pack_forget()
            self.label_ips.pack()

    def _exit(self, args):
        print(args)
        if self.var:
            data0 = str(self._input.get('1.0', 'end'))
            with open('ips.cfg', 'w') as file:
                file.write(data0)
                file.close()
        else:
            data0 = self.label_text
        print(data0)
        self.split_data = data0.split('\n')[:-1]
        self.root.quit()
        self.root.destroy()


class Settings:
    def lab(self, text, x, y, font):
        self.label = Label(self.root)
        self.label['text'] = text
        self.label['bg'] = self.color_d
        self.label['font'] = font
        self.label.place(x=x, y=y)

    def exit(self, args):
        print(args)
        self.con['DEFAULT']['locate_to_img'] = str(self.input6.get())
        self.con['DEFAULT']['update_send_to_android'] = str(self.input7.get())
        self.con['DEFAULT']['full_time_flash'] = str(self.input8.get())
        self.con['DEFAULT']['size_windows'] = f'{str(self.input2.get())} {str(self.input3.get())}'
        self.con['DEFAULT']['audio_beep'] = f'{str(self.input4.get())} {str(self.input5.get())}'
        self.con['DEFAULT']['count_battery_pie'] = str(self.input1.get())
        self.con['DEFAULT']['use_microphone'] = str(self.check1.get())
        self.con['DEFAULT']['use_camera'] = str(self.check2.get())
        self.con['DEFAULT']['fullscreen'] = str(self.check3.get())
        with open('config.ini', 'w') as file:
            self.con.write(file)
        self.root.quit()
        self.root.destroy()

    def __init__(self):
        x = 20
        y_ot_setting = 35
        c = [i*5 for i in range(200)]
        self.con = configparser.ConfigParser()
        self.con.read('config.ini')
        self.label = None
        self.locate = self.con['DEFAULT']['locate_to_img']
        self.update = self.con['DEFAULT']['update_send_to_android']
        self.full_time = self.con['DEFAULT']['full_time_flash']
        self.size_windows = self.con['DEFAULT']['size_windows']
        self.audio = self.con['DEFAULT']['audio_beep']
        self.count_pie = self.con['DEFAULT']['count_battery_pie']
        self.use_microphone = self.con['DEFAULT']['use_microphone']
        self.use_camera = self.con['DEFAULT']['use_camera']
        self.fullscreen = self.con['DEFAULT']['fullscreen']
        self.split_data = []
        self.root = Tk()
        self.root.title('Настройки')
        self.color_d = '#ffb700'
        self.root.geometry('400x500')
        self.root.resizable(width=False, height=False)
        self.root['background'] = self.color_d
        self.check1 = BooleanVar()
        self.check2 = BooleanVar()
        self.check3 = BooleanVar()
        self.check1.set(True if self.con['DEFAULT']['use_microphone'] == 'True' else False)
        self.check2.set(True if self.con['DEFAULT']['use_camera'] == 'True' else False)
        self.check3.set(True if self.con['DEFAULT']['fullscreen'] == 'True' else False)
        self.lab('Настройки', 100+x, c[5], "Times 20 bold")
        self.lab('количество ячеек в батареи', 65+x, c[16], "Times 11")
        self.lab('включать микрофон при старте', 55+x, c[22], "Times 11")
        self.lab('включать камеру при старте', 65+x, c[28], "Times 11")
        self.lab('расположение до фонов', 80+x, c[34], "Times 11")
        self.lab('Частота отправки покетов', 65+x, c[40], "Times 11")
        self.lab('Количество секунд работы фонарика', 20+x, c[46], "Times 11")
        self.lab('Полноэкранный режим', 95+x, c[52], "Times 11")
        self.input6 = Entry(self.root, width=3)
        self.input6.insert('end', self.locate)
        self.input6.place(x=293, y=c[34])
        self.input7 = Entry(self.root, width=3)
        self.input7.insert('end', self.update)
        self.input7.place(x=295, y=c[40])
        self.input8 = Entry(self.root, width=3)
        self.input8.insert('end', self.full_time)
        self.input8.place(x=335, y=c[46])
        self.checking = Checkbutton(self.root, bg=self.color_d, activebackground=self.color_d, var=self.check1)
        self.checking2 = Checkbutton(self.root, bg=self.color_d, activebackground=self.color_d, var=self.check2)
        self.checking3 = Checkbutton(self.root, bg=self.color_d, activebackground=self.color_d, var=self.check3)
        self.checking['onvalue'] = True
        self.checking['offvalue'] = False
        self.checking2['onvalue'] = True
        self.checking2['offvalue'] = False
        self.checking3['onvalue'] = True
        self.checking3['offvalue'] = False
        self.checking.place(x=325, y=c[22])
        self.checking2.place(x=310, y=c[28])
        self.checking3.place(x=300, y=c[52])
        self.input1 = Entry(self.root, width=3)
        self.input1.insert('end', self.count_pie)
        self.input1.place(x=295+x, y=c[16])
        self.lab('Размер окна', 115+x, c[22+y_ot_setting], "Times 15 bold")  # 25
        self.lab('ширина окна', 110+x, c[30+y_ot_setting], "Times 11")  # 25
        self.lab('высота окна', 115+x, c[36+y_ot_setting], "Times 11")  # 25
        self.scale = self.size_windows.split()
        self.input2 = Entry(self.root, width=4)
        self.input2.insert('end', self.scale[0])
        self.input2.place(x=225+x, y=c[30+y_ot_setting])
        self.input3 = Entry(self.root, width=4)
        self.input3.insert('end', self.scale[1])
        self.input3.place(x=225+x, y=c[36+y_ot_setting])
        self.music = self.audio.split()
        self.lab('звук переключения на следующий ip', 40, c[46+y_ot_setting], "Times 12 bold")
        self.lab('частота звука', 135, c[52+y_ot_setting], "Times 11")
        self.lab('продолжительность звука', 85, c[58+y_ot_setting], "Times 11")  # 25
        self.input4 = Entry(self.root, width=4)
        self.input4.insert('end', self.music[0])
        self.input4.place(x=250, y=c[52+y_ot_setting])
        self.input5 = Entry(self.root, width=3)
        self.input5.insert('end', self.music[1])
        self.input5.place(x=300, y=c[58+y_ot_setting])
        self.root.bind('<Escape>', self.exit)
        self.root.mainloop()


def _input_():
    _ips = ips().split_data
    print(_ips)
    _id = 0
    for ip in _ips:
        print(ip)
        if ip == '':
            break
        _id+=1
    return _ips[:_id]


if __name__ == '__main__':
    is_all_file_to_dir()
    while 1:
        try:
            Settings()
            data = _input_()
            print(data)
            data = [i.replace(':', ' ').split() for i in data]
            ips_ADDRESS = [i[0] for i in data]
            port = [i[1] for i in data]
            IPweb(ips_ADDRESS)
            break
        except Exception as e:
            print(e)
