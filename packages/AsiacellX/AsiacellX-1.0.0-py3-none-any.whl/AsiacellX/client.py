import requests
import json
import re
from .utils.headers import Headers
from .utils.helpers import ExractPID


class Client:
    def __init__(self, PhoneNumber: str, language: str = "ar") -> str:
        self.api = "https://app.asiacell.com/api/v1/"
        self.PhoneNumber = PhoneNumber
        self.access_token = None
        self.lang = language
        self.handshake_token = None
        self.userId = None
        self.refresh_token = None
     
     
     
    def login(self):
        data = {
               "username"     :  self.PhoneNumber,
               "captchaCode"  :  ""
               }
        
        response = requests.post(url=f"{self.api}login?lang={self.lang}", headers=Headers(data).WebHeaders, json=data)
        passPID = ExractPID(response.text)
        return passPID


    def verify_login(self, pid: str, code: int):
        data= {
                  "PID"       :  pid,
                  "passcode"  :  code
                  }
        responseSms = requests.post(url=f"{self.api}smsvalidation?lang={self.lang}", headers=Headers(data).WebHeaders, json=data).json()
        
        self.access_token = responseSms["access_token"]
        self.userId = responseSms["userId"]
        self.refresh_token = responseSms["refresh_token"]
        self.handshake_token = responseSms["handshake_token"]
        return responseSms


    def login_token(self, access_token: str):
        """login with Access Token AsiaCell"""


        self.access_token = access_token
        


    def Recharge(self, NumberCard: str, rechargeType: int = 1):
        data = json.dumps({
               "msisdn"        :  "",
               "voucher"       :  NumberCard,
               "rechargeType"  :  rechargeType
               })
        response = requests.post(url=f"{self.api}top-up?lang={self.lang}", headers=Headers(data).WebHeaders, json=data)
        return response.json()

