'''
Green Monster GUI Revamp
Containing ScanUtil Tab
Code Commissioned 2019-01-16
Code by A.J. Zec
'''

import tkinter as tk
from tkinter import ttk
import utils as u

SCAN_GET_DATA	=1001
SCAN_SET_DATA	=1002
SCAN_GET_STATUS	=1003
SCAN_SET_STATUS	=1004
GM_SCN_CHECK	=6002
GM_SCN_SET	=6003
SCN_RADIO_CLN	=6101
SCN_RADIO_NOT	=6102
SCN_RADIO_CLN_BT=0
SCN_RADIO_NOT_BT=1
SCN_INT_CLN	=1
SCN_INT_NOT	=0

class ScanUtil(tk.Frame):
  def __init__(self, tab):
    self.util_frame = tk.LabelFrame(tab, text='SCAN UTILITY', bg=u.green_color)
    self.options = ['CLEAN', 'NOT CLEAN']
    self.clean_setting = tk.StringVar()
    self.clean_setting.set(self.options[0])
    self.inj_frame = tk.LabelFrame(self.util_frame, text='Inj', bg=u.green_color)
    self.inj_labels = [tk.Label(self.inj_frame, text='Set Point 1', bg=u.green_color),
                       tk.Label(self.inj_frame, text='Set Point 2', bg=u.green_color),
                       tk.Label(self.inj_frame, text='Set Point 3', bg=u.green_color),
                       tk.Label(self.inj_frame, text='Set Point 4', bg=u.green_color)]
    self.inj_entries = [tk.Entry(self.inj_frame),
                        tk.Entry(self.inj_frame),
                        tk.Entry(self.inj_frame),
                        tk.Entry(self.inj_frame)]
    for i, op in enumerate(self.options):
      tk.Radiobutton(self.util_frame, text=op, variable=self.clean_setting,
          value=op, bg=u.green_color, command=self.set_status).grid(row=0, column=i, padx=10, pady=10, sticky='W')
    self.fill_inj_frame()
    self.inj_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='W')
    tk.Button(self.util_frame, text='Check Values', bg=u.green_color, command=self.check_values).grid(row=2, column=0, padx=10, pady=10)
    tk.Button(self.util_frame, text='Set Values', bg=u.green_color, command=self.set_values).grid(row=2, column=1, padx=10, pady=10)
    self.util_frame.pack(padx=20, pady=20, anchor='w')
    self.check_values()

  def fill_inj_frame(self):
    for r in range(0, 4):
      self.inj_labels[r].grid(row=r, column=0, padx=15, pady=10, sticky='E')
      u.set_text(self.inj_entries[r], '0').grid(row=r, column=1, padx=10, pady=10, sticky='W')

  def check_status(self):
    packet = [u.COMMAND_SCAN, SCAN_GET_STATUS, 0, 0, 0, "SCN status check", "Y"]
    err_flag, reply = u.send_command(u.Crate_INJ, packet)
    
    if err_flag == u.SOCK_OK:
      iclean = bool(reply[2])
      if (iclean == SCN_INT_NOT):
        self.clean_setting.set(self.options[1])
      elif (iclean == SCN_INT_CLN):
        self.clean_setting.set(self.options[0])
      else:
        print("UNKNOWN REPLY FOR SCN STATUS: " + str(iclean))
        self.clean_setting.set(self.options[1])

    else:
      print(" check_status: ERROR, Could not access socket.")
      return

  def check_values(self):
    i = 0
    while i < 4:
      packet = [u.COMMAND_SCAN, SCAN_GET_DATA, i+1, 0, 0, "Check SCN Data Value", "Y"]
      err_flag, reply = u.send_command(u.Crate_INJ, packet)
    
      if err_flag == u.SOCK_OK:
        value = int(reply[3])
        self.inj_entries[i].delete(0, tk.END)
        self.inj_entries[i].insert(0, str(value))
        print("Value is " + str(value))

      else:
        print(" check_status: ERROR, Could not access socket.")
        return

      i += 1

    self.check_status()

  def set_status(self):
    if self.clean_setting.get() == 'CLEAN':
      status = 1
    else:
      status = 0

    self.set_values()

    packet = [u.COMMAND_SCAN, SCAN_SET_STATUS, status, 0, 0, "SCN Status Change", "Y"]
    err_flag, reply = u.send_command(u.Crate_INJ, packet)
    
    print("Setting SCN status: " + str(status))
    if err_flag == u.SOCK_OK:
      print("SCAN status change call is complete");
    else:
      print(" check_status: ERROR, Could not access socket.")

    self.check_values()

  def set_values(self):
    i = 0
    while i < 4:
      value = int(self.inj_entries[i].get())
      packet = [u.COMMAND_SCAN, SCAN_SET_DATA, i+1, value, 0, "Set SCN Data Value", "Y"]
      err_flag, reply = u.send_command(u.Crate_INJ, packet)
    
      if err_flag == u.SOCK_OK:
        print("Writing new SCAN set point " + str(value) + " to data " + str(i))

      else:
        print(" check_status: ERROR, Could not access socket.")
        return

      i += 1

    self.check_values()

