
from .helpers import *



access_token=None
APPVERSION = "4.1.2"




class Headers:
    def __init__(self, data = None, deviceId = None):
        self.AppHeaders = {
            "X-ODP-API-KEY": GetApiKey(),
            "DeviceID": GeneratorDeviceIdApp(),
            "X-OS-Version": VersionPlatform(),
            "X-ODP-APP-VERSION": APPVERSION,
            "X-FROM-APP": "odp",
            "X-ODP-CHANNEL": "mobile",
            "Cache-Control": "private, max-age=240",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "odpapp.asiacell.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": UserAgent()
        }
        self.WebHeaders = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "DeviceID": str(GeneratorDeviceIdWeb()),
            "Host": "app.asiacell.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "X-CHANNEL": "PWA",
            "content-type": "application/json; charset=utf-8",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
            }
        if access_token:
            self.WebHeaders["Authorization"] = f"Bearer {access_token}"
        
        if data:
            self.WebHeaders["Content-Length"] = str(len(data))
