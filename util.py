import os
import pickle

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk



def get_button(window, text, color, command):
    button = ctk.CTkButton(
                        window,
                        text=text,
                        fg_color=color,
                        command=command,
                        width = 150,
                        height = 40,
                        font=('Helvetica bold', 20),
                        border_color = 'black',
                        border_width = 2,
                        corner_radius = 10
                    )

    return button


def get_img_label(window):
    label = tk.Label(window, bg='#EBEBEB')
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = ctk.CTkLabel(window, text=text)
    label.configure(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)
