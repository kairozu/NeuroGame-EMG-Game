#!/usr/bin/env python
# wxSerialConfigDialog1.py

import wx, serial
import cPickle as pickle
import os

SHOW_BAUDRATE   = 1<<0
SHOW_FORMAT     = 1<<1
SHOW_FLOW       = 1<<2
SHOW_TIMEOUT    = 1<<3
SHOW_ALL = SHOW_BAUDRATE|SHOW_FORMAT|SHOW_FLOW|SHOW_TIMEOUT

try:
    enumerate
except NameError:
    def enumerate(sequence):
        return zip(range(len(sequence)), sequence)

class SerialConfigDialog1(wx.Dialog):  
    def __init__(self, *args, **kwds):
        self.serial1 = kwds['serial1']
        del kwds['serial1']
        self.show = SHOW_ALL
        if kwds.has_key('show'):
            self.show = kwds['show']
            del kwds['show']
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_2 = wx.StaticText(self, -1, "Port")
        self.combo_box_port1 = wx.ComboBox(self, -1, choices=["dummy1", "dummy2", "dummy3", "dummy4", "dummy5"], style=wx.CB_DROPDOWN)
        if self.show & SHOW_BAUDRATE:
            self.label_1 = wx.StaticText(self, -1, "Baudrate")
            self.choice_baudrate = wx.Choice(self, -1, choices=["choice 1"])
        if self.show & SHOW_FORMAT:
            self.label_3 = wx.StaticText(self, -1, "Data Bits")
            self.choice_databits = wx.Choice(self, -1, choices=["choice 1"])
            self.label_4 = wx.StaticText(self, -1, "Stop Bits")
            self.choice_stopbits = wx.Choice(self, -1, choices=["choice 1"])
            self.label_5 = wx.StaticText(self, -1, "Parity")
            self.choice_parity = wx.Choice(self, -1, choices=["choice 1"])
        if self.show & SHOW_TIMEOUT:
            self.checkbox_timeout = wx.CheckBox(self, -1, "Use Timeout")
            self.text_ctrl_timeout = wx.TextCtrl(self, -1, "")
            self.label_6 = wx.StaticText(self, -1, "seconds")
        if self.show & SHOW_FLOW:
            self.checkbox_rtscts = wx.CheckBox(self, -1, "RTS/CTS")
            self.checkbox_xonxoff = wx.CheckBox(self, -1, "Xon/Xoff")
        self.button_ok = wx.Button(self, -1, "OK")
        self.button_cancel = wx.Button(self, -1, "Cancel")

        self.__set_properties()
        self.__do_layout()
        self.SetContentFromPort()
        self.__attach_events()

    def __set_properties(self):
        self.SetTitle("Serial Port Configuration")
        if self.show & SHOW_TIMEOUT:
            self.text_ctrl_timeout.Enable(0)
        self.button_ok.SetDefault()

    def __do_layout(self):
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_basics = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Basics"), wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.label_2, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_5.Add(self.combo_box_port1, 1, 0, 0)
        sizer_basics.Add(sizer_5, 0, wx.RIGHT|wx.EXPAND, 0)
        if self.show & SHOW_BAUDRATE:
            sizer_baudrate = wx.BoxSizer(wx.HORIZONTAL)
            sizer_baudrate.Add(self.label_1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_baudrate.Add(self.choice_baudrate, 1, wx.ALIGN_RIGHT, 0)
            sizer_basics.Add(sizer_baudrate, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_basics, 0, wx.EXPAND, 0)
        if self.show & SHOW_FORMAT:
            sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
            sizer_format = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Data Format"), wx.VERTICAL)
            sizer_6.Add(self.label_3, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_6.Add(self.choice_databits, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_6, 0, wx.EXPAND, 0)
            sizer_7.Add(self.label_4, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_7.Add(self.choice_stopbits, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_7, 0, wx.EXPAND, 0)
            sizer_8.Add(self.label_5, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_8.Add(self.choice_parity, 1, wx.ALIGN_RIGHT, 0)
            sizer_format.Add(sizer_8, 0, wx.EXPAND, 0)
            sizer_2.Add(sizer_format, 0, wx.EXPAND, 0)
        if self.show & SHOW_TIMEOUT:
            sizer_timeout = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Timeout"), wx.HORIZONTAL)
            sizer_timeout.Add(self.checkbox_timeout, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_timeout.Add(self.text_ctrl_timeout, 0, 0, 0)
            sizer_timeout.Add(self.label_6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_2.Add(sizer_timeout, 0, 0, 0)
        if self.show & SHOW_FLOW:
            sizer_flow = wx.StaticBoxSizer(wx.StaticBox(self, -1, "Flow Control"), wx.HORIZONTAL)
            sizer_flow.Add(self.checkbox_rtscts, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_flow.Add(self.checkbox_xonxoff, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 4)
            sizer_flow.Add((10,10), 1, wx.EXPAND, 0)
            sizer_2.Add(sizer_flow, 0, wx.EXPAND, 0)
        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, wx.ALL|wx.ALIGN_RIGHT, 4)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        sizer_2.SetSizeHints(self)
        self.Layout()

    def __attach_events(self):
        wx.EVT_BUTTON(self, self.button_ok.GetId(), self.OnOK)
        wx.EVT_BUTTON(self, self.button_cancel.GetId(), self.OnCancel)
        if self.show & SHOW_TIMEOUT:
            wx.EVT_CHECKBOX(self, self.checkbox_timeout.GetId(), self.OnTimeout)

    def OnOK(self, events):
        success = True
        success = self.SetPortsFromContent()    
        if success:
            self.EndModal(wx.ID_OK)

    def OnCancel(self, events):
        self.EndModal(wx.ID_CANCEL)

    def OnTimeout(self, events):
        if self.checkbox_timeout.GetValue():
            self.text_ctrl_timeout.Enable(True)
        else:
            self.text_ctrl_timeout.Enable(False)

    def SetContentFromPort(self):
        index = 0                               # fill in ports and select current setting
        self.combo_box_port1.Clear()
        for n in range(4):
            portname = serial.device(n)
            self.combo_box_port1.Append(portname)
            if self.serial1.portstr == portname:
                index = n
        if self.serial1.portstr is not None:
            self.combo_box_port1.SetValue(str(self.serial1.portstr))
        else:
            self.combo_box_port1.SetSelection(index)
            
        if self.show & SHOW_BAUDRATE:
            #fill in badrates and select current setting
            self.choice_baudrate.Clear()
            for n, baudrate in enumerate(self.serial1.BAUDRATES):
                self.choice_baudrate.Append(str(baudrate))
                if self.serial1.baudrate == baudrate:
                    index = n
            self.choice_baudrate.SetSelection(index)
        if self.show & SHOW_FORMAT:
            #fill in databits and select current setting
            self.choice_databits.Clear()
            for n, bytesize in enumerate(self.serial1.BYTESIZES):
                self.choice_databits.Append(str(bytesize))
                if self.serial1.bytesize == bytesize:
                    index = n
            self.choice_databits.SetSelection(index)
            #fill in stopbits and select current setting
            self.choice_stopbits.Clear()
            for n, stopbits in enumerate(self.serial1.STOPBITS):
                self.choice_stopbits.Append(str(stopbits))
                if self.serial1.stopbits == stopbits:
                    index = n
            self.choice_stopbits.SetSelection(index)
            #fill in parities and select current setting
            self.choice_parity.Clear()
            for n, parity in enumerate(self.serial1.PARITIES):
                self.choice_parity.Append(str(serial.PARITY_NAMES[parity]))
                if self.serial1.parity == parity:
                    index = n
            self.choice_parity.SetSelection(index)
        if self.show & SHOW_TIMEOUT:
            if self.serial1.timeout is None:                            # set the timeout mode and value
                self.checkbox_timeout.SetValue(False)
                self.text_ctrl_timeout.Enable(False)
            else:
                self.checkbox_timeout.SetValue(True)
                self.text_ctrl_timeout.Enable(True)
                self.text_ctrl_timeout.SetValue(str(self.serial1.timeout))
        if self.show & SHOW_FLOW:
            self.checkbox_rtscts.SetValue(self.serial1.rtscts)          # set the rtscts mode
            self.checkbox_xonxoff.SetValue(self.serial1.xonxoff)        # set the rtscts mode

        success = True
        
    def SetPortsFromContent(self):
        success = True
        #self.serial1.port = str(self.combo_box_port1.GetValue())
        #print("1x: " + self.serial1.portstr)
        #self.serial1.port = self.serial1.portstr
        if self.show & SHOW_BAUDRATE:
            self.serial1.baudrate = self.serial1.BAUDRATES[self.choice_baudrate.GetSelection()]
        if self.show & SHOW_FORMAT:
            self.serial1.bytesize = self.serial1.BYTESIZES[self.choice_databits.GetSelection()]
            self.serial1.stopbits = self.serial1.STOPBITS[self.choice_stopbits.GetSelection()]
            self.serial1.parity   = self.serial1.PARITIES[self.choice_parity.GetSelection()]
        if self.show & SHOW_FLOW:
            self.serial1.rtscts   = self.checkbox_rtscts.GetValue()
            self.serial1.xonxoff  = self.checkbox_xonxoff.GetValue()
        if self.show & SHOW_TIMEOUT:
            if self.checkbox_timeout.GetValue():
                try:
                    self.serial1.timeout = float(self.text_ctrl_timeout.GetValue())
                except ValueError:
                    dlg = wx.MessageDialog(self, 'Timeout must be a numeric value',
                                                'Value Error', wx.OK | wx.ICON_ERROR)
                    dlg.ShowModal()
                    dlg.Destroy()
                    success = False
            else:
                self.serial1.timeout = None
        return success
    
    def Save(self): # save dialog contents
        f = file('wxSerialConfigDialog1.pkl', 'w')
        pickle.dump(self.serial1.baudrate, f)
        pickle.dump(self.serial1.bytesize, f)
        pickle.dump(self.serial1.stopbits, f)
        pickle.dump(self.serial1.parity, f)
        pickle.dump(self.serial1.rtscts, f)
        pickle.dump(self.serial1.xonxoff, f)
        pickle.dump(self.serial1.timeout, f)
        success = True

    def Load(self): # save dialog contents
        if not os.path.exists("wxSerialConfigDialog1.pkl"):
            self.Save()
        else:
            f = file('wxSerialConfigDialog1.pkl', 'r')
            #self.serial1.portstrholder = pickle.load(f)
            self.serial1.baudrate = pickle.load(f)
            self.serial1.bytesize = pickle.load(f)
            self.serial1.stopbits = pickle.load(f)
            self.serial1.parity = pickle.load(f)
            self.serial1.rtscts = pickle.load(f)
            self.serial1.xonxoff = pickle.load(f)
            self.serial1.timeout = pickle.load(f)

            self.SetContentFromPort()
            success = True

class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        
        ser1 = serial.Serial()
        print ser1
        #loop until cancel is pressed, old values are used as start for the next run
        #show the different views, one after the other
        #value are kept.
        for flags in (SHOW_BAUDRATE, SHOW_FLOW, SHOW_FORMAT, SHOW_TIMEOUT, SHOW_ALL):
            dialogSerialConfig = SerialConfigDialog2(None, -1, "", serial1=ser1, show=flags)
            self.SetTopWindow(dialogSerialConfig)
            result = dialogSerialConfig.ShowModal()
            print ser
            if result != wx.ID_OK:
                break
        #the user can play around with the values, CANCEL aborts the loop
        while 1:
            dialogSerialConfig = SerialConfigDialog2(None, -1, "", serial1=ser1)
            self.SetTopWindow(dialogSerialConfig)
            result = dialogSerialConfig.ShowModal()
            print ser1
            if result != wx.ID_OK:
                break
        return 0

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
