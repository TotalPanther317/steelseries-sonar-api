from sonar import Sonar
from tkinter import *
import threading, time, rtmidi
import devices

sonar = Sonar() #create Sonar object
tk = Tk() #create Tk object
midiin = rtmidi.RtMidiIn() #create midi object

#doubleVars for storing the volume
var_media = DoubleVar()
var_chat = DoubleVar()
var_game = DoubleVar()
var_aux = DoubleVar()
var_mic = DoubleVar()

#make the tk beautiful
tk.config(bg='black')
tk.attributes("-topmost", True)

#set this variable to set a device on start
current_device = "start"

def process_midi(midi):
    if True:
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
        converted = ((midi.getControllerValue()*0.79)/100)
        if midi.getControllerNumber() == 2:
            sonar.set_volume('chatRender', converted)
        elif midi.getControllerNumber() == 3:
            sonar.set_volume('game', converted)
        elif midi.getControllerNumber() == 4:
            sonar.set_volume('media', converted)
        elif midi.getControllerNumber() == 5:
            sonar.set_volume('aux', converted)
        elif midi.getControllerNumber() == 0:
            sonar.set_volume_mic('chatCapture', converted)

def toggleDevice():
    global current_device
    if current_device == "start":
        print(str(devices.getPrimary()))
        current_device = "speakers" #it needs to be that because this will twice on starting
    elif current_device == "headset":
        id = str(devices.getSecondary())
        if id == 0:
            current_device = "headset"
        else:
            button_device.config(text='Monitoring:\nUsing\nSpeakers')
            current_device = "speakers"
            print("speakers_id: ", id)
            sonar.set_monitoring_device_id(id)
    elif current_device == "speakers":
        id = str(devices.getPrimary())
        button_device.config(text='Monitoring:\nUsing\nHeadset')
        current_device = "headset"
        print("headset_id: ", id)
        sonar.set_monitoring_device_id(id)
    
# create some labels
Label(tk, bg='black', fg='white', text='Devices').grid(row=1, column=1, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Game').grid(row=1, column=2, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Chat').grid(row=1, column=3, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Media').grid(row=1, column=4, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Aux').grid(row=1, column=5, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Mic').grid(row=1, column=6, padx=0, pady=0)

# device change button
button_device = Button(tk, text='Monitoring:\nUsing\nHeadset', bg='black', fg='white', command=toggleDevice)
button_device.grid(row=2, column=1, padx=0, pady=0)

# create Sliders (set to disabled to prevent interfering with the midi device)
fader_game = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_game, state=DISABLED)
fader_game.grid(row=2, column=2, padx=0, pady=0)

fader_chat = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_chat, state=DISABLED)
fader_chat.grid(row=2, column=3, padx=0, pady=0)

fader_media = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_media, state=DISABLED)
fader_media.grid(row=2, column=4, padx=0, pady=0)

fader_aux = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_aux, state=DISABLED)
fader_aux.grid(row=2, column=5, padx=0, pady=0)

fader_mic = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_mic, state=DISABLED)
fader_mic.grid(row=2, column=6, padx=0, pady=0)

# get midi Devices
ports = range(midiin.getPortCount())

# if a midi device is connected
if ports:
    # open midi port 0
    for i in ports:
        print(midiin.getPortName(i))
    print("Opening port 0!") 
    midiin.openPort(0)
    toggleDevice()
    toggleDevice()

    while True:
        tk.update()
        volume_out = sonar.get_volume_data()

        #getting some values from the json thing and storing them in the corresponding variables
        volume_media = volume_out['devices']['media']['stream']['monitoring']['volume']
        volume_chat = volume_out['devices']['chatRender']['stream']['monitoring']['volume']
        volume_game = volume_out['devices']['game']['stream']['monitoring']['volume']
        volume_aux = volume_out['devices']['aux']['stream']['monitoring']['volume']
        volume_mic = volume_out['devices']['chatCapture']['stream']['streaming']['volume']

        #converting values and putting them into the DoubleVars
        var_media.set((volume_media*100))
        var_chat.set((volume_chat*100))
        var_game.set((volume_game*100))
        var_aux.set((volume_aux*100))
        var_mic.set((volume_mic*100))

        #if there is midi data, put them into this function
        m = midiin.getMessage(250)
        if m:
            process_midi(m)
else:
    print('NO MIDI INPUT PORTS!')
    exit()