import requests
import json
import os


class Sonar:
    # chatCapture -> mic
    channel_names = [ "master", "game", "chatRender", "chatCapture", "media", "aux" ]

    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.load_base_url()
        self.load_server_address()
    
    def load_base_url(self):
        common_app_data_path = os.path.join(os.environ["ProgramData"], "SteelSeries", "SteelSeries Engine 3", "coreProps.json")
        print("Path: ", common_app_data_path)
        with open(common_app_data_path, "r") as rf:
            common_app_data = json.load(rf)
            print("URL from path: ", common_app_data["ggEncryptedAddress"])
            self.base_url = f'https://{common_app_data["ggEncryptedAddress"]}'

    def load_server_address(self):
        app_data = requests.get(self.base_url + "/subApps", verify=False)
        if app_data.status_code != 200:
            print(f'SteelSeries server not accessible! Status code: {app_data.status_code}')
            return False
        app_data_json = json.loads(app_data.text)

        if not app_data_json["subApps"]["sonar"]["isEnabled"]:
            print("SteelSeries Sonar is not enabled!")
            return False

        if not app_data_json["subApps"]["sonar"]["isReady"]:
            print("SteelSeries Sonar is not ready!")
            return False
        
        if not app_data_json["subApps"]["sonar"]["isRunning"]:
            print("SteelSeries Sonar is not running!")
            return False

        self.web_server_address = app_data_json["subApps"]["sonar"]["metadata"]["webServerAddress"]
        if self.web_server_address in ["", None, "null"]:
            print("Sonar webServerAddress not found!")
            return False
        
        print(f'Sonar webServerAddress: {self.web_server_address}')
        return True
    
    def get_volume_data(self):
        volume_info_url = self.web_server_address + "/volumeSettings/streamer"
        volume_data = requests.get(volume_info_url)
        if volume_data.status_code != 200:
            print(f'Sonar server not accessible! Status code: {volume_data.status_code}')
            return {}
        volume_data_json = json.loads(volume_data.text)

        return volume_data_json

    def set_volume(self, channel, volume):
        if channel not in self.channel_names:
            return {"error": True, "message": f"Channel '{channel}' not found!"}
        
        if volume < 0 or volume > 1:
            return {"error": True, "message": f"Invalid volume '{volume}'! Value must be between 0 and 1!"}
        
        url = f'{self.web_server_address}/volumeSettings/streamer/monitoring/{channel}/Volume/{json.dumps(volume)}'
        volume_data = requests.put(url)

        return json.loads(volume_data.text)
    
    def set_streaming_volume(self, channel, volume):
        if channel not in self.channel_names:
            return {"error": True, "message": f"Channel '{channel}' not found!"}
        
        if volume < 0 or volume > 1:
            return {"error": True, "message": f"Invalid volume '{volume}'! Value must be between 0 and 1!"}
        
        url = f'{self.web_server_address}/volumeSettings/streamer/streaming/{channel}/Volume/{json.dumps(volume)}'
        volume_data = requests.put(url)

        return json.loads(volume_data.text)

    def mute_channel(self, channel, muted):
        if channel not in self.channel_names:
            return {"error": True, "message": f"Channel '{channel}' not found!"}

        muted = (muted == True)
        
        url = f'{self.web_server_address}/volumeSettings/streamer/{channel}/Mute/{json.dumps(muted)}'
        mute_data = requests.put(url)

        return json.loads(mute_data.text)

    def set_monitoring_device_id(self, id):
        print("setting: ", id)
        id = str(id)
        id = id.replace("{", "%7B")
        id = id.replace("}", "%7D")
        print("modified: ", id)
        url = f'{self.web_server_address}/streamRedirections/monitoring/deviceId/{id}'
        device_data = requests.put(url)
        device_data.text

    def set_streaming_enable(self, channel, enable):
        url = f'{self.web_server_address}/streamRedirections/streaming/redirections/{channel}/isEnabled/{enable}'
        requests.put(url)

    def get_streaming_data(self):
        volume_info_url = self.web_server_address + "/streamRedirections/"
        volume_data = requests.get(volume_info_url)
        if volume_data.status_code != 200:
            print(f'Sonar server not accessible! Status code: {volume_data.status_code}')
            return {}
        volume_data_json = json.loads(volume_data.text)

        return volume_data_json
