from sonar import Sonar
from tkinter import *
import threading, time, json#, rtmidi
import devices

try:
    with open('config.json', 'r') as file:
        configFile = file.read()
except:
    print("config file not found")

configJson = json.loads(configFile)

numberGame = configJson["game"]
numberGameStream = configJson["gameStream"]
numberMic = configJson["mic"]
numberChat = configJson["chat"]
numberMedia = configJson["media"]
numberMediaStream = configJson["mediaStream"]
numberAux = configJson["aux"]
numberAuxStream = configJson["auxStream"]
#numberSwitch = configJson["switch"]

sonar = Sonar() #create Sonar object
tk = Tk() #create Tk object
midiin = rtmidi.RtMidiIn() #create midi object

mic_column = 2
game_column = 4
chat_column = 3
media_column = 5
aux_column = 6
stream_game_column = 8
stream_media_column = 9
stream_aux_column = 10

#doubleVars for storing the volume
var_media = DoubleVar()
var_chat = DoubleVar()
var_game = DoubleVar()
var_aux = DoubleVar()
var_mic = DoubleVar()
var_game_stream = DoubleVar()
var_media_stream = DoubleVar()
var_aux_stream = DoubleVar()

stream_media = BooleanVar()
stream_game = BooleanVar()
stream_aux = BooleanVar()

#make the tk beautiful
tk.config(bg='black')
tk.attributes("-topmost", True)

#set this variable to set a device on start
current_device = "start"

def process_midi(midi):
    if True:
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
        converted = ((midi.getControllerValue()*0.79)/100)
        print("converted: ", converted)
        if midi.getControllerNumber() == numberChat:
            sonar.set_volume('chatRender', converted)
        elif midi.getControllerNumber() == numberGame:
            sonar.set_volume('game', converted)
        elif midi.getControllerNumber() == numberMedia:
            sonar.set_volume('media', converted)
        elif midi.getControllerNumber() == numberAux:
            sonar.set_volume('aux', converted)
        elif midi.getControllerNumber() == numberMic:
            sonar.set_streaming_volume('chatCapture', converted)
        elif midi.getControllerNumber() == numberGameStream:
            if(converted > 0.01):
                sonar.set_streaming_enable('game', True)
            else:
                sonar.set_streaming_enable('game', False)
            sonar.set_streaming_volume('game', converted)
        elif midi.getControllerNumber() == numberMediaStream:
            if(converted > 0.01):
                sonar.set_streaming_enable('media', True)
            else:
                sonar.set_streaming_enable('media', False)
            sonar.set_streaming_volume('media', converted)
        elif midi.getControllerNumber() == numberAuxStream:
            if(converted > 0.01):
                sonar.set_streaming_enable('aux', True)
            else:
                sonar.set_streaming_enable('aux', False)
            sonar.set_streaming_volume('aux', converted)

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
Label(tk, bg='black', fg='white', text='Game').grid(row=1, column=game_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Chat').grid(row=1, column=chat_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Media').grid(row=1, column=media_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Aux').grid(row=1, column=aux_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Mic').grid(row=1, column=mic_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='').grid(row=1, column=7, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Game').grid(row=1, column=stream_game_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Media').grid(row=1, column=stream_media_column, padx=0, pady=0)
Label(tk, bg='black', fg='white', text='Aux').grid(row=1, column=stream_aux_column, padx=0, pady=0)


# device change button
button_device = Button(tk, text='Monitoring:\nUsing\nHeadset', bg='black', fg='white', command=toggleDevice)
button_device.grid(row=2, column=1, padx=0, pady=0)

# create Sliders (set to disabled to prevent interfering with the midi device)
fader_game = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_game, state=DISABLED)
fader_game.grid(row=2, column=game_column, padx=0, pady=0)

fader_chat = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_chat, state=DISABLED)
fader_chat.grid(row=2, column=chat_column, padx=0, pady=0)

fader_media = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_media, state=DISABLED)
fader_media.grid(row=2, column=media_column, padx=0, pady=0)

fader_aux = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_aux, state=DISABLED)
fader_aux.grid(row=2, column=aux_column, padx=0, pady=0)

fader_mic = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_mic, state=DISABLED)
fader_mic.grid(row=2, column=mic_column, padx=0, pady=0)

fader_game_stream = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_game_stream, state=DISABLED)
fader_game_stream.grid(row=2, column=8, padx=0, pady=0)

fader_media_stream = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_media_stream, state=DISABLED)
fader_media_stream.grid(row=2, column=stream_media_column, padx=0, pady=0)

fader_aux_stream = Scale(tk, from_ = 100, to = 0, orient = VERTICAL, bg='black', fg='white', variable=var_aux_stream, state=DISABLED)
fader_aux_stream.grid(row=2, column=stream_aux_column, padx=0, pady=0)

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

        streaming_out = sonar.get_streaming_data()
        streaming_out = streaming_out[0] #only important (streaming) data

        #getting some values from the json thing and storing them in the corresponding variables
        volume_media = volume_out['devices']['media']['stream']['monitoring']['volume']
        volume_chat = volume_out['devices']['chatRender']['stream']['monitoring']['volume']
        volume_game = volume_out['devices']['game']['stream']['monitoring']['volume']
        volume_aux = volume_out['devices']['aux']['stream']['monitoring']['volume']
        volume_mic = volume_out['devices']['chatCapture']['stream']['streaming']['volume']
        volume_game_stream = volume_out['devices']['game']['stream']['streaming']['volume']
        volume_media_stream = volume_out['devices']['media']['stream']['streaming']['volume']
        volume_aux_stream = volume_out['devices']['aux']['stream']['streaming']['volume']

        stream_game = streaming_out['status'][2]['isEnabled']
        stream_media = streaming_out['status'][3]['isEnabled']
        stream_aux = streaming_out['status'][4]['isEnabled']


        #converting values and putting them into the DoubleVars
        var_media.set((volume_media*100))
        var_chat.set((volume_chat*100))
        var_game.set((volume_game*100))
        var_aux.set((volume_aux*100))
        var_mic.set((volume_mic*100))
        var_game_stream.set((volume_game_stream*100))
        var_media_stream.set((volume_media_stream*100))
        var_aux_stream.set((volume_aux_stream*100))

        if(stream_game == True):
            fader_game_stream.config(bg='#008000')
        else:
            fader_game_stream.config(bg='black')

        if(stream_media == True):
            fader_media_stream.config(bg='#008000')
        else:
            fader_media_stream.config(bg='black')

        if(stream_aux == True):
            fader_aux_stream.config(bg='#008000')
        else:
            fader_aux_stream.config(bg='black')



        #if there is midi data, put them into this function
        m = midiin.getMessage(250)
        if m:
            process_midi(m)
else:
    print('NO MIDI INPUT PORTS!')
    exit()
