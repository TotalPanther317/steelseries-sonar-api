import os

file = None
file_text = None
after_split = None

def getDump():
    global file, file_text
    os.system(r"dump_devices.bat") #make SoudVolumeView dump everything

    file = open(r"dump.txt", "r") #open the file
    file_text = str(file.readlines()) #put the file into a variable

#doing some weird stuff, it works somehow
def getPrimary():
    getDump()
    location = 0
    location_2 = 0
    location_3 = 0

    after_split = None
    id_in_front = None

    location = file_text.find('Lautsprecher,Device,Render,Realtek(R)') #name of the main device is set here. First goes the word for 'Speaker' in the language of you windows install, 'Device' and 'Render' is mandatory, 'Realtek(R)' is to be replaced with the name of your audio device.
    after_split = file_text[location:]

    location_2 = after_split.find('{')
    id_in_front = after_split[location_2:]

    location_3 = id_in_front.find(',')
    id = id_in_front[:location_3]
    print("Headset Device ID: ", id)
    print()
    print()

    return id

#the same thing again
def getSecondary():
    getDump()
    location = 0
    location_2 = 0
    location_3 = 0

    after_split = None
    id_in_front = None

    location = file_text.find('Lautsprecher,Device,Render,3-') #name of the secondary device is set here. Naming follows the rules for the main device.
    after_split = file_text[location:]

    location_2 = after_split.find('{')
    id_in_front = after_split[location_2:]

    location_3 = id_in_front.find(',')
    id = id_in_front[:location_3]
    print("USB Audio Device ID: ", id)

    #if the secondary device exists, return an id, otherwise return a zero
    device_connected_info = id.find('{')
    print(device_connected_info)
    if device_connected_info == 0:
        print("Device connected")
        return id
    else:
        print("Not connected")
        return 0

