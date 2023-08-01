import os.path
import datetime
import pickle
import numpy as np

import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk

import util
import detector
import telegramwrapper


class App:
    def __init__(self):

        
        ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        self.main_window = ctk.CTk()
        self.main_window.title('Endoscopic Mucosal Recognition')
        self.main_window.geometry("1200x520+350+100")

        self.telegram_icon = ctk.CTkImage(light_image=Image.open('icon and logo/telegram.png'),
                                          size=(20,20))

        self.logo_pkm = ctk.CTkImage(light_image=Image.open('icon and logo/logo_pkm.png'),
                                     size=(700,500))

        self.main_window.grid_columnconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(1, weight=1)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_rowconfigure(2, weight=1)
        
        self.menu_page()

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'
        
    def menu_page(self):
        
        for widget in self.main_window.winfo_children():
            widget.destroy()

        self.pkm_label = ctk.CTkLabel(self.main_window, image=self.logo_pkm, text='')
        self.pkm_label.grid(columnspan=2, row=0, column=0, padx=20, pady=20)

        self.start_button = util.get_button(self.main_window, 'Start', '#5dbea3', self.cam_page)
        self.start_button.grid(columnspan=2, row=1, column=0, padx=20, pady=20, sticky='N')

    def cam_page(self):

        for widget in self.main_window.winfo_children():
            widget.destroy()


        self.button_frame = ctk.CTkFrame(self.main_window, fg_color='transparent')
        self.button_frame.grid(row=0, column=1, pady=10, sticky='sw')
        
        self.takephoto_button_main_window = util.get_button(self.button_frame, 'take photo', '#5dbea3', self.takephoto)
        self.takephoto_button_main_window.grid(row=0, column=1, padx=10, pady=10, sticky='S')

        self.menu_button = util.get_button(self.button_frame, 'Menu', '#5dbea3', self.menu_page)
        self.menu_button.grid(row=1, column=1, padx=10, pady=10, sticky='S')

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.grid(row=0, column=0, sticky='S')

        self.bottom_frame = ctk.CTkFrame(self.main_window, fg_color='transparent',height=10)
        self.bottom_frame.grid(row=2, columnspan=2, column=0)

        self.add_webcam(self.webcam_label)

        

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(1)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def takephoto(self):

        for widget in self.main_window.winfo_children():
            widget.destroy()

        self.button_frame = ctk.CTkFrame(self.main_window, fg_color='transparent')
        self.button_frame.grid(row=0, column=1, pady=10, sticky='sw')

        self.predict_button = util.get_button(self.button_frame, 'Predict', 'green', self.predict)
        self.predict_button.grid(row=0, column=1, padx=10, pady=10, sticky='S')

        self.try_again_button = util.get_button(self.button_frame, 'Try Again', 'red', self.cam_page)
        self.try_again_button.grid(row=1, column=1, padx=10, pady=10, sticky='S')

        self.capture_label = util.get_img_label(self.main_window)
        self.capture_label.grid(row=0, column=0, sticky='S')

        self.bottom = ctk.CTkFrame(self.main_window, fg_color='transparent',height=10)
        self.bottom.grid(row=2, columnspan=2, column=0)

        self.add_img_to_label(self.capture_label)

    def add_img_to_label(self, label):

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

    def predict(self):
        
        for widget in self.main_window.winfo_children():
            widget.destroy()
        
        result_arr = detector.predict(self.most_recent_capture_pil)

        self.predict_label = util.get_img_label(self.main_window)
        self.predict_label.grid(row=0, column=0, sticky='S')

        self.orig_image = Image.fromarray(np.flip(result_arr.orig_img, -1))
        self.result_image = Image.fromarray(np.flip(result_arr.plot(), -1))
        
        imgtk = ImageTk.PhotoImage(image=self.result_image)
        self.predict_label.imgtk = imgtk
        self.predict_label.configure(image=imgtk)

        self.button_frame = ctk.CTkFrame(self.main_window, fg_color='transparent')
        self.button_frame.grid(row=0, column=1, pady=10, sticky='sw')

        try:
            self.diagnosed_disease = util.get_text_label(self.button_frame, f'Predicted: {result_arr.names[int(result_arr.boxes.cls)]}')

        except ValueError:
            self.diagnosed_disease = util.get_text_label(self.button_frame, f'Predicted: no Disease Detected')
            
        self.diagnosed_disease.grid(row=0, column=1, padx=10, pady=170, sticky='NW')

        self.try_again_button = util.get_button(self.button_frame, 'Try Again', 'red', self.cam_page)
        self.try_again_button.grid(row=1, column=1, padx=10, pady=10, sticky='S')

        self.send_to_telegram_button = ctk.CTkButton(
                                        self.button_frame,
                                        text='Share',
                                        fg_color='#62c6dd',
                                        command= self.send_to_telegram,
                                        font=('Helvetica bold', 20),
                                        image = self.telegram_icon,
                                        compound = 'right',
                                        border_color = 'black',
                                        corner_radius = 10,
                                        border_width = 2,
                                        width = 150,
                                        height = 40
                                        )   

        self.send_to_telegram_button.grid(row=2, column=1, padx=10, pady=10, sticky='S')

        

    def send_to_telegram(self):
        self.result_image.save('temp_predicted.jpg')
        self.orig_image.save('temp_orig.jpg')
        telegramwrapper.start('temp_orig.jpg', 'temp_predicted.jpg')

        
            
    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
